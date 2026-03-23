# 演習5-2: Streamlit アプリの起動方法（Google Cloud Shell）

このディレクトリには、第5章の総仕上げ演習として作成した  
**記事生成マルチエージェント Web アプリ** のソースコードが含まれています。

---

## ディレクトリ構成

```
chap05/app/
├── app.py           # Streamlit アプリ本体
├── requirements.txt # 依存ライブラリ
└── README.md        # このファイル
```

---

## Google Cloud Shell でのセットアップ

### Step 1: このリポジトリを Cloud Shell にクローンする

```bash
git clone https://github.com/<your-repo>/student_workspace.git
cd student_workspace/chap05/app
```

### Step 2: 依存ライブラリをインストールする

```bash
pip install -r requirements.txt
```

### Step 3: 環境変数を設定する

```bash
export OPENAI_API_KEY="sk-..."
export LANGCHAIN_API_KEY="ls__..."
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="chap05-app"
```

### Step 4: Streamlit アプリを起動する

```bash
streamlit run app.py --server.port 8080
```

### Step 5: Cloud Shell のプレビュー機能でアプリにアクセスする

Cloud Shell ツールバーの **「ウェブでプレビュー」** → **「ポート 8080 でプレビュー」** をクリックします。

---

## アプリの使い方

1. **サイドバー** に OpenAI API キーと LangChain API キーを入力する  
2. **「API キーを設定」** ボタンをクリックする  
3. **「記事のトピックを入力」** テキストボックスに任意のトピックを入力する  
   - 例: `LangChain を使った企業の AI 活用事例`
   - 例: `生成AI時代のエンジニアに求められるスキルセット`
4. **「記事を生成する」** ボタンをクリックする  
5. **Supervisor → Research → Writer → Validator** の順にエージェントが動作し、最終的な記事が生成される

---

## LangSmith でのトレース確認

アプリ実行後、[LangSmith](https://smith.langchain.com/) の  
`chap05-app` プロジェクトで Supervisor → サブエージェントの  
階層的なトレースを確認できます。
