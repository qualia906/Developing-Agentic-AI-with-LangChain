# Agentic AI Development with LangChain — Student Workspace

このリポジトリは「**LangChain による Agentic AI 開発入門**」コースの受講者用ワークスペースです。

---

## ディレクトリ構成

```
student_workspace/
├── chap02/          # 第2章：LangChainとLangGraphの基本要素
│   ├── hands-on/    # 講師と一緒に動かすハンズオンコード
│   └── exercise/
│       ├── problem/ # 受講者が記述する穴埋め演習コード
│       └── solution/# 演習の正解コード（解答後に参照）
├── chap03/          # 第3章：Tool呼び出しとMemoryの実装
├── chap04/          # 第4章：MCPの連携とHuman-in-the-Loop
└── chap05/
│   ├── hands-on/
│   ├── exercise/
│   └── app/         # 総仕上げ：Streamlit Webアプリ
```

---

## 環境構築

### Google Colab（第2〜5章 演習5-1まで）

各 Notebook の先頭セルにインストールコマンドが記載されています。  
Google Colab でそのまま実行してください。

**必要な API キー（Colab のシークレットに設定）：**

| キー名 | 説明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI の API キー |
| `LANGCHAIN_API_KEY` | LangSmith の API キー |

### Google Cloud Cloud Shell（第5章 演習5-2）

`chap05/app/` ディレクトリ内の `README.md` を参照してください。

---

## 注意事項

- `exercise/problem/` の Notebook には `# TODO:` コメントがあります。そこに実装を記述してください。
- `exercise/solution/` は演習を終えてから参照してください。
