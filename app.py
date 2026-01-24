import streamlit as st
import tempfile
from core import parse_resume

st.set_page_config(page_title="SIGMA-CV", layout="centered")
st.title("Σ SIGMA-CV Resume Parser")

uploaded = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded.name) as tmp:
        tmp.write(uploaded.read())
        path = tmp.name

    if st.button("Parse Resume"):
        result = parse_resume(path)
        st.subheader("👤 Personal Information")
        st.write(f"**Name:** {result['personal_info'].get('name', 'N/A')}")
        st.write(f"**Email:** {result['personal_info'].get('email', 'N/A')}")
        st.write(f"**Phone:** {result['personal_info'].get('phone', 'N/A')}")

        st.subheader("🎓 Education")
        if result["education"]:
            for edu in result["education"]:
                st.write(f"- {edu}")
        else:
            st.write("Not detected")

        st.subheader("💼 Experience")
        if result["experience"]:
            for exp in result["experience"]:
                st.write(f"- {exp}")
        else:
            st.write("Not detected")

        st.subheader("🛠 Skills")
        if result["skills"]:
            st.write(", ".join(result["skills"]))
        else:
            st.write("Not detected")

