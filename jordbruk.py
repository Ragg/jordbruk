import re
import csv
from fractions import Fraction
import pypyodbc


def split(s):
    if s is None:
        return
    s = s.strip()
    s = re.sub('[%]', '', s)
    num = False
    pair = ["", ""]
    for cur in s:
        if cur.isdigit() or cur == r"/":
            if num is False:
                num = True
            pair[1] += cur
        elif cur.isspace():
            if num is True:
                pair[1] += cur
        else:
            if num is True:
                num = False
                yield pair
                pair = ["", ""]
            pair[0] += cur
    yield pair


def parse(fraction_string):
    s = fraction_string.strip()
    if not s:
        return 0
    spl = s.split()
    assert(len(spl) == 1 or len(spl) == 2)
    try:
        return sum(map(Fraction, spl))
    except (ValueError, ZeroDivisionError):
        print(repr(s))
        return 0

def main():
    db = r"C:\Users\rhdgjest\Documents\jordbruk\jordbruk.accdb"
    dbstring = r"Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};Dbq={};".format(db)
    conn = pypyodbc.connect(dbstring)
    query = "SELECT UTSAED, KREATUR, JID FROM Jordbruk;"
    cursor = conn.cursor()
    cursor.execute(query)

    crops_map = {
        "po": "Poteter",
        "hv": "Hvete",
        "ru": "Rug",
        "ha": "Havre",
        "by": "Bygg",
        "bl": "Blandkorn",
        "er": "Erter",
    }

    animals_map = {
        "he": "Hester",
        "ku": "Kveg",
        "sv": "Svin",
        "få": "Faar",
        "gj": "Gjeter",
        "re": "Rensdyr",
    }

    rows = []
    i = 0
    slash = []
    for row in cursor:
        #i += 1
        #if i > 1000:
        #    break
        crops = {}
        animals = {}
        for crop in split(row[0]):
            try:
                crops[crops_map[crop[0]]] = parse(crop[1])
            except KeyError as e:
                print(e)
        for animal in split(row[1]):
            try:
                animals[animals_map[animal[0]]] = parse(animal[1])
            except KeyError as e:
                print(e)
        crops.update(animals)
        crops["JID"] = row[2]
        rows.append(crops)

    fieldnames = list(crops_map.values()) + list(animals_map.values())
    fieldnames.append('JID')
    csv.register_dialect('jordbruk', delimiter=';', quoting=csv.QUOTE_ALL)
    with open("jordbruk.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames, 0.0, dialect='jordbruk')
        writer.writeheader()
        writer.writerows(rows)
    with open("slash.txt", "w") as slashfile:
        for line in slash:
            slashfile.write(str(line))
            slashfile.write("\n")


main()
