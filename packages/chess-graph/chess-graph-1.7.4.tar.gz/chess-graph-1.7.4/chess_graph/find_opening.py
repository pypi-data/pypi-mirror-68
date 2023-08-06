import csv
import os

codes = []
names = []
positions = []

#example ids: ['e4', ('e4' , 'e5')]
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "elo_reading", "openings_sheet.csv")

def create_openings():
    with open(DATA_PATH, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            codes.append(row[0])
            names.append(row[1])
            positions.append(row[2])
        del codes[0], names[0], positions[0]

    positions_copy = []
    for position in positions:
        if len(position.split()) > 1:
            position = position.split()
            positions_copy.append(tuple(position))
        else:
            positions_copy.append(position)
    return codes, names, positions_copy

#print(positions_copy)
