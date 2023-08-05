# exex [![Build Status](https://travis-ci.org/vikpe/exex.svg?branch=master)](https://travis-ci.org/vikpe/exex) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
> Extract data from Excel documents

## Installation
```sh
pip install exex
```

## Usage

![Sample Excel file](https://raw.githubusercontent.com/vikpe/exex/master/docs/sample_xlsx.png "Sample Excel file")

**Load Excel file**
```python
from openpyxl import load_workbook
from exex import parse

book = load_workbook("sample.xlsx") # load excel file
sheet = book.active # get active sheet
```

**Single cell by name**
```python
parse.values(sheet["A1"])
"name"
```

**Single cell by row/column number**
```python
parse.values(sheet.cell(row=1, column=1)) 
"name"
```
   
**Range of cells**
```python
parse.values(sheet["A1":"B2"])
[
  ["name", "abbreviation"],
  ["alpha", "a"],
]
```

**All cells**
```python              
parse.values(sheet.values)
[
  ["name", "abbreviation", "age"],
  ["alpha", "a", 1],
  ["beta", "b", 2],
  ["gamma", "g", 3],
]
```

**Row by number**
```python                  
parse.values(sheet[1])
["alpha", "a", 1]
```

**Range of rows**
```python           
parse.values(sheet[1:2])
[
  ["name", "abbreviation", "age"],
  ["alpha", "a", 1],
]
```

**Column by name**
```python            
parse.values(sheet["A"])
["name", "alpha", "beta", "gamma"]
```

**Rangge of columns**
```python
parse.values(sheet["A:B"])
[
  ["name", "alpha", "beta", "gamma"],
  ["abbreviation", "a", "b", "g"],
]
```

**Ways to access sheets**
```python
# Sheets
book.sheets[0]                # (sheet) sheet by index
book.sheets["prices"]         # (sheet) sheet by name
book.active                   # (sheet) active sheet

book.sheetnames               # (array) sheet names
```

## Development

**Tests** (local Python version)
```sh
poetry run pytest
```

**Tests** (all Python versions defined in `tox.ini`)
```sh
poetry run tox
```

**Code formatting** (black)
```sh
poetry run black .
```
