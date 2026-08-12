import streamlit as st
from transformers import pipeline
import datetime

# ページの設定
st.set_page_config(
    page_title="ProofSavant - 公式事案記録システム",
    page_icon="⚖️",
    layout="centered"
)

# スタイリッシュなカスタムCSS
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { font-family: 'Helvetica Neue', Arial, sans-serif; font-weight: 700; color: #f0f2f6; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }
    .stButton>button { width: 100%; background: linear-gradient(135deg, #2980b9, #2c3e50); color: white; font-weight: bold; border-radius: 8px; padding: 12px; border: none; }
    .stDownloadButton>button { width: 100%; background: linear-gradient(135deg, #27ae60, #1e8449); color: white; font-weight: bold; border-radius: 8px; padding: 12px; border: none; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="koheiduck/bert-japanese-finetuned-sentiment")

st.title("⚖️ ProofSavant")
st.subheader("公式・被害事案記録システム")
st.markdown("<p style='color: #8b949e; font-size: 11pt;'>被害の状況を高精度AIが解析し、客観的な法的証拠データとして記録・出力します。</p>", unsafe_allow_html=True)

date = st.text_input("1. それは「いつ」起きましたか？")
location = st.text_input("2. 「どこで」起きましたか？")
aggressor = st.text_input("3. 「誰から」被害を受けましたか？")
witnesses = st.text_input("4. 目撃者や証拠はありますか？")
incident_desc = st.text_area("5. 被害の具体的な状況や、辛い気持ちを教えてください。")

if st.button("AIで解析して報告書を作成"):
    if incident_desc:
        with st.spinner("AIが解析中..."):
            nlp = load_model()
            result = nlp(incident_desc)[0]
            label = result['label']
            score = result['score']

            harassment_level = "低"
            if label == "NEGATIVE":
                if score > 0.90:
                    harassment_level = "高（法的対応・即時介入を強く推奨）"
                elif score > 0.70:
                    harassment_level = "中（経過観察および証拠保全を推奨）"

            # 日本時間に修正
            JST = datetime.timezone(datetime.timedelta(hours=9))
            current_time = datetime.datetime.now(JST).strftime("%Y年%m月%d日 %H:%M:%S")

            st.success("解析が完了しました。")
            st.write("---")
            st.markdown("### ■ AI感情・心理負荷解析結果")
            st.write(f"・主要感情判定: **{label}**")
            st.write(f"・AI確信度スコア: **{score:.4f} / 1.0000**")
            st.error(f"・システム判定: 【 {harassment_level} 】")

            html_content = f"""
            <!DOCTYPE html>
            <html lang="ja">
            <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; padding: 30px; max-width: 800px; margin: 0 auto; }}
                h1 {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; border-bottom: 5px solid #e74c3c; }}
                h2 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 10px; margin-top: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f9fbfc; width: 30%; }}
                .alert {{ border: 2px solid #e74c3c; background-color: #fff3f3; padding: 20px; border-radius: 5px; }}
            </style>
            </head>
            <body>
                <h1>ProofSavant</h1>
                <div style="text-align: right; font-size: 10pt;">[記録日時] {current_time}</div>
                <h2>■ 事案の基本情報</h2>
                <table>
                    <tr><th>発生時期</th><td>{date}</td></tr>
                    <tr><th>発生場所</th><td>{location}</td></tr>
                    <tr><th>加害者</th><td>{aggressor}</td></tr>
                    <tr><th>証拠</th><td>{witnesses}</td></tr>
                </table>
                <h2>■ 被害状況</h2>
                <p>{incident_desc}</p>
                <div class="alert">
                    <h3>■ AI解析結果</h3>
                    <p>・判定: <strong>{label}</strong> ({harassment_level})</p>
                </div>
            </body>
            </html>
            """
            
            st.download_button(
                label="📥 公式報告書をダウンロード",
                data=html_content,
                file_name="ProofSavant_Report.html",
                mime="text/html"
            )
    else:
        st.warning("具体的な被害状況を入力してください。")
