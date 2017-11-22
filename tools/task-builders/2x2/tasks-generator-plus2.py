
import csv
import re
import json
import random
import math

TASK_SIZE = 9
cre = re.compile(
    r'^([A-Z]{2})\t([A-Z]+)\t([0-9A-Z]*)\t([0-9A-Z]*)\t([^\t]+)\t([^\t]+)\t([0-9]+).*\t([0-9]+)\t([^\t]*)[\r\n]?', re.I | re.U)
are = re.compile(r'^([0-9]+)\t([0-9]+)\t([a-zA-Z]{2})\t([^\t]+)', re.I | re.U)
russo_re = re.compile(r'[йцукенгшщзхъэждлорпавыфячсмитьбю]')


def generator_22(ac=500, bads=4):

    ops = ['+', '-', '×', '÷']

    for q in range(ac):

        op = random.choice(ops)

        if op == '+':

            a = int(random.random() * 150 + 10)
            b = int(random.random() * 150 + 5)
            c = a + b
            s = "%s %s %s" % (a, op, b)

        elif op == '-':

            ab = [int(random.random() * 100 + 20), int(random.random() * 250 + 1)]
            a = max(ab)
            b = min(ab)
            if a == b:
                a = int((1.1 + random.random()) * a)

            c = a - b
            s = "%s %s %s" % (a, op, b)

        elif op == '×':

            a = max(int(random.random() * 50 + 1), 1)
            b = int(random.random() * 120 + 1)
            c = a * b
            s = "%s %s %s" % (a, op, b)

        elif op == '÷':

            b = int(random.random() * 50 + 1)
            c = max(int(random.random() * 120 + 1), 2)
            a = c * b
            s = "%s %s %s" % (a, op, b)

        ans = [c, ]

        # НЕправильные ответы
        while len(ans) < (bads + 1):

            if len(ans) < bads / 2:
                cx = int(c * 3 * random.random())
            else:
                cx = int(120 * random.random())

            if cx in ans:
                continue

            ans.append(cx)

        print(s, ans)

        # { "task": "Выберите", "answs": [ "Рим", ], "correct": [0,1, 4, 5 ] }
        task = {}
        task['task'] = """<strong>%s</strong>""" % (s, )
        task['answs'] = []
        task['correct'] = []

        bids = list(range(len(ans)))
        random.shuffle(bids)

        for i in range(len(ans)):
            task['answs'].append(ans[bids[i]])
            if bids[i] == 0:
                task['correct'].append(i)

        tasks.append(task)

    return tasks

if __name__ == '__main__':
#    cities, countries = parse_files()
#    save_files(cities, countries)

    tasks = []

    tasks += generator_22()

    random.shuffle(tasks)

    i = 0
    games = []
    bk = {'data': []}
    for task in tasks:

        i += 1

        bk['data'].append(task)

        if i % TASK_SIZE == 0:
            bk['engine'] = 'tktk'
            bk['topic'] = '2+2'
            bk['name'] = 'устный счёт'
            bk['config'] = {'auto_next': True, 'auto_next_delay': 1000, 'butsize': 'huge'}
            games.append(bk)
            bk = {'data': []}

    print("len(games)= %s × %s (%s tasks)" % (len(games), TASK_SIZE, len(tasks)))
    open('plus2-games.json', 'w').write(json.dumps(games, indent=2, ensure_ascii=False))
