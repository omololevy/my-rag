from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.vectorstores.utils import filter_complex_metadata
import logging


class ChatPDF:
    vector_store = None
    retriever = None
    chain = None
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.model = ChatOllama(model="mistral")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that I don't know. Use three sentences
             maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

    def ingest(self, pdf_file_path: str):
        try:
            docs = PyPDFLoader(file_path=pdf_file_path).load()
            chunks = self.text_splitter.split_documents(docs)
            chunks = filter_complex_metadata(chunks)

            vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
            self.retriever = vector_store.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    "k": 3,
                    "score_threshold": 0.5,
                },
            )

            self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                          | self.prompt
                          | self.model
                          | StrOutputParser())
            self.logger.info(f"PDF ingested successfully from {pdf_file_path}")
        except Exception as e:
            self.logger.error(f"Error ingesting PDF: {e}")
            raise  # Re-raise the exception for handling in the app.py

    def ask(self, query: str):
        if not self.chain:
            return "Please, upload a PDF document first."

        try:
            return self.chain.invoke(query)
        except Exception as e:
            self.logger.error(f"Error processing question: {e}")
            return "An error occurred while processing your question. Please try again later."


    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
