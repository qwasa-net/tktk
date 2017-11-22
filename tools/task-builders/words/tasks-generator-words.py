# -*- coding: utf-8 -*-

import json
import re
import sys
import random

TASK_SIZE = 9
WIKI_INFILE = "wiki.json"
NOUNS_INFILE = "ru_1000_nouns.txt"
VERBS_INFILE = "ru_1000_verbs.txt"


def generate_symons(words, allwords):

    tasks = []
    oks = 3
    bads = 4
    c = 0

    for w in words:

        syns = w['data']['syns']
        ants = w['data']['ants']

        if len(syns) >= oks:

            qwords = syns[:oks]

            j = 0
            while True:
                bw = random.choice(allwords)
                if bw == w['word'] or bw in syns:
                    continue

                qwords.append(bw)

                j += 1
                if j >= bads:
                    break

            c += 1
            print(c, w['word'], syns, qwords)

            task = {}
            task['task'] = """Выберите синонимы к слову <strong>%s</strong>""" % w['word']
            task['answs'] = []
            task['correct'] = []

            bids = list(range(len(qwords)))
            random.shuffle(bids)

            for i in range(len(qwords)):
                task['answs'].append(qwords[bids[i]])
                if bids[i] < oks:
                    task['correct'].append(i)

            tasks.append(task)

    return tasks


def generate_verbs(words, qc=80, t1='N', t2='V'):

    tasks = []
    oks = 3
    bads = 3
    c = 0

    for k in range(qc):

        qwords = []

        i = 0
        while True:
            bw = random.choice(wkwords[t1])
            if bw in wkwords[t2]:
                continue

            qwords.append(bw)

            i += 1
            if i >= oks:
                break

        i = 0
        while True:

            bw = random.choice(wkwords[t2])
            if bw in wkwords[t1]:
                continue

            qwords.append(bw)
            i += 1
            if i >= bads:
                break

        c += 1
        print(c, qwords)

        task = {}
        if t1 == 'N':
            task['task'] = """Выберите всё <strong>существительные</strong>"""
        elif t1 == 'V':
            task['task'] = """Выберите всё <strong>глаголы</strong>"""

        task['answs'] = []
        task['correct'] = []

        bids = list(range(len(qwords)))
        random.shuffle(bids)

        for i in range(len(qwords)):
            task['answs'].append(qwords[bids[i]])
            if bids[i] < oks:
                task['correct'].append(i)

        tasks.append(task)

    return tasks


def generate_conundrum(words, wwl=8, wl=4):

    tasks = []
    oks = 3
    bads = 3
    c = 0

    # все слова
    for ww in words:

        if len(ww) < wwl:
            continue

        # количество букв
        lls = {}
        for l in ww:
            lc = ww.count(l)
            lls[l] = lc

        cons = []

        # подбор подходящих
        for w in words:

            if w == ww or len(w) < wl:
                continue

            good = True

            # каждая буква есть в супер-слове
            for l in w:
                if l not in lls or w.count(l) > lls[l]:
                    good = False
                    break

            if good:
                cons.append(w)

        # сколько-то набралось
        if len(cons) < oks:
            continue

        random.shuffle(cons)
        #cons = sorted(cons, key=lambda x: len(x), reverse=True)
        qwords = cons[:3]

        i = 0
        while True:

            bw = random.choice(words)
            if bw in cons or len(bw) < wl:
                continue

            qwords.append(bw)
            i += 1
            if i >= bads:
                break

        c += 1
        print(c, ww, qwords)

        task = {}
        task['task'] = """Выберите слова, которые можно составить из букв слова <strong>%s</strong>""" % ww

        task['answs'] = []
        task['correct'] = []

        bids = list(range(len(qwords)))
        random.shuffle(bids)

        for i in range(len(qwords)):
            task['answs'].append(qwords[bids[i]])
            if bids[i] < oks:
                task['correct'].append(i)

        tasks.append(task)

    return tasks


tasks = []

if __name__ == "__main__":

    print("@ %s" % (__file__, ), file=sys.stderr)

    wkwords = {}

    if len(sys.argv) > 1:
        WIKI_INFILE = sys.argv[1]

    words = json.loads(open(WIKI_INFILE).read())

    nouns_words = list(filter(None, open(NOUNS_INFILE, "r").read().splitlines()))
    verbs_words = list(filter(None, open(VERBS_INFILE, "r").read().splitlines()))
    allwords = nouns_words + verbs_words

    for w in words:
        m = w['data']['morph']
        if m in wkwords:
            wkwords[m].append(w['word'])
        else:
            wkwords[m] = [w['word'], ]

    print(wkwords.keys())

    tasks = []
    tasks += generate_symons(words, allwords)
    tasks += generate_verbs(wkwords, 200, 'V', 'N')
    tasks += generate_verbs(wkwords, 200, 'N', 'V')
    tasks += generate_conundrum(nouns_words)
    tasks += generate_conundrum(verbs_words, 10, 6)

    random.shuffle(tasks)

    i = 0
    games = []
    bk = {'data': []}
    for task in tasks:

        i += 1

        bk['data'].append(task)

        if i % TASK_SIZE == 0:
            bk['engine'] = 'tktk'
            bk['topic'] = 'слова'
            bk['lang'] = 'ru'
            bk['name'] = 'буквы и слова'
            games.append(bk)
            bk = {'data': []}

    print("len(games)= %s × %s (%s tasks)" % (len(games), TASK_SIZE, len(tasks)))
    open('words-games.json', 'w').write(json.dumps(games, indent=2, ensure_ascii=False))
