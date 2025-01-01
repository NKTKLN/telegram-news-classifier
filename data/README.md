# Dataset of Telegram News Posts

For the Russian version of this dataset description, you can access it [here](README_ru.md).

## 🗒 Description

This dataset contains messages collected from various **Russian** news Telegram channels. It includes two types of files: a separate JSON file for each channel and a consolidated CSV file with all the data. All messages are classified into categories, making the dataset suitable for text classification tasks.

The classification was performed automatically using the **Qwen 2.5** model.

## 📝 Data Structure

1. **Folder with JSON files**: Each file in the folder contains messages from one channel. The file name corresponds to the channel's ID, and its contents are in JSON format, with each object representing an individual post. Example file name: `{channel_id}_messages.json`. The structure of each message is as follows:

```json
{
    "message_id": 11655,
    "sender_id": -1001000724666,
    "text": "Post text",
    "date": "2024-11-07T18:09:50+00:00",
    "channel": "Channel name",
    "category": "category"
}
```

2. **CSV File**: All data from the JSON files are combined into a single CSV file, which includes information about each post, including the channel ID, post text, publication date, and category. The file name is `all_channel_posts.csv`.

Example CSV row:

```csv
message_id,sender_id,text,date,channel,category
11655,-1001000724666,"Дерматологи уточнили причину «рака сари» у носящих эту одежду","2024-11-07T18:09:50+00:00","Naked Science","science"
```

Where:

- **message_id**: Unique identifier for the message.
- **sender_id**: Identifier of the channel or user that sent the message.
- **text**: Post text.
- **date**: Date and time of the post in ISO 8601 format.
- **channel**: Channel name.
- **category**: Post category, one of: `"other"`, `"business"`, `"finances"`, `"political"`, `"personal"`, `"stuff"`, `"gaming"`, `"science"`, `"moscow"`, `"weather"`, `"it"`, `"advertisement"`.

## 📚 Categories

Each post was classified into one of the following categories:

- **other**: Texts that do not fit into any of the other categories.
- **business**: News and information about business.
- **finances**: Texts about finance, markets, economy, and money.
- **political**: News about politics, laws, elections, government bodies.
- **personal**: Personal incidents, unusual or curious cases.
- **stuff**: Entertainment topics, holidays, horoscopes, mystical stories.
- **gaming**: News about video games, esports, gaming events.
- **science**: Science, technology, medicine, research.
- **moscow**: News about Moscow.
- **weather**: Weather-related news: forecasts, disasters.
- **it**: News about IT and technology: software, hardware, devices, programming languages, machine learning.
- **advertisement**: Advertising texts about goods, services, promotions.

## 🔍 Data Sources

The data for this dataset was collected from various **Russian** news Telegram channels. All channels provide public access to their content, except for some that have age restrictions or private links. Below are the links to the channels used (some channels may have age restrictions):

- [msk_live](https://t.me/msk_live)
- [habr_com](https://t.me/habr_com)
- [bbbreaking](https://t.me/bbbreaking)
- [ru2ch](https://t.me/ru2ch)
- [rian_ru](https://t.me/rian_ru)
- [banksta](https://t.me/banksta)
- [bbcrussian](https://t.me/bbcrussian)
- [topor](https://t.me/topor)
- [moscowach](https://t.me/moscowach)
- [mash](https://t.me/mash)
- [nsmag](https://t.me/nsmag)
- [shot_shot](https://t.me/shot_shot)
- [moscowtoplive](https://t.me/moscowtoplive)
- [moskva_tretiy_rim](https://t.me/moskva_tretiy_rim)
- [moscowtop](https://t.me/moscowtop)
- [ENews112](https://t.me/ENews112)
- [moscowmap](https://t.me/moscowmap)
- [goproglib](https://t.me/goproglib)
- [proglibrary](https://t.me/proglibrary)
- [pyproglib](https://t.me/pyproglib)
- [tproger](https://t.me/tproger)
- [topor (18+)](https://t.me/joinchat/ScL1FOCgJCbFNJK1)
- [topor live](https://t.me/+oDf_lVJzbNQyYWFi)
- [cyber topor](https://t.me/+iI538bjZlGJmYWQy)

These channels contain diverse content, covering various topics such as news, technology, economics, and more, with age restrictions for some of them.

## 🚫 Potential Data Inaccuracies

The data was annotated automatically using the **Qwen 2.5** model, and may contain inaccuracies:

- **Incorrect classification**: Some messages may have been assigned to the wrong category, especially if the topic is ambiguous.
- **Errors in text interpretation**: Unusual expressions or slang may have been misclassified.
- **Contextual errors**: The model may not account for the full context of a post.

It is recommended to use this dataset while keeping these potential classification errors in mind.

## 🤔 Applications

This dataset can be used for various tasks such as:

- Text classification.
- Trend analysis of news.
- Research in media content and social networks.
- Training machine learning models for news data analysis.

## 🗃 Directory Structure

```filesystem
/raw
    /{channel_id}_messages.json  # Files with data for each channel
all_channel_posts.csv           # Consolidated CSV file with all the data
README.md                      # This file
```

## 📃 License

The dataset is distributed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENCE.md).
