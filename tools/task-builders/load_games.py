import argparse
import json
import sys
import pytils

import django
django.setup()
import apps.pw.models as models


def reset_database():
    rc = models.Game.objects.all().delete()
    print(rc, file=sys.stderr)

    rc = models.Engine.objects.all().delete()
    print(rc, file=sys.stderr)

    rc = models.Topic.objects.all().delete()
    print(rc, file=sys.stderr)


def load_file(fname, save=False):

    games = json.load(open(fname))

    engines = {}
    topics = {}

    for g in games:

        t = g.get('topic', None)
        e = g.get('engine', None)

        # engine -- get or create
        if e not in engines:
            try:
                engine = models.Engine.objects.get(name=e)
            except:
                engine = models.Engine()
                engine.name = e
                engine.slug = pytils.translit.slugify(e)
                if save:
                    engine.save()
                else:
                    print(engine)
            engines[e] = engine

        # topic -- get or create
        if t not in topics:
            try:
                topic = models.Topic.objects.get(name=t)
            except:
                topic = models.Topic()
                topic.engine = engines[e]
                topic.slug = pytils.translit.slugify(t)
                topic.name = t
                if save:
                    topic.save()
                else:
                    print(topic)
            topics[t] = topic

        game = models.Game()
        game.topic = topics[t]
        game.name = g.get('name', None)
        cfg = g.get('config', None)
        if cfg is not None:
            # game.config = json.dumps(cfg, indent=1, ensure_ascii=False)
            game.config = json.dumps(cfg, ensure_ascii=False)
        game.data = json.dumps(g.get('data', None), ensure_ascii=False)
        if save:
            game.save()
        else:
            print(game)

        print(game.id, game)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("infiles", metavar="INFILE.json", nargs='+', type=str)
    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--save', action='store_true')
    args = parser.parse_args()

    if args.reset:
        reset_database()

    for infile in args.infiles:
        load_file(infile, args.save)
        print(infile)


if __name__ == "__main__":
    main()
