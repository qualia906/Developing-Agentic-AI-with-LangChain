"""
chap05/app/app.py
======================
第5章 総仕上げ演習（演習5-2）：Streamlit で動かす記事生成 AI エージェント
Cloud Shell での実行を想定した Web UI アプリケーション
"""

import os
import streamlit as st
from langchain.agents import create_agent
from langchain.tools import tool

# ─────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────
st.set_page_config(
    page_title="記事生成 AI エージェント | LangChain Multi-Agent",
    page_icon="🤖",
    layout="wide",
)

# ─────────────────────────────────────────
# API キーの読み込み（環境変数 or UI入力）
# ─────────────────────────────────────────
def get_api_keys() -> tuple[str, str]:
    """環境変数またはサイドバーの入力から API キーを取得する"""
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    langchain_key = os.environ.get("LANGCHAIN_API_KEY", "")
    return openai_key, langchain_key


# ─────────────────────────────────────────
# サブエージェントとツールの作成（セッションにキャッシュ）
# ─────────────────────────────────────────
@st.cache_resource
def build_supervisor_agent():
    """マルチエージェントシステムを構築して返す（初回のみ）"""

    # ─── サブエージェント ───
    research_agent = create_agent(
        model="openai:gpt-4o",
        tools=[],
        system_prompt=(
            "あなたはリサーチの専門家です。\n"
            "与えられたトピックについて、重要なポイントを3〜5つ箇条書きでまとめてください。\n"
            "事実に基づいた正確な情報を提供してください。"
        ),
    )

    writer_agent = create_agent(
        model="openai:gpt-4o",
        tools=[],
        system_prompt=(
            "あなたはテクノロジー分野のプロのライターです。\n"
            "提供されたリサーチ情報をもとに、一般のビジネスパーソン向けの\n"
            "わかりやすい記事（300〜500文字）を執筆してください。\n"
            "見出し、本文の構成を工夫して、読みやすい文章にしてください。"
        ),
    )

    validator_agent = create_agent(
        model="openai:gpt-4o",
        tools=[],
        system_prompt=(
            "あなたはコンテンツレビューの専門家です。\n"
            "提供された記事を以下の観点でレビューし、スコアとフィードバックを提供してください：\n"
            "1. 正確性（情報は正しいか）: /10\n"
            "2. 読みやすさ（文章は明瞭か）: /10\n"
            "3. 完成度（構成・内容は十分か）: /10\n"
            "最後に総合スコアと改善提案を述べてください。"
        ),
    )

    # ─── サブエージェントをツールとしてラップ ───
    @tool
    def research(topic: str) -> str:
        """指定されたトピックについてリサーチを行い、重要なポイントをまとめます。

        Args:
            topic: リサーチするトピック
        """
        result = research_agent.invoke(
            {"messages": [{"role": "user", "content": f"以下のトピックについてリサーチしてください：{topic}"}]}
        )
        return result["messages"][-1].content

    @tool
    def write_article(research_result: str, topic: str) -> str:
        """リサーチ結果をもとに、指定トピックの記事を執筆します。

        Args:
            research_result: リサーチ結果
            topic: 記事のトピック
        """
        result = writer_agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"トピック: {topic}\n\n"
                            f"リサーチ結果:\n{research_result}\n\n"
                            "上記の情報をもとに記事を執筆してください。"
                        ),
                    }
                ]
            }
        )
        return result["messages"][-1].content

    @tool
    def validate_article(article: str) -> str:
        """執筆された記事の品質をチェックし、スコアとフィードバックを返します。

        Args:
            article: チェックする記事の本文
        """
        result = validator_agent.invoke(
            {
                "messages": [
                    {"role": "user", "content": f"以下の記事をレビューしてください：\n\n{article}"}
                ]
            }
        )
        return result["messages"][-1].content

    # ─── Supervisor エージェント ───
    supervisor = create_agent(
        model="openai:gpt-4o",
        tools=[research, write_article, validate_article],
        system_prompt=(
            "あなたはコンテンツ制作チームのスーパーバイザーです。\n"
            "ユーザーからトピックが与えられたら、以下のステップで記事制作を管理してください：\n"
            "1. research ツールでトピックをリサーチする\n"
            "2. write_article ツールでリサーチ結果をもとに記事を執筆する\n"
            "3. validate_article ツールで記事の品質をチェックする\n"
            "4. 最終的な記事と品質レポートをまとめてユーザーに提示する\n"
            "日本語で回答してください。"
        ),
    )

    return supervisor


