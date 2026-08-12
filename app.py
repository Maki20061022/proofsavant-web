import streamlit as st
from transformers import pipeline
import datetime

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="koheiduck/bert-japanese-finetuned-sentiment")

st.title("ProofSavant")
st.subheader("公式・被害事案記録システム")
st.write("被害の状況をAIが解析し、客観的なデータとして記録します。")

date = st.text_input("1. それは「いつ」起きましたか？")
location = st.text_input("2. 「どこで」起きましたか？")
aggressor = st.text_input("3. 「誰から」被害を受けましたか？")
witnesses = st.text_input("4. 目撃者や証拠はありますか？")
incident_desc = st.text_area("5. 被害の具体的な状況や、辛い気持ちを教えてください。")

if st.button("AIで解析して報告書を作成"):
    if incident_desc:
        with st.spinner("AIが心理状態を解析中..."):
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

            current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

            st.success("解析が完了しました。")
            
            st.write("---")
            st.markdown("### ■ AI感情・心理負荷解析結果")
            st.write(f"・主要感情判定: **{label}**")
            st.write(f"・AI確信度スコア: **{score:.4f} / 1.0000**")
            st.error(f"・システム判定: 【 {harassment_level} 】")

            # 美しいデザインのHTMLレポートを動的生成
            html_content = f"""
            <!DOCTYPE html>
            <html lang="ja">
            <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; padding: 30px; max-width: 800px; margin: 0 auto; background-color: #fdfdfd; }}
                h1 {{ background-color: #2c3e50; color: white; padding: 20px; text-align: center; font-size: 22pt; margin-bottom: 5px; border-bottom: 5px solid #e74c3c; }}
                h2 {{ color: #2c3e50; border-left: 5px solid #3498db; padding-left: 10px; margin-top: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; background-color: white; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f9fbfc; width: 30%; color: #555; }}
                .alert {{ border: 2px solid #e74c3c; background-color: #fff3f3; padding: 20px; border-radius: 5px; margin-top: 30px; }}
                .alert-title {{ color: #c0392b; font-weight: bold; font-size: 15pt; border-bottom: 1px solid #fadbd8; padding-bottom: 10px; margin-bottom: 15px; margin-top: 0; }}
            </style>
            </head>
            <body>
                <h1>ProofSavant</h1>
                <div style="text-align: center; font-size: 12pt; color: #555; margin-bottom: 20px;">公式・被害事案報告書</div>
                <p style="text-align: right; color: #666; font-size: 10pt;">[記録日時] {current_time}</p>
                <h2>■ 事案の基本情報 (5W1H)</h2>
                <table>
                    <tr><th>発生時期</th><td>{date}</td></tr>
                    <tr><th>発生場所</th><td>{location}</td></tr>
                    <tr><th>加害者(推定)</th><td>{aggressor}</td></tr>
                    <tr><th>目撃者・証拠の有無</th><td>{witnesses}</td></tr>
                </table>
                <h2>■ 被害の具体的内容・心理状態</h2>
                <p style="background-color: #f9fbfc; padding: 15px; border-left: 4px solid #95a5a6; white-space: pre-wrap;">{incident_desc}</p>
                <div class="alert">
                    <h3 class="alert-title">■ AI感情・心理負荷解析結果</h3>
                    <p style="margin: 5px 0;">・主要感情判定: <strong>{label}</strong></p>
                    <p style="margin: 5px 0;">・AI確信度スコア: <strong>{score:.4f} / 1.0000</strong></p>
                    <p style="color: #c0392b; font-weight: bold; font-size: 13pt; margin-top: 15px;">・システム判定: 【 {harassment_level} 】</p>
                </div>
            </body>
            </html>
            """

            # 【追加】画面上にダウンロードボタンを表示する
            st.download_button(
                label="📥 公式報告書（印刷用ファイル）をダウンロード",
                data=html_content,
                file_name="ProofSavant_Report.html",
                mime="text/html"
            )
    else:
        st.warning("具体的な被害状況を入力してください。")
