import numpy as np
import csv
import pandas as pd


dict_from_csv = {}
with open("material_energy.csv", 'r') as file:
   MatEE = csv.reader(file)
   MatEE = {rows[0]:rows[1] for rows in MatEE}





