# ===== Stage 1: Assembler =====
FROM python:3.13-slim AS builder

# Base python runtime env + uv settings + venv in /opt/venv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install uv binary (fast deps resolver/installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Tools needed to fetch and unpack the classifier model
RUN apt-get update && apt-get install --no-install-recommends -y \
      curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependency manifests first (better layer cache)
COPY pyproject.toml uv.lock ./

# Create venv + install prod deps (locked, without dev)
RUN uv venv /opt/venv \
    && uv sync --frozen --no-dev --no-install-project

# spaCy pipeline for lemmatization; not a PyPI dependency, so it is fetched here
RUN python -m spacy download ru_core_news_sm

# Fine-tuned RuBERT model, baked in so a fresh container needs no downloads
RUN mkdir -p /opt/model \
    && curl -L -o /tmp/model.zip \
       "https://files.nktkln.com/Projects/Telegram%20News%20Classifier/model/?zip" \
    && unzip -j /tmp/model.zip -d /opt/model \
    && rm /tmp/model.zip

# Copy source code after deps to keep caching efficient
COPY . .

# Install the project itself into the venv (so `python -m news_classifier.main` works)
RUN uv sync --frozen --no-dev

# ===== Stage 2: Final =====
FROM python:3.13-slim AS final

# Runtime python env; use the prebuilt venv binaries
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Paths that differ from the local defaults: the model is baked into the image
# and everything the bot writes goes to /state, which is where a volume belongs
ENV MODEL_PATH=/opt/model \
    DB_PATH=/state/messages.db \
    SESSION_NAME=/state/news_classifier \
    TAXONOMY_PATH=/app/config/categories.yaml \
    FORUM_STATE_PATH=/app/config/forum_state.yaml

# Create unprivileged user (fixed UID/GID for k8s-friendly perms)
RUN groupadd -g 10000 shrimp && \
    useradd -m -u 10000 -g shrimp shrimp

WORKDIR /app

# Bring in venv, model and app from builder stage
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/model /opt/model
COPY --from=builder /app /app

# Fix ownership so non-root user can read/run everything
RUN mkdir -p /state && chown -R shrimp:shrimp /app /opt/venv /opt/model /state

USER shrimp

VOLUME ["/state"]

# Run module as entrypoint; CMD left empty so --login can be appended
ENTRYPOINT ["python", "-m", "news_classifier.main"]
CMD []
