import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
import tempfile
from utils import run_pipeline

st.set_page_config(
    page_title="Smart Meeting Analyzer",
    layout="wide",
    page_icon="📝",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.reportview-container .main .block-container{
    padding-top: 2rem;
}
.card {
    background: #161b22;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #30363d;
}
h1, h2, h3, h4, p, label, textarea {
    color: #e6edf3 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>📝 Smart Meeting Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>AI-powered Meeting Summary & Action Items Extractor</h3>", unsafe_allow_html=True)
st.write("----")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📥 Enter Meeting Transcript")
    user_text = st.text_area("Paste transcript here:", height=300)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📄 Upload .txt File")
    uploaded = st.file_uploader("Upload your file", type=["txt"])
    if uploaded:
        user_text = uploaded.read().decode("utf-8")
        st.success("File uploaded successfully!")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("----")

if st.button("🚀 Analyze Meeting", use_container_width=True):
    if not user_text.strip():
        st.error("Please paste or upload a meeting transcript.")
    else:
        with st.spinner("Analyzing meeting…"):
            summary, actions = run_pipeline(user_text)

        st.success("Analysis complete!")

        st.markdown("<h2>📌 Structured Summary</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><p>{summary.replace('\n', '<br>')}</p></div>", unsafe_allow_html=True)

        st.markdown("<h2>📝 Extracted Action Items</h2>", unsafe_allow_html=True)
        if actions:
            df = pd.DataFrame(actions)
            st.table(df)
        else:
            st.info("No action items detected.")

        st.session_state["summary"] = summary
        st.session_state["actions"] = actions

        st.write("----")

if "summary" in st.session_state:
    st.markdown("<h2>📄 Export Report</h2>", unsafe_allow_html=True)

    if st.button("Download PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 15, "Meeting Report", ln=True)

        pdf.set_font("Arial", "B", 16)
        pdf.ln(5)
        pdf.cell(0, 10, "Summary:", ln=True)

        pdf.set_font("Arial", "", 12)
        for line in st.session_state["summary"].split("\n"):
            pdf.multi_cell(0, 8, line)

        pdf.set_font("Arial", "B", 16)
        pdf.ln(5)
        pdf.cell(0, 10, "Action Items:", ln=True)

        pdf.set_font("Arial", "", 12)
        for a in st.session_state["actions"]:
            pdf.multi_cell(0, 8, f"- {a['assignee']} | {a['deadline']} | {a['task']}")

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(tmp.name)

        with open(tmp.name, "rb") as f:
            st.download_button(
                label="📄 Download Meeting Report (PDF)",
                data=f,
                file_name="meeting_report.pdf",
                mime="application/pdf"
            )
