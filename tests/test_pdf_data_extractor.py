import unittest
import script.pdf_data_extractor as src


class TestPdfDataExtractor(unittest.TestCase):
    """Validation of functions in pdf_data_extractor.py script.
    """

    def test_check_unwanted_keywords_in_the_line(self):
        test_cases = [
            {'input': 'Identity Theft Resource Center',
             'expected': 'Identity Theft'},
            {'input': '2018 Breach List: 1,244',
             'expected': 'Breach List:'},
            {'input': 'Records Exposed: 446,515,334',
             'expected': 'Records Exposed:'},
            {'input': 'Breached Entity: State Published Date Breach  Category',
             'expected': 'Breached Entity:'},
            {'input': 'No unwanted keyword in this text',
                'expected': None},
            {'input': '',
             'expected': None},
        ]

        for case in test_cases:
            self.assertEqual(
                src.check_unwanted_keywords_in_the_line(case['input']),
                case['expected'])

    def test_get_data_lines_from_text(self):
        input = 'Identity Theft\n' \
            '2018 Breach List:\n' \
            'Records Exposed:\n' \
            'Breached Entity:\n'  \
            'California Department of Insurance\n'  \
            '("CDI")\n' \
            'Source: www.databreaches.net\n' \
            'URL:  # https://www.databreaches.net\n' \
            'Breached Entity:\n'
        expected = [['California Department of Insurance',
                     '("CDI")',
                     'Source: www.databreaches.net',
                     'URL:  # https://www.databreaches.net']]

        self.assertEqual(
            src.get_data_lines_from_text(input), expected)

    def test_extract_data(self):
        input = [['California CA 12/13/2018 Electronic Government/Military Unknown',
                  '("CDI")',
                  'Source: www.databreaches.net',
                  'URL: #https://www.databreaches.net']]
        expected = [['California (CDI)', 'CA', '12/13/2018', 'Electronic',
                     'Government/Military', 'Unknown',
                     'www.databreaches.net', '#https://www.databreaches.net']]
        self.assertEqual(src.extract_data(input), expected)

    def test_get_records(self):
        test_cases = [
            {'input': 'California CA 12/13/2018 Electronic Government/Military Unknown',
             'expected': 'Unknown'},
            {'input': '',
             'expected': '-'}
        ]
        for case in test_cases:
            self.assertEqual(src.get_records(case['input']), case['expected'])

    def test_get_category(self):
        test_cases = [
            {'input': 'California CA 12/13/2018 Electronic Government/Military Unknown',
             'expected': 'Government/Military'},
            {'input': '',
             'expected': '-'}
        ]
        for case in test_cases:
            self.assertEqual(
                src.get_category(case['input']), case['expected'])

    def test_get_type(self):
        test_cases = [
            {"input": 'California CA 12/13/2018 Electronic Government/Military Unknown',
             "expected": 'Electronic'},
            {"input": 'a a a Paper Data a a',
             "expected": 'Paper Data'},
            {"input": 'a a a irrelevant a a',
             "expected": '-'},
            {"input": '',
             "expected": '-'}
        ]
        for case in test_cases:
            self.assertEqual(src.get_type(case['input']), case['expected'])

    def test_get_date(self):
        test_cases = [
            {"input": 'California CA 12/13/2018 Electronic Government/Military Unknown',
             "expected": '12/13/2018'},
            {"input": 'a a a 12/13/201 a a',
             "expected": '-'},
            {"input": 'a a a 2/13/2018 a a',
             "expected": '2/13/2018'},
            {"input": 'a a a 12/3/2018 a a',
             "expected": '12/3/2018'},
            {"input": '',
             "expected": '-'},

        ]
        for case in test_cases:
            self.assertEqual(src.get_date(case['input']), case['expected'])

    def test_get_state(self):
        test_cases = [
            {"input": 'California CA 12/13/2018 Electronic Government/Military Unknown',
             "expected": 'CA'},
            {"input": 'a a a CAA a a',
             "expected": '-'},
            {"input": 'a a C CA CC CC',
             "expected": 'CA'},
            {"input": 'a a AAA AAA CA',
             "expected": 'CA'},
            {"input": 'AAaaa a CA a a a',
             "expected": 'CA'},
            {"input": '',
             "expected": '-'},
        ]
        for case in test_cases:
            self.assertEqual(src.get_state(case['input']), case['expected'])

    def test_get_source(self):
        test_cases = [
            {"input": 'Source: www.databreaches.net',
             "expected": 'www.databreaches.net'},
            {"input": 'Source:  ',
             "expected": '-'},
            {"input": 'Source:',
             "expected": '-'},
            {"input": '',
             "expected": '-'},
        ]
        for case in test_cases:
            self.assertEqual(src.get_source(case['input']), case['expected'])

    def test_get_url(self):
        test_cases = [
            {"input": 'URL: #https://www.databreaches.net',
             "expected": '#https://www.databreaches.net'},
            {"input": 'URL:  ',
             "expected": '-'},
            {"input": 'URL:',
             "expected": '-'},
            {"input": '',
             "expected": '-'}
        ]
        for case in test_cases:
            self.assertEqual(src.get_source(case['input']), case['expected'])

    def test_get_entity(self):
        test_cases = [
            {"input": (['California asd asd'], 'asd asd'),
             "expected": 'California'},
            {"input": (['California asd asd', '("C")', '', ''], 'asd asd'),
             "expected": 'California (C)'},
            {"input": (['', '(C)', '', ''],  'asd asd'),
             "expected": '(C)'},
            {"input": (['', '', '', ''], 'asd asd'),
             "expected": '-'},
        ]

        for case in test_cases:
            self.assertEqual(
                src.get_entity(case['input'][0], case['input'][1]), case['expected'])

    def test_file_list(self):
        input = ['aaa.pdf', 'bbb.pdf']
        expected = '.pdf'
        self.assertTrue(input)
        for file in input:
            self.assertRegexpMatches(file, expected)

    def test_create_dataframe(self):
        expected = ['BreachedEntity',
                    'State',
                    'PublishedDate',
                    'BreachType',
                    'BreachCategory',
                    'RecorsReported',
                    'Source',
                    'URL']
        df = src.create_dataframe()
        for i, column in enumerate(df.columns):
            self.assertEqual(column, expected[i])


if __name__ == '__main__':
    unittest.main()
