import csv


dict_from_csv = {}
with open("subsys_weights.csv", 'r') as file:
   lst = csv.reader(file)
   lst = {rows[0]:rows[1] for rows in lst}
subsys_weights = lst