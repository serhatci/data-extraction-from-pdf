# Data extraction from a pdf file

A script to extract text data from a pdf file, converts it to pandas data frame and saves it in to a csv file.

[![CodeFactor](https://www.codefactor.io/repository/github/serhatci/data-extraction-from-pdf/badge)](https://www.codefactor.io/repository/github/serhatci/data-extraction-from-pdf)
<img src=https://img.shields.io/github/license/serhatci/data-extraction-from-pdf /></img>


## Installation

You can clone below repository:  
`git clone https://github.com/serhatci/data-extraction-from-pdf.git`

install the requirements:  
`pip install -r requirements.txt`

Be sure following pdf files are in the script folder:  
ITRCAnnualReportPdf2019.pdf  
ITRCAnnualReportPdf2018.pdf

and run the application:  
`python script/pdf_data_extractor.py`

## Requirements

Script works Python 3.7 or higher version.

Below libraries should be installed:

```
pip install pdfplumber
pip install pandas
```

## Visualization of extracted text from pdf file

Below image represents the format of pdf file and the extracted data in the CSV file.

![alt text](readme.jpg)
