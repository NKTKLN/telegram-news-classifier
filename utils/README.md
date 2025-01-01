# Telegram Message Exporter

## 🗒 Description

This script allows you to fetch and export messages from multiple Telegram channels to individual JSON files. The messages are saved along with important details such as the message ID, sender ID, text content, date, and the channel name.

The script uses the [Telethon](https://github.com/LonamiWebs/Telethon) library to interact with Telegram's API.

## 💾 Prerequisites

Before running this script, you need to have the following:

1. **Python**: Python 3.7 or higher is required.
2. **Telethon**: The script uses the Telethon library to connect to Telegram's API.

You also need to generate your **`api_id`** and **`api_hash`** from the Telegram Developer site.

## ⚙️ Setup

### Step 1: Create a Virtual Environment (optional but recommended)

Using a virtual environment allows you to manage dependencies separately for each project.

1. **Create a virtual environment**:

   If you're using **Windows**:

   ```bash
   python -m venv venv
   ```

   For **Linux/macOS**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:

   - On **Windows**:

     ```bash
     .\venv\Scripts\activate
     ```

   - On **Linux/macOS**:

     ```bash
     source venv/bin/activate
     ```

   After activating the virtual environment, your terminal prompt should change to indicate that you're inside the `venv` environment.

### Step 2: Install Python dependencies

You can install the required dependencies by running the following command:

```bash
pip install telethon
```

### Step 3: Obtain your `api_id` and `api_hash`

To use the Telegram API, you need to create a Telegram application to obtain the `api_id` and `api_hash`.

1. Go to [Telegram's Developer Page](https://my.telegram.org/auth).
2. Log in with your Telegram account.
3. Create a new application and note down your `api_id` and `api_hash`.

### Step 4: Update the script with your credentials

In the script, replace the following placeholders with your actual credentials:

```python
api_id = 'your_api_id'  # Replace with your actual API ID
api_hash = 'your_api_hash'  # Replace with your actual API Hash
```

### Step 5: Configure the message limit (optional)

You can modify the `LIMIT` variable in the script to control how many messages to fetch from each channel. By default, the script fetches the last 3000 messages:

```python
LIMIT = 3000  # Change this value to set a different limit
```

### Step 6: Run the script

Once you have set up everything, you can run the script as follows:

```bash
python telegram_message_exporter.py
```

The script will start fetching messages from all available channels and save them into individual JSON files. Each file will be named after the channel ID, e.g., `123456789_messages.json`.

## Example JSON Format

Each JSON file will have the following format:

```json
[
    {
        "message_id": 123456789,
        "sender_id": 987654321,
        "text": "This is a sample message",
        "date": "2024-12-17T10:00:00",
        "channel": "Sample Channel"
    },
    {
        "message_id": 123456790,
        "sender_id": 987654322,
        "text": "Another sample message",
        "date": "2024-12-17T10:05:00",
        "channel": "Sample Channel"
    }
]
```

## 📃 License

This project is licensed under the MIT License, see [LICENSE.md](/LICENSE.md) for full text.
