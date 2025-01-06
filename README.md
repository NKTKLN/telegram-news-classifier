# 📣 Telegram News Classifier

## 🗒 Description

At some point, I realized that most of the posts from the Telegram channels I subscribed to were not informative and lacked value for me. Therefore, I decided to create a bot that sorts out ads and categorizes all the news and posts from the channels I follow.

## ⚙️ Bot Configuration

The configuration file can be found in the `config/example_config.yaml` file. Here's an example of what it should look like:

```yaml
telegram:
  api_id: 1821196
  api_hash: "your_api_hash_here"  # https://my.telegram.org/auth
  session_name: "news_classifier"

bot_settings:
  model_path: "model"
  db_path: "messages.db"

# Optional: Uncomment to exclude categories or channels

# exclude_categories:
#   - 1
#   - 2

# exclude_channels:
#   - 1
#   - 2
```

### How to set it up:

1. Obtain your **API ID** and **API Hash** by logging into [Telegram's Developer Portal](https://my.telegram.org/auth).
2. Replace `your_api_hash_here` with your actual API hash.
3. The `model_path` should point to the folder where the model is located (downloadable from [this link](https://files.nktkln.com/Projects/Telegram%20News%20Classifier/model/model.zip)).
4. The `db_path` is the database where the bot stores the messages.

The `example_config.yaml` is just a template. Once you've filled it with your details, you can rename it to `config.yaml`.

## 🐳 Run in Docker

You can run the bot using Docker. Simply execute:

```bash
docker build -t telegram-news-classifier .
```

### If No Session Exists

If the session file (`news_classifier.session`) is missing, the bot will require you to log in. To do this, run the following command:

```bash
docker run --it -v $(pwd):/app telegram-news-classifier --login
```

This command will initiate the login process, and you will be prompted to enter your phone number and the authentication code from Telegram. After the first login, the session file will be saved and used for future runs.

### Running the Bot (After Session Exists)

If the session file is already present (created after the first login), you can run the bot without the `--login` flag:

```bash
docker run --it -v $(pwd):/app telegram-news-classifier
```

Alternatively, if you're using `docker-compose`, you can run the bot with:

```bash
docker-compose up --build -d
```

## 🔧 Manual Run

Alternatively, you can set up and run it manually using Python and Poetry:

1. Install Poetry if you haven't already: [Poetry installation guide](https://python-poetry.org/docs/#installation).
2. Clone the repository and navigate to the project folder.
3. Download the model from [this link](https://files.nktkln.com/Projects/Telegram%20News%20Classifier/model/model.zip).
4. Install the dependencies by running:

   ```bash
   poetry install
   ```

5. To run the bot, use:

   ```bash
   poetry run python bot/main.py
   ```

## ✅ ToDo

- [ ] Add a "merge" news function (combine news from different sources into the most detailed version).
- [ ] Add deletion of topics if changes have been made to the config.

## 📃 License

This project is licensed under the MIT License. See [LICENSE.md](/LICENSE.md) for the full text.
