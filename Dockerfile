# Base Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

RUN python -m spacy download ru_core_news_sm

# Download and extract the model
RUN mkdir -p /app/model && \
    curl -L -o /app/model/model.zip https://files.nktkln.com/Projects/Telegram%20News%20Classifier/model/model.zip && \
    unzip /app/model/model.zip -d /app && \
    rm /app/model/model.zip

# Copy the rest of the application files
COPY . .

# Set the entry point
ENTRYPOINT ["python", "-m", "bot.main"]
CMD []
