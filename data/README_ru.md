# Dataset of Telegram News Posts

## Описание

Данный датасет содержит сообщения, собранные с различных новостных Телеграм-каналов. Он включает два типа файлов: для каждого канала отдельный JSON-файл и общий CSV-файл с полными данными. Все сообщения классифицированы по категориям, что позволяет использовать датасет для задач классификации текста.

Классификация была выполнена автоматически с помощью модели **Qwen 2.5**.

## Структура данных

1. **Папка с JSON файлами**: Каждый файл в папке содержит сообщения одного канала. Имя файла соответствует ID канала, а его содержимое представлено в формате JSON, где каждый объект представляет отдельный пост. Пример имени файла: `{channel_id}_messages.json`.

2. **CSV файл**: Все данные из JSON файлов собраны в одном CSV-файле, который включает информацию о каждом сообщении, включая ID канала, текст поста, дату публикации и классификацию. Имя файла: `all_channel_posts.csv`.

Пример строки в CSV:

```csv
message_id,sender_id,text,date,channel,category
11655,-1001000724666,"Дерматологи уточнили причину «рака сари» у носящих эту одежду","2024-11-07T18:09:50+00:00","Naked Science","science"
```

Где:
- **message_id**: Уникальный идентификатор сообщения.
- **sender_id**: Идентификатор канала или пользователя, отправившего сообщение.
- **text**: Текст поста.
- **date**: Дата и время публикации поста в формате ISO 8601.
- **channel**: Название канала.
- **category**: Категория поста, одна из: `"other"`, `"business"`, `"finances"`, `"political"`, `"personal"`, `"stuff"`, `"gaming"`, `"science"`, `"moscow"`, `"weather"`, `"it"`, `"advertisement"`.

## Категории

Каждый пост был классифицирован по одной из следующих категорий:

- **other**: Тексты, не подходящие ни под одну из остальных категорий.
- **business**: Новости и информация о бизнесе.
- **finances**: Тексты о финансах, рынках, экономике, деньгах.
- **political**: Новости о политике, законах, выборах, государственных органах.
- **personal**: Личные происшествия, необычные или курьезные случаи.
- **stuff**: Развлекательные темы, праздники, гороскопы, мистические истории.
- **gaming**: Новости про видеоигры, киберспорт, игровые события.
- **science**: Наука, технологии, медицина, исследования.
- **moscow**: Новости о Москве.
- **weather**: Новости о погоде: прогнозы, катаклизмы.
- **it**: Новости IT и технологий: софт, железо, устройства, языки программирования, машинное обучение.
- **advertisement**: Рекламные тексты о товарах, услугах, акциях.

## Формат файлов

1. **JSON файлы (для каждого канала)**: Каждый файл имеет название в формате `{channel_id}_messages.json`, где содержится список сообщений. Структура каждого сообщения:
```json
{
    "message_id": 11655,
    "sender_id": -1001000724666,
    "text": "Текст поста",
    "date": "2024-11-07T18:09:50+00:00",
    "channel": "Название канала",
    "category": "категория"
}
```

2. **CSV файл**: Все данные, собранные из JSON файлов, представлены в одном CSV-файле `all_channel_posts.csv`.

## Источники данных

Данные для данного датасета были собраны с различных новостных Телеграм-каналов. Все каналы предоставляют публичный доступ к своему контенту, за исключением некоторых, которые имеют возрастные ограничения или приватные ссылки. Ниже приведены ссылки на использованные каналы (некоторые каналы могут быть с возрастными ограничениями):

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

Эти каналы содержат разнообразный контент, охватывающий различные области, такие как новости, технологии, экономика и другие, с учетом возрастных ограничений для некоторых из них.

## Возможные неточности в данных

Данные были размечены автоматически с помощью модели **Qwen 2.5**, и могут содержать неточности:
- **Неверная классификация**: Некоторые сообщения могут быть отнесены к неверной категории, особенно если тема сообщения неоднозначна.
- **Ошибки в интерпретации текста**: Необычные выражения или сленг могут быть неправильно классифицированы.
- **Контекстные ошибки**: Модель может не учитывать полный контекст поста.

Рекомендуется использовать этот датасет с учетом этих возможных ошибок в классификации.

## Применение

Этот датасет можно использовать для различных задач, таких как:
- Классификация текстов.
- Анализ новостных трендов.
- Исследования в области медиаконтента и социальных сетей.
- Обучение моделей машинного обучения для анализа новостных данных.

## Структура директории

```
/raw
    /{channel_id}_messages.json  # Файлы с данными для каждого канала
all_channel_posts.csv           # Общий CSV файл со всеми данными
README.md                      # Этот файл
```

## Лицензия

Датасет распространяется под лицензией [Creative Commons Attribution 4.0 International License (CC BY 4.0)](/LICENCE).

## Контакты

Если у вас есть вопросы, обращайтесь:
- **Телеграм**: [@NKTKLN](https://t.me/NKTKLN)