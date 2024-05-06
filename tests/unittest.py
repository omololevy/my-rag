import unittest
from ..rag import AnalyseIt

class TestAnalyseIt(unittest.TestCase):
    def setUp(self):
        self.analyse_it = AnalyseIt()

    def test_ingest(self):
        # Test the ingest method
        pdf_file_path = "Nairobi.pdf"
        self.analyse_it.ingest(pdf_file_path)

    def test_ask(self):
        # Test the ask method
        query = "What is the capital of Kenya?"
        response = self.analyse_it.ask(query)

    def test_clear(self):
        # Test the clear method
        self.analyse_it.clear()

if __name__ == '__main__':
    unittest.main()
