import streamlit as st
import requests
import json

st.title("FinWise PDF Parser Frontend")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    with st.spinner("Uploading PDF..."):
        response = requests.post("http://127.0.0.1:8000/api/upload", files=files)

    if response.status_code == 200:
        data = response.json()
        st.success("PDF parsed successfully!")

        # Display metadata
        st.subheader("Metadata")
        st.json(data["parsed"]["meta"])

        # Display text per page
        st.subheader("Page Texts")
        for i, page in enumerate(data["parsed"]["page_texts"], start=1):
            st.markdown(f"**Page {i}:**")
            st.text(page)

        # Display tables (if any)
        st.subheader("Tables")
        if data["parsed"]["tables"]:
            st.json(data["parsed"]["tables"])
        else:
            st.write("No tables found.")

        # Real LLM Output
        st.subheader("LLM Output")

        with st.spinner("Extracting financial insights using LLM..."):
            llm_response = requests.post(
                "http://127.0.0.1:8000/api/extract",
                json={"text": "\n".join(data["parsed"]["page_texts"])}
            )

        if llm_response.status_code == 200:
            llm_data = llm_response.json()
            st.success("LLM extraction complete!")
            st.json(llm_data)
        else:
            st.error(f"LLM Error: {llm_response.status_code} - {llm_response.text}")

    else:
        st.error(f"Error: {response.status_code} - {response.text}")
