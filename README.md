# 📣 Telegram News Classifier

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-RuBERT-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Test accuracy](https://img.shields.io/badge/test%20accuracy-0.781-2A6DB2)](./notebooks/model.ipynb)
[![Macro F1](https://img.shields.io/badge/macro%20F1-0.77-2A6DB2)](./notebooks/model.ipynb)
[![Telethon](https://img.shields.io/badge/Telethon-user%20account-26A5E4?logo=telegram&logoColor=white)](https://docs.telethon.dev/)
[![spaCy](https://img.shields.io/badge/spaCy-ru__core__news__sm-09A3D5?logo=spacy&logoColor=white)](https://spacy.io/models/ru)
[![DuckDB](https://img.shields.io/badge/DuckDB-message%20store-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Task](https://img.shields.io/badge/Task-runner-29BEB0?logo=task&logoColor=white)](https://taskfile.dev/)
[![uv](https://img.shields.io/badge/uv-managed-DE5FE9?logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/linting-ruff-D7FF64?logo=ruff&logoColor=black)](https://docs.astral.sh/ruff/)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-2A6DB2.svg)](https://mypy-lang.org/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-FAB040?logo=pre-commit&logoColor=black)](https://pre-commit.com/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-FE5196?logo=conventionalcommits&logoColor=white)](https://www.conventionalcommits.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE.md)

**English** · [Русский](./README.ru.md)

This project explores automatic topic classification for Russian-language
Telegram posts. Its practical goal is to reduce information overload: instead
of reading every channel in a feed, a user can filter posts by the topics they
actually care about.

The repository materials cover the whole ML workflow — collecting and labeling
Telegram posts, exploring and cleaning the data, comparing classification
approaches, and fine-tuning RuBERT.

## 🎯 Project goal

Build a model that assigns a Telegram post to a thematic category based on its
text. The classifier is intended to become the core of a personalized news
filter for Telegram.

The current labels are: politics, personal posts, IT, business, Moscow, science,
finance, miscellaneous content, gaming, advertising, and weather. The source
dataset also carries an `other` label, and all twelve labels are trained on —
the bot drops `personal` and `other` when forwarding instead, through
`exclude_categories`.

## 📊 Dataset

`all_channel_posts.csv` contains 22,099 posts collected from 24 Telegram
channels between August 2023 and December 2024.

| Column | Description |
| --- | --- |
| `message_id` | Telegram message identifier |
| `sender_id` | Source identifier |
| `text` | Original post text |
| `date` | Publication timestamp |
| `channel` | Channel name |
| `category` | Manually assigned topic |

The dataset has no missing values. EDA found 772 duplicated texts and a clear
class imbalance: politics is the largest category with 4,631 posts, while
weather has 406. Because of this imbalance, stratified splitting and metrics
beyond plain accuracy are important.

## 🧹 Text preparation

The preprocessing pipeline:

- converts text to lowercase;
- removes links, hashtags, mentions, HTML/Markdown and special characters;
- lemmatizes Russian words with spaCy;
- removes Russian stop words and common channel boilerplate;
- removes duplicate texts and posts labeled `other`.

The EDA also studies post length, frequent words and n-grams, publication time,
category balance, TF-IDF features, sentence embeddings, and low-dimensional
projections with t-SNE and UMAP.

## 📈 Results

The classifier is `DeepPavlov/rubert-base-cased` fine-tuned over 12 classes —
5 epochs, batch size 8, learning rate 5e-5, sequences truncated to 128 tokens,
the checkpoint picked by 5-fold stratified cross-validation.

On the held-out test set of 2,210 posts:

| Metric | Value |
| --- | --- |
| Accuracy | 0.781 |
| Macro F1 | 0.77 |
| Weighted F1 | 0.78 |
| Macro ROC-AUC | 0.967 |

Cross-validation accuracy stayed in a narrow band across the five folds —
0.7788, 0.7725, 0.7753, 0.7758, 0.7843 — for a mean of 0.777, so the test
figure is not a lucky split.

Per category, sorted by F1:

| Category | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| `political` | 0.92 | 0.92 | **0.92** | 463 |
| `science` | 0.88 | 0.89 | **0.88** | 128 |
| `it` | 0.83 | 0.86 | **0.84** | 241 |
| `weather` | 0.84 | 0.78 | **0.81** | 40 |
| `gaming` | 0.76 | 0.81 | **0.79** | 52 |
| `moscow` | 0.75 | 0.84 | **0.79** | 192 |
| `finances` | 0.81 | 0.76 | **0.78** | 114 |
| `personal` | 0.77 | 0.70 | **0.73** | 339 |
| `advertisement` | 0.80 | 0.64 | **0.71** | 44 |
| `business` | 0.74 | 0.67 | **0.70** | 203 |
| `stuff` | 0.61 | 0.69 | **0.65** | 61 |
| `other` | 0.61 | 0.66 | **0.63** | 333 |

The spread is the interesting part. `political` and `science` have vocabulary of
their own and land above 0.88, while the two catch-all classes — `other` and
`stuff` — sit at the bottom, which is what a catch-all class does: it has no
vocabulary of its own, only the absence of everyone else's. `advertisement` has
the sharpest precision/recall split (0.80 vs 0.64), so roughly a third of ads
still slip through as something else.

### Why a transformer

The obvious question is what a cheap linear model scores on the same data, so
the EDA evaluates two on exactly this split — same `train_test_split`, same five
stratified folds, same 12 classes, same text cleaning:

| Model | CV accuracy | Test accuracy | Test macro F1 |
| --- | --- | --- | --- |
| TF-IDF + LogisticRegression | 0.733 ± 0.006 | 0.736 | 0.714 |
| TF-IDF + LinearSVC | 0.733 ± 0.004 | 0.734 | 0.707 |
| **RuBERT, fine-tuned** | **0.777** | **0.781** | **0.77** |

Fine-tuning buys about 4.5 points of accuracy and 5.6 points of macro F1 over
logistic regression. Most of it comes from the classes where keywords run out —
`other` goes 0.55 → 0.63 F1 and `business` 0.62 → 0.70 — while `political` is
nearly a tie at 0.89 → 0.92, its vocabulary being unmistakable to either model.
The two linear baselines are indistinguishable from each other, which is what
usually happens once the TF-IDF features are fixed.

The baselines are untuned and run without lemmatization, so read 4.5 points as
the upper end of what the transformer is worth here — enough to justify shipping
`torch`, not enough to call a linear model hopeless.

All numbers come from [`notebooks/model.ipynb`](notebooks/model.ipynb) and
[`notebooks/eda.ipynb`](notebooks/eda.ipynb), as the saved cell outputs show
them.

## 📦 Dependencies

* [Python 3.13+](https://www.python.org/downloads/) — the floor in
  `pyproject.toml`, pinned for `uv` in `.python-version`
* [uv](https://docs.astral.sh/uv/getting-started/installation/) — environment
  and lock file
* [Task](https://taskfile.dev/) — every command below is a task
* [Docker](https://docs.docker.com/get-docker/) — only for the container build
* A Telegram **API ID** and **API hash** from
  [my.telegram.org](https://my.telegram.org/auth) — the bot signs in as your
  user account, not as a bot account, because only a user sees the channels you
  subscribe to
* The fine-tuned model from
  [files.nktkln.com](https://files.nktkln.com/Projects/Telegram%20News%20Classifier/model/model.zip)

Everything else, `torch` and `spacy` included, is installed by `task init`.

## 🚀 Running

Install the dependencies, download the spaCy pipeline and install the git hooks:

```sh
task init
```

Unpack the classifier model into `model/` next to `pyproject.toml`:

```sh
curl -L -o model.zip "https://files.nktkln.com/Projects/Telegram%20News%20Classifier/model/model.zip" && unzip -j model.zip -d model && rm model.zip
```

Copy the settings template and fill in your API ID and hash:

```sh
cp .env.example .env
```

Sign in once. Telethon asks for your phone number and the code Telegram sends
you, then writes `news_classifier.session`, which every later run reuses:

```sh
task login
```

Start the bot:

```sh
task run
```

On the first start it creates the forum supergroup and one topic per category,
and records their IDs in `config/forum_state.yaml`. Delete that file and the
next start creates a fresh forum.

## 🔧 Configuration

Credentials and paths live in `.env`, read by `pydantic-settings`; `.env.example`
lists all of them with their defaults.

| Variable | Default | What it is |
| --- | --- | --- |
| `API_ID`, `API_HASH` | — | Telegram credentials; required |
| `SESSION_NAME` | `news_classifier` | Telethon session file, without the extension |
| `MODEL_PATH` | `model` | Directory with the model and its tokenizer |
| `DB_PATH` | `messages.db` | DuckDB file of recently seen posts |
| `TAXONOMY_PATH` | `config/categories.yaml` | Category names and exclusions |
| `FORUM_STATE_PATH` | `config/forum_state.yaml` | Forum and topic IDs; written by the bot |
| `FORUM_TITLE` | `News` | Title of the forum created on the first run |
| `MESSAGE_LIFETIME` | `2` | Hours a post stays a duplicate candidate |
| `SIMILARITY_THRESHOLD` | `0.1` | Jaccard score above which two posts are the same news |
| `SPACY_MODEL` | `ru_core_news_sm` | Pipeline used for lemmatization |
| `DISABLE_LOGGING`, `LOG_LEVEL`, `LOG_PATH` | `false`, `INFO`, empty | Loguru sinks; without `LOG_PATH` logs go to stdout only |

The taxonomy is a structure rather than a knob, so it stays in YAML:

```yaml
categories:
  0: "business"
  1: "it"
  # ...
exclude_categories:
  - 9  # advertisement
exclude_channels: []
```

The keys under `categories` are the class indices the model predicts. Rename
them freely — the names only become topic titles — but never renumber them, and
never add one: a twelfth index is a category the model cannot output.
`exclude_categories` drops a class without retraining and gives it no topic;
`exclude_channels` takes whole channels out, by the negative `-100…` chat ID
Telegram uses for supergroups and channels.

`config/forum_state.yaml` is state, not configuration. The bot writes it, it is
git-ignored, and it is the only thing standing between a restart and a second
forum being created.

> [!IMPORTANT]
> `MESSAGE_LIFETIME` sets both how long posts are kept and how often they are
> deleted, so it decides how far back the duplicate filter can see. Raising it
> catches slower repeats at the cost of comparing against more lemma sets.

## 🧠 How a post is handled

Every new message from a channel goes through the same sequence, and each step
can end it:

| Step | Drops the post when |
| --- | --- |
| Source check | It is not a channel post, has no text, or the channel is in `exclude_channels` |
| Database lookup | Its ID, or the ID of its album, is already stored |
| Duplicate filter | Its lemmas overlap a post from the last `MESSAGE_LIFETIME` hours above `SIMILARITY_THRESHOLD` |
| Classifier | The predicted category is in `exclude_categories` |
| Topic lookup | No topic exists for that category yet |

What is left is forwarded into the topic for its category. Albums are forwarded
whole: the first message of an album waits a second for its siblings to arrive,
so a set of photos does not turn into one photo.

The filter runs on the cleaned text, not the original. `preprocess_text` strips
HTML and Markdown, then everything that is not a Latin or Cyrillic letter, which
is also the form the model was trained on — the same function feeds both the
duplicate check and the classifier, so they can never disagree about what a post
says.

## 🧰 Tasks

`Taskfile.yml` is the interface to the project; `task --list` prints them all.

| Task | Does |
| --- | --- |
| `task init` | Sync dependencies, download the spaCy pipeline, install the git hooks |
| `task login` | Authorize the Telegram session and exit |
| `task run` | Run the bot |
| `task fmt` | `ruff format`, then `ruff check --fix` |
| `task lint` | `ruff check`, format check, `mypy` |
| `task audit` | `pip-audit` against the installed set |
| `task unused-libs` | `deptry` — declared but unused, and undeclared imports |
| `task build` | `uv build` — wheel and sdist |
| `task check` | The full gate: lint, build, audit, unused-libs |
| `task ci` | What a pipeline runs: lint, build |
| `task docker` | Build the image and start the container |
| `task docker-login` | Sign in interactively inside the container |

The `transformers` pin stays at `<5.0.0` because the model in this repository
was fine-tuned and only ever run against 4.x — moving the major version is a
change to validate against the model, not a lock file edit.

## 🐳 Docker

```sh
task docker-build
task docker-login   # first run only, asks for the code Telegram sends you
task docker-run
```

The build is two-stage: the builder resolves from `uv.lock` with
`--frozen --no-dev` into `/opt/venv`, downloads the spaCy pipeline and unpacks
the classifier model into `/opt/model`; the final stage copies those into a
fresh `python:3.13-slim` and runs as `shrimp`, a non-root user with a fixed UID
and GID of `10000`.

The model lives at `/opt/model` rather than in the working directory on purpose:
`compose.yml` mounts `./config` and `./state` into the container, and anything
mounted over `/app` would hide a model that is already in the image. Everything
the bot writes — the session file and the message database — goes to `/state`,
so the image itself stays read-only in practice.

## 📁 Source layout

```
src/news_classifier/
  settings/       AppSettings; the .env contract
  domain/         Post, Taxonomy, ForumState — plain pydantic models
  storage/        DuckDB message store, YAML taxonomy and forum state
  services/       preprocessing, duplicate detection, the classifier
  telegram/       client wiring, forum setup, the message handler
  main.py         entry point; task run calls it as python -m news_classifier.main
config/           categories.yaml (tracked), forum_state.yaml (written by the bot)
utils/            standalone channel exporter, used to build the dataset
notebooks/        training and analysis, see below
data/             the dataset the model was trained on
```

The dataset of classified Telegram posts and the notebooks that produced the
model are documented separately: [`data/README.md`](data/README.md) and
[`utils/README.md`](utils/README.md).

## ✅ ToDo

- [ ] Add a "merge" news function (combine news from different sources into the
      most detailed version).
- [ ] Delete topics when the taxonomy changes.
- [ ] Rewrite the duplicate-news comparison and keep the older posts in a
      vector database.

## 📜 License

This project is licensed under the MIT License. See
[LICENSE.md](./LICENSE.md) for the full text.
