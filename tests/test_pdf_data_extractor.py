import unittest
import script.pdf_data_extractor as src


class TestPdfDataExtractor(unittest.TestCase):
    """Validation of functions in pdf_data_extractor.py script.
    """

    def test_check_unwanted_keywords_in_the_line(self):
        line = 'Identity Theft Resource Center'
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, 'Identity Theft')

        line = '2018 Breach List: 1,244'
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, 'Breach List:')

        line = 'Records Exposed: 446,515,334'
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, 'Records Exposed:')

        line = 'Breached Entity: State Published Date Breach Category'
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, 'Breached Entity:')


if __name__ == '__main__':
    unittest.main()
