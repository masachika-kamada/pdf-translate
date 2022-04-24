# 数式に対応した英語論文PDF翻訳WEBアプリケーション

### 解決したい問題

Google翻訳やDeepLなどの翻訳サイトでPDFを翻訳にかけたときに、数式やギリシャ文字が含まれていると、本文と数式の区別がつかず訳文がおかしくなること

### ソリューション

- AI OCRの文字認識信頼度を使用し、数式箇所を検出し本文と区別して翻訳を行う
- 翻訳文中に使われる英数字の羅列を、数式対応表で読み替える

### デモ画面

![demo](https://user-images.githubusercontent.com/63488322/164994688-4112a46c-dc1b-42ef-ba0a-690882265961.png)

# 使い方

1) リポジトリのクローン
2) secret.jsonを下記のフォーマットで作成しDeepLとAzureのAPIキーを追加

```json
{
    "KEY": "deepl_key",
    "SUBSCRIPTION_KEY": "azure_subscription_key",
    "ENDPOINT": "azure_endpoint"
}
```

3) Streamlit実行

```bash
streamlit run main.py
```

# 紹介記事

[ハッカソンでプレゼンに使用したGoogleスライドの資料](https://docs.google.com/presentation/d/1J3nLaAWF0OZJb9MYbCijdUoWe4SAGd7l/edit?usp=sharing&ouid=115655998262836126293&rtpof=true&sd=true)

# 受賞

第一回技育CAMPハッカソン 努力賞 (2022-04-24)

<img src="https://user-images.githubusercontent.com/63488322/164994336-6dbeade7-8eeb-4b77-a2ee-31641847cca7.png" width="500px">
