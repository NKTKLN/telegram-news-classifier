# 📤 Telegram Message Exporter

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/Telethon-user%20account-26A5E4?logo=telegram&logoColor=white)](https://docs.telethon.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE.md)

**Telegram Message Exporter** walks every channel your Telegram account follows
and writes their posts to one JSON file per channel under `data/raw/`. It is the
script the [dataset](../data/README.md) behind the classifier was collected
with, and the one to run again when the model needs more data.

It is a collection tool, not part of the bot: nothing in `src/` imports it, and
it is excluded from the dependency check. What it shares with the bot is the
credentials — the same `API_ID` and `API_HASH` from `.env` — because both sign
in as your user account, which is the only kind of session that can read the
channels you subscribe to.

## 📦 Dependencies

The script needs `telethon` and `loguru`, both already in the project's
dependencies, so the project environment is enough:

```sh
task sync
```

## 🚀 Running

Set `API_ID` and `API_HASH` in `.env` — see the
[main README](../README.md#-configuration) — then run the script from the
project root:

```sh
uv run python utils/telegram_message_exporter.py
```

The first run signs in interactively and stores
`telegram_message_exporter.session`, a session of its own so that a long export
never interferes with the running bot.

## 🔧 What it does

| Setting | Value | Where |
| --- | --- | --- |
| Posts per channel | 3000, newest first | `MESSAGE_LIMIT` |
| Output directory | `data/raw/`, created if missing | `OUTPUT_DIR` |
| File name | `{abs(channel_id)}_messages.json` | `save_messages` |
| Session | `telegram_message_exporter` | `SESSION_NAME` |

Posts without text are skipped, and a channel whose file already exists has the
new posts prepended to the old ones rather than replacing them — so running the
export twice grows the file instead of truncating it, and duplicates are the
caller's problem to deduplicate on `message_id`.

## 📝 Output format

```json
[
    {
        "message_id": 11655,
        "sender_id": -1001000724666,
        "text": "Post text",
        "date": "2024-11-07T18:09:50+00:00",
        "channel": "Naked Science"
    }
]
```

`date` is ISO 8601 as Telegram delivers it, in UTC. The category field the
dataset carries is not written here: it is added later by the classification
notebooks in [`notebooks/`](../notebooks).

## 📜 License

This project is licensed under the MIT License. See
[LICENSE.md](../LICENSE.md) for the full text.
