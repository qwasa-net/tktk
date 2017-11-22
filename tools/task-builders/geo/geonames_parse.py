
import csv
import re
import json
import random

cre = re.compile(
    r'^([A-Z]{2})\t([A-Z]+)\t([0-9A-Z]*)\t([0-9A-Z]*)\t([^\t]+)\t([^\t]+)\t([0-9]+).*\t([0-9]+)\t([^\t]*)[\r\n]?', re.I | re.U)
are = re.compile(r'^([0-9]+)\t([0-9]+)\t([a-zA-Z]{2})\t([^\t]+)', re.I | re.U)
russo_re = re.compile(r'[йцукенгшщзхъэждлорпавыфячсмитьбю]')


def parse_files():

    # список городов
    ct_csv = list(csv.reader(open('cities15000.txt'), delimiter='\t'))

    cts = {}
    for l in ct_csv:
        k = int(l[0])
        # geo-id name country-code population
        cts[k] = [k, l[1], l[8], int(l[14])]

    # список стран
    cnts = {}
    for line in open('countryInfo.txt'):
        mo = cre.search(line)
        if mo:
            k = int(mo.group(8))
            # code name capital population
            cnts[k] = [mo.group(1), mo.group(5), mo.group(6), int(mo.group(7))]

    # переводы
    for line in open('alternateNames.txt'):

        mo = are.search(line)

        if not mo:
            continue

        # RU
        if mo.group(3) == 'ru' and russo_re.search(mo.group(4)):

            k = int(mo.group(2))

            if k in cts and len(cts[k]) < 5:
                cts[k].append(mo.group(4))

            elif k in cnts and len(cnts[k]) < 5:
                cnts[k].append(mo.group(4))

    countries = {}
    for k in cnts:
        # фильтр по наличию переводов у страны
        if len(cnts[k]) > 4:
            countries[cnts[k][0]] = cnts[k]

    # сортировка по числу жителей, фильтр по наличию перевода
    cities = sorted(filter(lambda x: len(x) > 4, cts.values()), key=lambda x: -x[3])

    # к городам добавляются страны
    # geo-id name c-code population c-code c-name capital population
    for s in cities:
        if s[2] in countries:
            s.extend(countries[s[2]])

    print("cities=", len(cities))
    print("countries=", len(countries))

    return cities, countries


def save_files(ct, cr):
    open('cities.json', 'w').write(json.dumps(ct, indent=2))
    open('countries.json', 'w').write(json.dumps(ct, indent=2))


if __name__ == '__main__':

    # http://download.geonames.org/export/dump/
    # cities15000.txt
    # countryInfo.txt
    # alternateNames.txt

    cities, countries = parse_files()
    save_files(cities, countries)
