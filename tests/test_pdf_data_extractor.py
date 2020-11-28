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

        line = 'Breached Entity: State Published Date Breach  Category'
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, 'Breached Entity:')

        line = 'No unwanted keyword in this text'
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, None)

        line = ''
        res = src.check_unwanted_keywords_in_the_line(line)
        self.assertEqual(res, None)

    def test_get_data_lines_from_text(self):
        text = 'Identity Theft\n' \
            '2018 Breach List:\n' \
            'Records Exposed:\n' \
            'Breached Entity:\n'  \
            'California Department of Insurance\n'  \
            '("CDI")\n' \
            'Source: www.databreaches.net\n' \
            'URL:  # https://www.databreaches.net\n' \
            'Breached Entity:\n'
        eq = [['California Department of Insurance',
               '("CDI")',
               'Source: www.databreaches.net',
               'URL:  # https://www.databreaches.net']]
        res = src.get_data_lines_from_text(text)
        self.assertEqual(res[0][0], eq[0][0])
        self.assertEqual(res[0][1], eq[0][1])
        self.assertEqual(res[0][2], eq[0][2])
        self.assertEqual(res[0][3], eq[0][3])


if __name__ == '__main__':
    unittest.main()
