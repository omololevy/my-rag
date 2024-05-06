import unittest
from rag import AnalyseIt
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.analyse_it = AnalyseIt()

    def test_ingest_integration(self):
        # Test integration between AnalyseIt and PyPDFLoader
        pdf_loader = PyPDFLoader(file_path="Nairobi.pdf")
        self.analyse_it.ingest(pdf_loader)
        self.assertIsNotNone(self.analyse_it.chain)

    def test_ask_integration(self):
        # Test integration between AnalyseIt and RecursiveCharacterTextSplitter
        pdf_loader = PyPDFLoader(file_path="Nairobi.pdf")
        self.analyse_it.ingest(pdf_loader)
        query = "What is the capital of Kenya?"
        response = self.analyse_it.ask(query)
        self.assertIsNotNone(response)

    def test_clear_integration(self):
        # Test integration between AnalyseIt and Chroma
        pdf_loader = PyPDFLoader(file_path="Nairobi.pdf")
        self.analyse_it.ingest(pdf_loader)
        self.analyse_it.clear()
        self.assertIsNone(self.analyse_it.chain)

if __name__ == '__main__':
    unittest.main()
