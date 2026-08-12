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

            st.success("解析が完了しました。")
            
            st.write("---")
            st.markdown("### ■ AI感情・心理負荷解析結果")
            st.write(f"・主要感情判定: **{label}**")
            st.write(f"・AI確信度スコア: **{score:.4f} / 1.0000**")
            st.error(f"・システム判定: 【 {harassment_level} 】")
            st.write("※この結果はスクリーンショット等で証拠として保存してください。")
    else:
        st.warning("具体的な被害状況を入力してください。")
