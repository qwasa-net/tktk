# -*- coding: utf-8 -*-

import csv
import re
import json
import random
import unidecode

TASK_SIZE = 9
cre = re.compile(
    r'^([A-Z]{2})\t([A-Z]+)\t([0-9A-Z]*)\t([0-9A-Z]*)\t([^\t]+)\t([^\t]+)\t([0-9]+).*\t([0-9]+)\t([^\t]*)[\r\n]?', re.I | re.U)
are = re.compile(r'^([0-9]+)\t([0-9]+)\t([a-zA-Z]{2})\t([^\t]+)', re.I | re.U)
russo_re = re.compile(r'[йцукенгшщзхъэждлорпавыфячсмитьбю]')


def parse_files():

    # http://download.geonames.org/export/dump/
    # cities15000.txt —
    # countryInfo.txt
    # alternateNames.txt

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


def load_files():
    cities = json.loads(open('cities.json').read())
    countries = json.loads(open('cities.json').read())
    return cities, countries

BAG = ['RU', 'FI', 'IN', 'ES', 'IT', 'DE', 'CZ', 'GB', 'US', 'CN', 'PK', 'PL', 'FR', 'PT', 'AR', 'BR', 'MX']
BAG_RUS2 = ['России', 'Финляндии', "Индии", "Испании", "Италии", "Германии", "Чехии", "Великобритании",
            "США", "Китая", "Пакистана", "Польши", "Франции", "Португалии", "Аргентины", "Бразилии", "Мексики"]

BAGS_RUS3 = {
    'RU': ['России', 'в России'],
    'FI': ['Финляндии', 'в Финляндии'],
    'IN': ['Индии', 'в Индии'],
    'ES': ['Испании', 'в Испании'],
    'IT': ['Италии', 'в Италии'],
    'DE': ['Германии', 'в Германии'],
    'CZ': ['Чехии', 'в Чехии'],
    'GB': ['Великобритании', 'в Великобритании'],
    'US': ['США', 'в США'],
    'CN': ['Китая', 'в Китае'],
    'PK': ['Пакистана', 'в Пакистане'],
    'PL': ['Польши', 'в Польше'],
    'FR': ['Франции', 'в Франции'],
    'PT': ['Португалии', 'в Португалии'],
    'AR': ['Аргентины', 'в Аргентине'],
    'BR': ['Бразилии', 'в Бразилии'],
    'MX': ['Мексики', 'в Мексике'],
}


def generator_1(cities, countries, ac=25):

    # city bags
    cbags = []
    dbags = {}

    for c in cities:
        if len(c) > 8:
            if c[2] in BAG:
                # print ("%s — %s" % (c[4], c[9]))
                cbags.append(c)
                if c[2] in dbags:
                    dbags[c[2]].append(c)
                else:
                    dbags[c[2]] = [c, ]

    # Генераторы заданий
    tasks = []

    # ГОРОДА ↔ СТРАНЫ
    aa = 4
    ab = 4
    for q in range(ac):

        for b in dbags.keys():

            bname = BAG_RUS2[BAG.index(b)]

            bc = []

            # правильные ответы
            l = len(dbags[b])
            for i in range(aa):
                while True:
                    idx = int(l * 0.3 * random.random())
                    candy = dbags[b][idx]
                    if candy not in bc:
                        bc.append(candy)
                        break

            # НЕправильные ответы
            for i in range(ab):
                w = random.choice(list(filter(lambda x: x != b, BAG)))
                l = len(dbags[w])
                idx = int(l * 0.75 * random.random())
                bc.append(dbags[w][idx])

            print(b)
            print(bc)

            # { "task": "Выберите", "answs": [ "Рим", ], "correct": [0,1, 4, 5 ] }
            task = {}
            task['task'] = """Выберите <strong>города %s</strong>""" % (bname.upper(), )
            task['answs'] = []
            task['correct'] = []

            bids = list(range(len(bc)))
            for i in 'qwertyu':
                random.shuffle(bids)

            for i in range(len(bc)):
                if bids[i] < aa:
                    task['answs'].append([bc[bids[i]][4], None, 1])
                else:
                    if bc[bids[i]][4] != bc[bids[i]][1]:
                        exp = "%s (%s) %s %s" % (bc[bids[i]][4],
                                                 bc[bids[i]][1],
                                                 " — город" if i % 2 else "находится",
                                                 BAGS_RUS3[bc[bids[i]][2]][1])
                    else:
                        exp = "%s %s %s" % (bc[bids[i]][4],
                                            " — город" if i % 2 else "находится",
                                            BAGS_RUS3[bc[bids[i]][2]][1])

                    task['answs'].append([bc[bids[i]][4], exp, 0])

                # task['answs'].append(bc[bids[i]][4])
                # if bids[i] < aa:
                #     task['correct'].append(i)

            tasks.append(task)

    return tasks


