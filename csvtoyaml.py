#!/usr/bin/python
import csv
import os
def from_csv_to_yaml(file):
    with open(file, 'r') as csvfile:
        freader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        # Creates the output file named fixture.yaml
        f = open('fixture.yaml', 'w')
        for i, row in enumerate(freader):
            csv_content = ' '.join(row)
            csv_content = csv_content.split(',')
            f.write('- model: app.Bus\n')
            f.write('  pk: %d\n' % i)
            f.write('  fields:\n')
            f.write('    nama_po: %s\n' % csv_content[1])
            f.write('    plat_no: %s\n' % csv_content[2])
            f.write('    jenis_trayek: %s\n' % csv_content[3])
            f.write('    jumlah_kursi: %s\n' % csv_content[4])
        f.close()

from_csv_to_yaml('Data Bus PMLD - Sheet1.csv')