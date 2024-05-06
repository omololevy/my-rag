import streamlit as st
from pdf_analyzer import extract_text_from_pdf
from transformers import pipeline

# Load the question answering model
nlp = pipeline("question-answering")

def main():
    st.title("PDF Analyzer")
    st.write("Upload a PDF file or drag and drop it here:")
    uploaded_file = st.file_uploader("", type=["pdf"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        text = extract_text_from_pdf(uploaded_file)
        st.write(text)

        question = st.text_input("Enter your question:")
        if st.button("Answer"):
            if question:
                # Perform question answering on the extracted text
                answer = nlp(question=question, context=text)
                st.write("Answer:", answer["answer"])
            else:
                st.write("Please enter a question.")

if __name__ == "__main__":
    main()
