import re
import pdfplumber  # reads pdf files
import pandas as pd


def check_unwanted_keywords_in_the_line(line):
    """Checks if the keywords exist in the given text.

    Args:
        line (str): given text line

    Returns:
        (str): matching keyword
    """
    unwanted_keywords = ['Identity Theft',
                         'Breach List:',
                         'Records Exposed:',
                         'Breached Entity:']
    for keyword in unwanted_keywords:
        if re.search(keyword, line):
            return re.search(keyword, line).group()


def get_data_lines_from_text(text):
    """Extract and groups lines from text which are only 
    related for data extraction.

    Args:
        text (str): text collected from single page of pfd file.

    Returns:
        data_lines (list): group of lines including only relevant data 
        for extraction
    """
    data_lines = []
    group = []
    for line in text.split('\n'):
        result = check_unwanted_keywords_in_the_line(line)
        if result is None:
            group.append(line)
        elif result == 'Breached Entity:' and group != []:
            data_lines.append(group)
            group = []
    return data_lines


def extract_data(data_list):
    """Extract necessary data from lines in the data list.

    Args:
        data_list (list): data lines for data extraction.

    Returns:
        data (list): final data for appending in to a dataframe.
    """
    data = []
    for block in data_list:
        state = get_state(block[0])
        date = get_date(block[0])
        b_type = get_type(block[0])
        category = get_category(block[0])
        records = get_records(block[0])

        extracted_text = (' ').join([state, date, b_type, category, records])
        entity = get_entity(block, extracted_text)

        source = get_source(block[-2])
        url = get_url(block[-1])

        data.append([entity, state, date, b_type,
                     category, records, source, url])
    return data


def check_data(func):
    """Decorator function for checking possible exceptions during extraction.

    Args:
        func (obj): function used in try-except block

    Except:
        (str) : in case of exception assigns '-' for the missing data.
    """
    def inner(line):
        try:
            return func(line)
        except:
            return '-'
    return inner


@check_data
def get_records(line1):
    """Collects record reported from the line.

    Args:
        line1 (str): 1.st line of data block

    Returns:
        str: record reported
    """
    record = line1.split(' ')[-1]
    return record if record != '' else '-'


@check_data
def get_category(line1):
    """Collects breach category from the line.

    Args:
        line1 (str): 1.st line of data block

    Returns:
        str: breach category
    """
    line1 = line1.split(' ')
    return line1[-2]


@check_data
def get_type(line1):
    """Collects breach type from the line.

    Args:
        line1 (str): 1.st line of data block

    Returns:
        str: breach type
    """
    if re.search('Paper Data', line1) is not None:
        return 'Paper Data'
    elif re.search('Electronic', line1) is not None:
        return 'Electronic'
    else:
        return '-'


@check_data
def get_date(line1):
    """Collects published date from the line.

    Args:
        line1 (str): 1.st line of data block

    Returns:
        str: published date
    """
    return re.search(r'(\d{2}|\d{1})/(\d{2}|\d{1})/\d{4}', line1).group().strip()


@check_data
def get_state(line1):
    """Collects state from the line.

    Args:
        line1 (str): 1.st line of data block

    Returns:
        str: state
    """
    return re.search(r'\b[A-Z][A-Z]\b', line1).group().strip()


@check_data
def get_source(line2):
    """Collects source from the line.

    Args:
        line2 (str): 2.st line of data block

    Returns:
        str: source
    """
    src = line2.split(' ')[1]
    return src if src != '' else '-'


@check_data
def get_url(line3):
    """Collects URL from the line.

    Args:
        line3 (str): 3.st line of data block

    Returns:
        str: URL
    """
    link = line3.split(' ')[1]
    return link if link != '' else '-'


def get_entity(block, extracted_text):
    """Collect entity from the line1 of data block

    Args:
        block (list): block including lines of data for extraction 
        extracted_text (str): text which is already extracted from first line

    Returns:
        (str): entity
    """
    try:
        entity = re.sub(extracted_text, '', block[0])
        if len(block) > 3:
            for i in range(1, len(block)-2):
                entity += block[i]
    except:
        return '-'
    else:
        ent = entity.replace('  ', ' ').replace('"', '').strip()
        return ent if ent != '' else '-'


def file_list():
    """Provides files to be extracted.

    Files should be in the same folder with script file.

    Returns:
        (list): file names
    """
    return ['script/ITRCAnnualReportPdf2019.pdf',
            'script/ITRCAnnualReportPdf2018.pdf']


def create_dataframe():
    """Provied the dataframe with appropriate column names.

    Returns:
        (obj): pandas dataframe
    """
    return pd.DataFrame(columns=['BreachedEntity',
                                 'State',
                                 'PublishedDate',
                                 'BreachType',
                                 'BreachCategory',
                                 'RecorsReported',
                                 'Source',
                                 'URL'])


if __name__ == "__main__":

    df = create_dataframe()

    for file in file_list():
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
            for page in pages:
                text = page.extract_text()
                data_lines = get_data_lines_from_text(text)
                data = extract_data(data_lines)
                df = df.append(pd.DataFrame(data, columns=df.columns))
                print(f'EXTRACTED: page {page.page_number} of {file}')

        df.to_csv(f'{file[:-4]}.csv', index=False, sep=';')
        print('Data successfully extracted and saved to csv file!...')
        df.iloc[0:0]
