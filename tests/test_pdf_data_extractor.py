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

    def test_extract_data(self):
        data_list = [['California CA 12/13/2018 Electronic Government/Military Unknown',
                      '("CDI")',
                      'Source: www.databreaches.net',
                      'URL: #https://www.databreaches.net']]
        eq = [['California (CDI)', 'CA', '12/13/2018', 'Electronic',
               'Government/Military', 'Unknown',
               'www.databreaches.net', '#https://www.databreaches.net']]
        res = src.extract_data(data_list)
        self.assertEqual(res, eq)

    def test_get_records(self):
        line = 'California CA 12/13/2018 Electronic Government/Military Unknown'
        self.assertEqual(src.get_records(line), 'Unknown')
        self.assertEqual(src.get_records(''), '-')

    def test_get_category(self):
        line = 'California CA 12/13/2018 Electronic Government/Military Unknown'
        self.assertEqual(src.get_category(line), 'Government/Military')
        self.assertEqual(src.get_category(''), '-')

    def test_get_type(self):
        line = 'California CA 12/13/2018 Electronic Government/Military Unknown'
        self.assertEqual(src.get_type(line), 'Electronic')
        self.assertEqual(src.get_type(
            'a a a Paper Data a a'), 'Paper Data')
        self.assertEqual(src.get_type('a a a irrelevant a a'), '-')
        self.assertEqual(src.get_type(''), '-')

    def test_get_date(self):
        line = 'California CA 12/13/2018 Electronic Government/Military Unknown'
        self.assertEqual(src.get_date(line), '12/13/2018')
        self.assertEqual(src.get_date('a a a 12/13/201 a a'), '-')
        self.assertEqual(src.get_date('a a a 2/13/2018 a a'), '2/13/2018')
        self.assertEqual(src.get_date('a a a 12/3/2018 a a'), '12/3/2018')
        self.assertEqual(src.get_date(''), '-')

    def test_get_state(self):
        line = 'California CA 12/13/2018 Electronic Government/Military Unknown'
        self.assertEqual(src.get_state(line), 'CA')
        self.assertEqual(src.get_state('a a a CAA a a'), '-')
        self.assertEqual(src.get_state('a a C CA CC CC'), 'CA')
        self.assertEqual(src.get_state('a a AAA AAA CA'), 'CA')
        self.assertEqual(src.get_state('AAaaa a CA a a a'), 'CA')
        self.assertEqual(src.get_state(''), '-')

    def test_get_source(self):
        line = 'Source: www.databreaches.net'
        self.assertEqual(src.get_source(line), 'www.databreaches.net')
        self.assertEqual(src.get_source('Source:  '), '-')
        self.assertEqual(src.get_source('Source:'), '-')
        self.assertEqual(src.get_source(''), '-')

    def test_get_url(self):
        line = 'URL: #https://www.databreaches.net'
        self.assertEqual(src.get_url(line), '#https://www.databreaches.net')
        self.assertEqual(src.get_url('URL:  '), '-')
        self.assertEqual(src.get_url('URL:'), '-')
        self.assertEqual(src.get_source(''), '-')

    def test_get_entity(self):
        block = ['California asd asd']
        extracted_text = 'asd asd'
        self.assertEqual(src.get_entity(block, extracted_text), 'California')

        block = ['California asd asd', '("C")', '', '']
        self.assertEqual(src.get_entity(
            block, extracted_text), 'California (C)')

        block = ['', '(C)', '', '']
        self.assertEqual(src.get_entity(
            block, extracted_text), '(C)')

        block = ['', '', '', '']
        self.assertEqual(src.get_entity(
            block, extracted_text), '-')

    def test_file_list(self):
        files = ['aaa.pdf', 'bbb.pdf']
        self.assertTrue(files)
        for file in files:
            self.assertRegexpMatches(file, '.pdf')

    def test_create_dataframe(self):
        col = ['BreachedEntity',
               'State',
               'PublishedDate',
               'BreachType',
               'BreachCategory',
               'RecorsReported',
               'Source',
               'URL']
        df = src.create_dataframe()
        for i, column in enumerate(df.columns):
            self.assertEqual(column, col[i])


if __name__ == '__main__':
    unittest.main()
