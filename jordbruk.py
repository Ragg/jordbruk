# coding: utf-8
import csv
from fractions import Fraction
import pypyodbc
from pyparsing import Word, alphas, Regex, ZeroOrMore, Group
import logging


def split(s):
    if s is None or "!" in s:
        return []
    match = ZeroOrMore(Group(Word(alphas+"æøåÆØÅ") + Regex(r"[0-9/ ]*\d")))
    result = match.parseString(s.replace("%", ""))
    return result.asList()


def parse(fraction_string):
    s = fraction_string.strip()
    if not s:
        return 0
    spl = s.split()
    assert(len(spl) == 1 or len(spl) == 2)
    try:
        return float(sum(map(Fraction, spl)))
    except (ValueError, ZeroDivisionError):
        logging.info(repr(s))
        return 0


def main():
    logging.basicConfig(filename="jordbruk.log", level=logging.INFO)
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
    slash = []
    for i, row in enumerate(cursor):
        print("\r{}".format(i), end="")
        crops = {}
        animals = {}
        for crop in split(row[0]):
            try:
                crops[crops_map[crop[0]]] = parse(crop[1])
            except KeyError as e:
                logging.info(e)
        for animal in split(row[1]):
            try:
                animals[animals_map[animal[0]]] = parse(animal[1])
            except KeyError as e:
                logging.info(e)
        crops.update(animals)
        crops["JID"] = row[2]
        rows.append(crops)

    fieldnames = list(crops_map.values()) + list(animals_map.values())
    fieldnames.append('JID')
    csv.register_dialect('jordbruk', delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    with open("jordbruk.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames, 0.0, dialect='jordbruk')
        writer.writeheader()
        writer.writerows(rows)
    with open("slash.txt", "w") as slashfile:
        for line in slash:
            slashfile.write(str(line))
            slashfile.write("\n")

if __name__ == "__main__":
    main()
