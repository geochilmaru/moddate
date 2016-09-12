import csv
import os


def write_csv(filename, rows, delimiter, order_by):
    with open(filename, 'wb') as csvfile:
        if order_by != "":
            fieldnames = order_by
        else:
            fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        for row in rows:
            try:
                writer.writerow(row)
            except Exception as detail:
                print type(detail)
                print detail


def read_csv(filename, delimiter):
    reader = []
    csvfile = ""
    if not os.path.isfile(filename):
        csvfile = open(filename, "wb")
    else:
        csvfile = open(filename, "rb")
        reader = csv.DictReader(csvfile, delimiter=delimiter)
    return list(reader)
