# XivDbReader

This is a python module that goes and extracts data from Final Fantasy XIV official database.  The goal is to extract the data and store it in a DB to be reused.

## Requirements

Python 3
requests
BeautifulSoup

## Getting Started



## How to use

``` python
from XivDbReader import Reader
from XivDbReader.collections import *
from typing import List

read = Reader()

# Returns items extracted from the list pages
itemLinks: List = read.getItems(itemType="arms")
```