# ─────────────────────────────────────────
# サイドバー
# ─────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ 設定")
    st.markdown("---")

    st.subheader("API キー")
    openai_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.environ.get("OPENAI_API_KEY", ""),
        help="環境変数 OPENAI_API_KEY が設定されている場合は自動入力されます",
    )
    langchain_key_input = st.text_input(
        "LangChain API Key (LangSmith)",
        type="password",
        value=os.environ.get("LANGCHAIN_API_KEY", ""),
        help="LangSmith でトレースを有効にするために使用します",
    )

    if st.button("🔑 API キーを設定", type="primary"):
        if openai_key_input:
            os.environ["OPENAI_API_KEY"] = openai_key_input
        if langchain_key_input:
            os.environ["LANGCHAIN_API_KEY"] = langchain_key_input
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "chap05-app"
        st.success("API キーを設定しました！")

    st.markdown("---")
    st.subheader("🏗️ システム構成")
    st.markdown("""
    ```
    Supervisor Agent
    ├── 📚 Research Agent
    ├── ✍️ Writer Agent
    └── ✅ Validator Agent
    ```
    """)

    st.markdown("---")
    st.caption("第5章 総仕上げ演習 | LangChain Multi-Agent")


# ─────────────────────────────────────────
# メインコンテンツ
# ─────────────────────────────────────────
st.title("🤖 記事生成 AI エージェント")
st.markdown(
    "**Supervisor** が **3つのサブエージェント**（リサーチ・執筆・バリデーション）を "
    "協調させて、高品質な記事を自動生成します。"
)
st.markdown("---")

# トピック入力
topic = st.text_input(
    "📝 記事のトピックを入力してください",
    placeholder="例: LangChain を使った企業の AI 活用事例",
    help="日本語でトピックを入力してください。AIが自動でリサーチ→執筆→品質チェックを実行します。",
)

generate_btn = st.button("🚀 記事を生成する", type="primary", disabled=(not topic))

if generate_btn and topic:
    # API キーチェック
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("❌ OpenAI API キーが設定されていません。サイドバーで設定してください。")
        st.stop()

    # エージェントの進捗を表示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        research_status = st.empty()
    with col2:
        writing_status = st.empty()
    with col3:
        validate_status = st.empty()

    research_status.info("📚 リサーチ中...")
    writing_status.info("⏳ 待機中")
    validate_status.info("⏳ 待機中")

    # 結果表示エリア
    result_area = st.empty()

    with st.spinner("マルチエージェントシステムが記事を生成しています..."):
        try:
            supervisor = build_supervisor_agent()

            # Supervisor を実行（リサーチ→執筆→バリデーションが自動実行される）
            result = supervisor.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"『{topic}』というトピックで記事を作成してください",
                        }
                    ]
                }
            )

            # ステータスを更新
            research_status.success("📚 リサーチ完了")
            writing_status.success("✍️ 執筆完了")
            validate_status.success("✅ 検証完了")

            # 最終回答を表示
            final_answer = result["messages"][-1].content

            st.markdown("---")
            st.subheader("📄 生成結果")
            st.markdown(final_answer)

            # メッセージフローの詳細（折りたたみ）
            with st.expander("🔍 エージェントの実行ログ（上級者向け）"):
                st.caption("Supervisor が各サブエージェントを呼び出した流れを確認できます。")
                for i, msg in enumerate(result["messages"]):
                    msg_type = type(msg).__name__
                    with st.container():
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                st.markdown(
                                    f"**[{i+1}] AIMessage** → 🛠️ `{tc['name']}` を呼び出し"
                                )
                        elif msg_type == "ToolMessage":
                            st.markdown(
                                f"**[{i+1}] ToolMessage** ← `{getattr(msg, 'name', 'unknown')}` の結果 "
                                f"({len(msg.content)} 文字)"
                            )
                        else:
                            preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                            st.markdown(f"**[{i+1}] {msg_type}** | {preview}")

        except Exception as e:
            research_status.error("❌ エラー")
            writing_status.empty()
            validate_status.empty()
            st.error(f"エラーが発生しました: {str(e)}")
            st.info("API キーが正しく設定されているか確認してください。")
