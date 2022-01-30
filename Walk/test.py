import pandas as pd
import numpy as np
import xlsxwriter
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font, NamedStyle
import sys


args = sys.argv[1]
print(args)
data = pd.read_excel (r''+args)
print(len(data.Time))
