# -*- coding: utf-8 -*-

import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import zlib
import json
import re
import sys
import xml.sax

whends_re = re.compile('(^[\s\n\r]+|[\s\n\r]+$)', re.I | re.U | re.M)
whends0_re = re.compile('(^[\s\n\r]+)|([\s\n\r]+$)', re.I | re.U)
whites_re = re.compile('[\s\n\r]+', re.I | re.U | re.M)
whites0_re = re.compile('[ ]{2,}', re.I | re.U | re.M)

wiki_cleanup_magic_words = re.compile(r'__([A-Z]{3,})__', re.U | re.M)

title_sfx = re.compile(r'\s*\(.+\)$', re.U | re.M)

WIKI_DEBUG = False
SKIP_REFS = True
SKIP_TABLES = True
SKIP_MEDIA = True


def sstrip(t):

    if not t:
        return ""
    t = whends_re.sub('', t)
    t = whites_re.sub(' ', t)
    return t


def int0(s):
    try:
        return int(s)
    except:
        return 0


class WikiReader(xml.sax.handler.ContentHandler):

    INIT, PAGE, TITLE, TEXT, TEXT_REDIRECTED, PCOMMENT = list(range(6))

    def __init__(self, **kwargs):
        self.mode = WikiReader.INIT
        self.level = 0
        self.pages = 0
        self.count = 0
        self.text = None
        self.page_lang = ''
        self.texts = []

    def startElement(self, name, attrs):
        self.level += 1

        if name == "page":
            self.mode = WikiReader.PAGE

        elif name == "title" and self.mode == WikiReader.PAGE:
            self.mode = WikiReader.TITLE
            self.texts = None

        elif name == "text" and self.mode == WikiReader.PAGE:
            self.mode = WikiReader.TEXT
            self.texts = None

        elif name == "comment" and self.mode == WikiReader.PAGE:
            self.mode = WikiReader.PCOMMENT
            self.texts = None

        elif name == "redirect" and self.mode == WikiReader.PAGE:
            self.mode = WikiReader.TEXT_REDIRECTED
            self.texts = None

    def characters(self, content):
        if self.texts is None:
            self.texts = [content]
        else:
            self.texts.append(content)

    def endElement(self, name):

        self.level -= 1

        if name == "page":
            self.mode = WikiReader.INIT
            self.pages += 1
            if self.count % 100 == 0:
                save_awiki()
            if self.pages % 1000 == 0:
                print("# pages = %s / %s" % (self.pages, self.count),
                      file=sys.stderr)

        elif name == "title" and self.mode == WikiReader.TITLE:
            self.title = "".join(self.texts) if self.texts is not None else ""
            self.mode = WikiReader.PAGE

        elif name == "comment" and self.mode == WikiReader.PCOMMENT:
            t = "".join(self.texts) if self.texts is not None else ""
            mo = re.search(r'langs: ([a-z]{2})', t)
            if mo:
                self.page_lang = mo.group(1)
            else:
                self.page_lang = ""
            self.mode = WikiReader.PAGE

        elif name == "text" and self.mode == WikiReader.TEXT:

            self.mode = WikiReader.PAGE

            text = "".join(self.texts) if self.texts is not None else ""

            if self.page_lang != 'ru' or self.title.find(':') > 0 or self.title.find('/') > 0:
                return

            if self.title not in nv1k.n1k and self.title not in nv1k.v1k:
                return

            if len(text) > 0:

                data = self.examine_word(text)
                if data:
                    a = {}
                    a['word'] = self.title
                    a['data'] = data
                    awiki.append(a)
                    self.count += 1

    def examine_word(self, text):

        wklinks_re = re.compile(r'\[\[([a-zA-Zа-яА-Я]{4,})\]\]')

        # === Морфо
        morph = None
        morph_re = re.compile(r'===\s*Морфологические и синтаксические свойства\s*===(.*?)===', re.I | re.DOTALL)
        mo = morph_re.search(text)
        if mo:
            tmo = mo.group(1)
            if tmo.find('{{сущ ru') >= 0:
                morph = "N"
            elif tmo.find('{{гл ru') >= 0:
                morph = 'V'
            elif tmo.find('{{прил ru') >= 0:
                morph = 'A'

        ants = []
        ant0_re = re.compile(r'====\s*Антонимы\s*====(.*?)====', re.I | re.DOTALL)
        mo = ant0_re.search(text)
        if mo:
            # [[отмель]], [[мель]]; {{помета|частичн.}}, {{разг.|-}}: [[мелкота]]
            for w in wklinks_re.findall(mo.group(1)):
                ants.append(w)

        syns = []
        sin0_re = re.compile(r'====\s*Синонимы\s*====(.*?)====', re.I | re.DOTALL)
        mo = sin0_re.search(text)
        if mo:
            # [[отмель]], [[мель]]; {{помета|частичн.}}, {{разг.|-}}: [[мелкота]]
            for w in wklinks_re.findall(mo.group(1)):
                syns.append(w)

        if morph is not None and len(syns) > 0:
            return {'syns': syns, 'ants': ants, 'morph': morph}
        else:
            return None

awiki = []


def save_awiki(sfx=''):

    f = open('awiki%s.json' % sfx, 'w')
    f.write(json.dumps(awiki, indent=2, ensure_ascii=False))
    f.close()


if __name__ == "__main__":

    print("@ %s" % (__file__, ), file=sys.stderr)

    if len(sys.argv) > 1:
        WIKI_FILE = sys.argv[1]

    f = open(WIKI_FILE)

    wiki = WikiReader()

    parser = xml.sax.make_parser()
    parser.setContentHandler(wiki)
    parser.parse(f)
    save_awiki()