def filt_caps(c):
    if len(c) > 8:
        if unidecode.unidecode(c[1]).lower() == unidecode.unidecode(c[7]).lower():
            return True
    return False


def generator_2(cities, countries, ac=35):

    tasks = []
    # ГОРОДА == СТОЛИЦЫ
    # caps = sorted(filter(lambda x: len(x) > 8 and x[1] == x[7], cities), key=lambda x: -x[8])
    caps = sorted(filter(filt_caps, cities), key=lambda x: -x[8])
    print(caps)

    aa = 3
    ab = 5
    for q in range(ac):

        bc = []
        # правильные ответы
        l = len(caps)
        for i in range(aa):
            while True:
                idx = int(l * 0.15 * random.random())
                candy = caps[idx]
                if candy not in bc:
                    bc.append(candy)
                    break

        # НЕправильные ответы
        l = len(cities)
        for i in range(ab):
            while True:
                idx = int(l * 0.25 * random.random())
                candy = cities[idx]
                if candy not in bc and candy not in caps:
                    bc.append(candy)
                    break

        print(bc)

        # { "task": "Выберите", "answs": [ "Рим", ], "correct": [0,1, 4, 5 ] }
        task = {}
        task['task'] = """Выберите только <strong>столицы государств</strong>"""
        task['answs'] = []
        task['correct'] = []

        bids = list(range(len(bc)))
        random.shuffle(bids)

        for i in range(len(bc)):
            if bids[i] < aa:
                exp = "%s (%s) — %s" % (bc[bids[i]][4], bc[bids[i]][1], bc[bids[i]][-1])
                task['answs'].append([bc[bids[i]][4], exp, 1])
            else:
                # exp = "%s — %s" % (bc[bids[i]][4], bc[bids[i]][-1])
                task['answs'].append([bc[bids[i]][4], None, 0])
            # task['answs'].append(bc[bids[i]][4])
            # if bids[i] < aa:
            #     task['correct'].append(i)

        tasks.append(task)

    return tasks


# random.shuffle(tasks)

if __name__ == '__main__':
#    cities, countries = parse_files()
#    save_files(cities, countries)

    cities, countries = load_files()

    tasks = []

    tasks += generator_1(cities, countries, 17)
    tasks += generator_2(cities, countries, 120)

    random.shuffle(tasks)

    i = 0
    games = []
    bk = {'data': []}
    for task in tasks:

        i += 1

        bk['data'].append(task)

        if i % TASK_SIZE == 0:
            bk['engine'] = 'tktk'
            bk['topic'] = 'города'
            bk['lang'] = 'ru'
            bk['name'] = 'моря и страны'
            games.append(bk)
            bk = {'data': []}

    print("len(games)= %s × %s (%s tasks)" % (len(games), TASK_SIZE, len(tasks)))
    open('geodata-games.json', 'w').write(json.dumps(games, indent=2, ensure_ascii=False))
