# -*- coding: utf-8 -*-
# :Project:   SoL -- Configuration tool
# :Created:   gio 18 apr 2013 18:43:18 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2015, 2016, 2018, 2019, 2020 Lele Gaifax
#

from argparse import ArgumentParser, SUPPRESS
from binascii import hexlify
from datetime import date
from hashlib import md5
from math import exp
from os import makedirs, urandom
from os.path import abspath, dirname, exists, join
import re
from shutil import copyfile
import sys
from time import time
from urllib.request import urlopen

from sqlalchemy import engine_from_config
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from metapensiero.sqlalchemy.proxy.json import register_json_decoder_encoder

from pyramid.paster import get_appsettings, setup_logging

import sol
from sol.models import Base, Club, Player, Rate, Rating, bio
from sol.models.utils import normalize
from sol.views import json_decode, json_encode


def create_config(args):
    "Dump/update a configuration file suitable for production"

    if exists(args.config):
        print('The config file "%s" already exists!' % args.config)
        return update_config(args)

    alembicdir = args.alembic_dir or join(dirname(dirname(sol.__file__)), 'alembic')
    datadir = args.data_dir
    secret = hexlify(urandom(20)).decode('ascii')
    signer_secret_key = hexlify(urandom(20)).decode('ascii')
    admin = args.admin
    password = args.password
    if not password:  # pragma: nocover
        password = input('Choose a password for the "%s" super user: ' % admin)
    if not password:  # pragma: nocover
        password = hexlify(urandom(5)).decode('ascii')
        random_password = True
    else:
        random_password = False

    if not all(c.isalnum() for c in admin):
        print("Invalid admin name, only letters and digits allowed!")
        return 128

    if len(password) < 8 or password.isdigit():
        print("Invalid password, must be at least eight characters and not all digits!!")
        return 128

    with open(join(dirname(__file__), "config.tpl"), encoding='utf-8') as f:
        configuration = f.read()

    with open(args.config, 'w', encoding='utf-8') as f:
        f.write(configuration.format(secret=secret, signer_secret_key=signer_secret_key,
                                     admin=admin, password=password,
                                     alembicdir=alembicdir, datadir=datadir))

    print('The configuration file "%s" has been successfully created' % args.config)
    print('The password for the "%s" super user is "%s"%s' % (
        admin, password, ", you should change it!" if random_password else ""))


def update_config(args):
    "Update an existing configuration file"

    if not exists(args.config):
        print('The config file "%s" does not exists!' % args.config)
        return 128

    with open(args.config, 'r', encoding='utf-8') as f:
        configuration = f.read()

    alembicdir = args.alembic_dir or get_alembic_dir()
    substitutions = [(re.compile(r'script_location\s*=\s*(.+)\s*$'),
                      alembicdir,
                      'script_location = %s')]
    admin = args.admin
    if admin is not None:
        if admin == 'ask':  # pragma: nocover
            admin = input('Choose a name for the super user (defaults to "admin"): ' % admin)
            admin = admin.strip()
            if not admin:
                admin = "admin"
        else:
            admin = admin.strip()

        if not all(c.isalnum() for c in admin):
            print("Invalid admin name, only letters and digits allowed!")
            return 128

        substitutions.append((re.compile(r'sol\.admin\.user\s*=\s*(.+)\s*$'),
                              admin,
                              'sol.admin.user = %s'))
    password = args.password
    if password is not None:
        if password == 'ask':  # pragma: nocover
            password = input('Choose a password for the super user: ')
        password = password.strip()

        if len(password) < 8 or password.isdigit():
            print("Invalid password, must be at least eight characters and not all digits!!")
            return 128

        substitutions.append((re.compile(r'sol\.admin\.password\s*=\s*(.+)\s*$'),
                              password,
                              'sol.admin.password = %s'))

    updated = False
    lines = configuration.splitlines()
    for pos, line in enumerate(lines):
        for rx, value, repl in substitutions:
            match = rx.match(line)
            if match is not None:
                if match.group(1) != value:
                    lines[pos] = repl % value
                    updated = True

    if updated:
        with open(args.config, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
            f.write('\n')

        print('The configuration file "%s" has been successfully updated' % args.config)
    else:
        print('The configuration file "%s" is already up-to-date!' % args.config)


def initialize_db(args):
    "Initialize the database structure"

    if not exists(args.config):  # pragma: no cover
        print('The config file "%s" does not exist!' % args.config)
        return 128

    setup_logging(args.config)
    settings = get_appsettings(args.config)
    engine = engine_from_config(settings, 'sqlalchemy.')

    if engine.has_table('tourneys'):  # pragma: no cover
        print('Database "%s" already exist.'
              ' You may want to execute "upgrade-db" instead...' % engine.url)
        return None

    Base.metadata.create_all(engine)

    print('The database "%s" has been successfully initialized' % engine.url)

    from alembic.config import Config
    from alembic import command

    cfg = Config(args.config, ini_section="app:main")
    if args.use_default_alembic_dir:
        print("Will use 'script_location' from the package")
        cfg.set_main_option('script_location', get_alembic_dir())
    command.stamp(cfg, "head")


def upgrade_db(args):
    "Upgrade the database structure"

    if not exists(args.config):  # pragma: no cover
        print('The config file "%s" does not exist!' % args.config)
        return 128

    from alembic.config import Config
    from alembic import command

    setup_logging(args.config)
    settings = get_appsettings(args.config)
    engine = engine_from_config(settings, 'sqlalchemy.')

    cfg = Config(args.config, ini_section="app:main")
    if args.use_default_alembic_dir:
        print("Will use 'script_location' from the package")
        cfg.set_main_option('script_location', get_alembic_dir())
    command.upgrade(cfg, "head")

    print('The database "%s" has been successfully upgraded' % engine.url)


def restore_all(args):
    "Load historic data into the database, player's portraits and club's emblems as well"

    if not exists(args.config):  # pragma: no cover
        print('The config file "%s" does not exist!' % args.config)
        return 128

    setup_logging(args.config)
    settings = get_appsettings(args.config)
    engine = engine_from_config(settings, 'sqlalchemy.')

    register_json_decoder_encoder(json_decode, json_encode)

    sasess = Session(bind=engine)

    pdir = settings['sol.portraits_dir']
    if not exists(pdir):  # pragma: no cover
        makedirs(pdir, mode=0o700)

    edir = settings['sol.emblems_dir']
    if not exists(edir):  # pragma: no cover
        makedirs(edir, mode=0o700)

    if args.url.startswith('file://') or exists(args.url):
        if not args.url.startswith('file://'):
            args.url = abspath(args.url)
        backup_url = args.url
    else:
        backup_url = args.url + 'bio/backup?serialization_format=json'
        if not args.all:
            backup_url += '&only_played_tourneys=1'

    print("Loading backup from %s..." % backup_url)

    try:
        tourneys, skipped = bio.restore(sasess, pdir, edir, url=backup_url)
        sasess.commit()
    except Exception:
        sasess.rollback()
        raise
    finally:
        sasess.close()

    print("Done, %d new/updated tourneys, %d skipped/already present." % (len(tourneys),
                                                                          skipped))


def backup_all(args):
    "Save a backup of the database, player's portraits and club's emblems as well"

    if not exists(args.config):
        print('The config file "%s" does not exist!' % args.config)
        return 128

    setup_logging(args.config)
    settings = get_appsettings(args.config)
    engine = engine_from_config(settings, 'sqlalchemy.')

    register_json_decoder_encoder(json_decode, json_encode)

    sasess = Session(bind=engine)
    pdir = settings['sol.portraits_dir']
    edir = settings['sol.emblems_dir']

    print("Saving backup to %s..." % args.location)

    try:
        bio.backup(sasess, pdir, edir,
                   args.location, args.keep_only_if_changed)
        sasess.commit()
    except Exception:
        sasess.rollback()
        raise
    finally:
        sasess.close()

    print("Done.")


def player_unique_hash(firstname, lastname, nickname):
    hash = md5()
    hash.update(firstname.encode('ascii', 'ignore'))
    hash.update(lastname.encode('ascii', 'ignore'))
    hash.update(nickname.encode('ascii', 'ignore'))
    hash.update(str(time()).encode('ascii', 'ignore'))
    return hash.hexdigest()[:15]


def _evaluator(fmap, formula):
    def evaluator(record, fmap=fmap, formula=formula):
        locs = {}
        for fname in fmap.values():
            if fname in fmap:
                try:
                    locs[fname] = float(record[fname])
                except Exception:
                    pass
        return eval(formula, {'exp': exp}, locs)

    test = {fname: '1' for fname in fmap.values()}
    try:
        evaluator(test)
    except Exception:  # pragma: nocover
        return None
    else:
        return evaluator


def load_historical_rating(args):
    "Load historic rating into the database from a CSV text file"

    if not exists(args.config):
        print('The config file "%s" does not exist!' % args.config)
        return 128

    fmap = dict(firstname='firstname',
                lastname='lastname',
                nickname='nickname')
    for item in args.map:
        if '=' in item:
            internal, external = item.split('=')
            internal = internal.strip()
            external = external.strip()
        else:
            internal = external = item.strip()
        fmap[internal] = external

    refdate = date(*map(int, args.date.split('-')))

    try:
        int(args.deviation)
    except ValueError:
        deviation = _evaluator(fmap, args.deviation)
        if deviation is None:
            print('The formula "%s" to compute the deviation is invalid!' % args.deviation)
            return 128
    else:
        deviation = lambda dummy, rd=int(args.deviation): rd  # noqa

    try:
        float(args.volatility)
    except ValueError:
        volatility = _evaluator(fmap, args.volatility)
        if volatility is None:
            print('The formula "%s" to compute the volatility is invalid!' % args.volatility)
            return 128
    else:
        volatility = lambda dummy, rd=args.volatility: rd  # noqa

    if args.rate is not None:
        rate = _evaluator(fmap, args.rate)
        if rate is None:
            print('The formula "%s" to compute the rate is invalid!' % args.rate)
            return 128
    else:
        rate = lambda record: record[fmap['rate']]  # noqa

    if not args.dry_run:
        setup_logging(args.config)

    settings = get_appsettings(args.config)
    engine = engine_from_config(settings, 'sqlalchemy.')
    sasess = Session(bind=engine)

    if not args.dry_run:
        if sasess.query(Rating).filter_by(description=args.description).first():
            print('Rating "%s" already exists!' % args.description)
            return 128

    if args.url.startswith('file://') or exists(args.url):
        if not args.url.startswith('file://'):
            args.url = "file://" + abspath(args.url)

    print("Loading ratings from %s..." % args.url)

    separator = '\t' if args.tsv else ','

    new = set()
    done = set()
    rates = []

    with urlopen(args.url) as csvfile:
        data = csvfile.read().decode(args.encoding)

    lines = data.splitlines()
    columns = [c.strip() for c in lines.pop(0).split(separator)]
    for c in fmap.values():
        if c not in columns:
            print('Column "%s" not found!' % c)
            return 128

    try:
        for record in (dict(zip(columns, row.split(separator))) for row in lines):
            firstname = normalize(record[fmap['firstname']].strip())
            lastname = normalize(record[fmap['lastname']].strip())
            nickname = record[fmap['nickname']].strip()

            if (firstname, lastname, nickname) in done:
                continue

            done.add((firstname, lastname, nickname))

            try:
                player, merged_into = Player.find(sasess, lastname, firstname, nickname)
            except MultipleResultsFound:
                nickname = player_unique_hash(firstname, lastname, nickname)

            if player is None:
                player = Player(firstname=firstname, lastname=lastname, nickname=nickname)
                new.add(player)
                if 'sex' in fmap:
                    sex = record[fmap['sex']].strip().upper()
                    if sex in 'FM':
                        player.sex = sex
                if 'club' in fmap:
                    clubdesc = normalize(record[fmap['club']].strip())
                    if clubdesc:
                        try:
                            club = sasess.query(Club).filter_by(description=clubdesc).one()
                        except NoResultFound:
                            club = Club(description=clubdesc)

                        player.club = club

            rates.append(Rate(date=refdate, player=player,
                              rate=int(rate(record)),
                              deviation=int(deviation(record)),
                              volatility=volatility(record)))

        if args.dry_run:
            for rate in rates:
                print("%s%s (%s): rate=%d deviation=%s volatility=%s" % (
                    "NEW " if rate.player in new else "",
                    rate.player, rate.player.club,
                    rate.rate, rate.deviation, rate.volatility))
            # Force a rollback
            raise SystemExit
        else:
            rating = Rating(description=args.description,
                            level=args.level,
                            inherit=args.inherit,
                            rates=rates)
            sasess.add(rating)

        sasess.commit()
        print("Done, %d new rates." % len(rates))
    except Exception:
        sasess.rollback()
        raise
    finally:
        sasess.close()


def _sound(which, ogg):
    if not exists(ogg):
        print('Specified sound file "%s" does not exist!' % ogg)
        return 128
    if not ogg.endswith('.ogg'):
        print('The sound file must be a OGG and have ".ogg" as extension!')
        return 128

    target = join(dirname(dirname(abspath(__file__))), 'static', 'sounds',
                  which+'.ogg')
    print('Copying "%s" to "%s"...' % (ogg, target))
    copyfile(ogg, target)


def start_sound(args):
    "Replace the start sound"

    return _sound('start', args.sound)


def stop_sound(args):
    "Replace the stop sound"

    return _sound('stop', args.sound)


def prealarm_sound(args):
    "Replace the prealarm sound"

    return _sound('prealarm', args.sound)


def get_alembic_dir():
    """Return the default ``script_location``"""
    return join(dirname(dirname(sol.__file__)), 'alembic')


def main(args=None):
    parser = ArgumentParser(description="SoL command line admin utility",
                            epilog=('You can get individual commands help'
                                    ' with "soladmin sub-command -h".'))
    subparsers = parser.add_subparsers()

    subp = subparsers.add_parser('create-config',
                                 help=create_config.__doc__)
    subp.add_argument('-a', '--admin', default='admin',
                      help="Specify the name of the super user, “admin”"
                      " by default")
    subp.add_argument('-p', '--password', help="Specify the admin password,"
                      " if not set you will be prompted for one")
    subp.add_argument('-d', '--data-dir', default='%(here)s',
                      help="Directory where data (db, emblems, portraits, backups and logs)"
                      " will be stored, by default the one containing the configuration file")
    # For test purpose, the location of the alembic scripts
    subp.add_argument('--alembic-dir', help=SUPPRESS)
    subp.add_argument('config', help="Name of the new configuration file")
    subp.set_defaults(func=create_config)

    subp = subparsers.add_parser('update-config',
                                 help=update_config.__doc__)
    subp.add_argument('-a', '--admin',
                      help="Specify the new name of the super user, with the value “ask”"
                      " it will be prompted interactively")
    subp.add_argument('-p', '--password', help="Specify the new admin password, with the value"
                      " “ask” it will be prompted interactively")
    # For test purpose, the location of the alembic scripts
    subp.add_argument('--alembic-dir', help=SUPPRESS)
    subp.add_argument('config', help="Name of the existing configuration file")
    subp.set_defaults(func=update_config)

    subp = subparsers.add_parser('initialize-db',
                                 help=initialize_db.__doc__)
    subp.add_argument('--use-default-alembic-dir', default=False, action='store_true',
                      help="Override the 'script_location' parameter in the file"
                      " with the default of the package ({})".format(get_alembic_dir()))
    subp.add_argument('config', help="Name of the configuration file")
    subp.set_defaults(func=initialize_db)

    subp = subparsers.add_parser('upgrade-db',
                                 help=upgrade_db.__doc__)
    subp.add_argument('--use-default-alembic-dir', default=False, action='store_true',
                      help="Override the 'script_location' parameter in the file"
                      " with the default of the package ({})".format(get_alembic_dir()))
    subp.add_argument('config', help="Name of the configuration file")
    subp.set_defaults(func=upgrade_db)

    subp = subparsers.add_parser('restore',
                                 help=restore_all.__doc__)
    subp.add_argument('-a', '--all', default=False, action="store_true",
                      help="By default only played tourneys are transfered,"
                      " i.e. only those with at least one played match. This"
                      " flag restores all tourneys.")
    subp.add_argument('config', help="Name of the configuration file")
    subp.add_argument('url', default="https://sol4.metapensiero.it/",
                      nargs="?",
                      help='URL from where historic data will be loaded'
                      ' if different from "https://sol4.metapensiero.it/".'
                      ' It may also be a file:// URI or a local file path'
                      ' name.')
    subp.set_defaults(func=restore_all)

    subp = subparsers.add_parser('backup',
                                 help=backup_all.__doc__)
    subp.add_argument('-k', '--keep-only-if-changed', default=False,
                      action="store_true",
                      help="If given, and the location argument is a"
                      " directory containing other backup archives,"
                      " keep the new backup only if it is different"
                      " from the previous one.")
    subp.add_argument('config', help="Name of the configuration file")
    subp.add_argument('location', nargs="?", default='.',
                      help='Local file name where the backup will be written.'
                      ' If it actually points to an existing directory (its'
                      ' default value is ".", the current working directory)'
                      ' the file name will be generated from the current time'
                      ' and with a ".zip" extension.')
    subp.set_defaults(func=backup_all)

    subp = subparsers.add_parser('load-historical-rating',
                                 help=load_historical_rating.__doc__)
    subp.add_argument('--date', default='1900-01-01',
                      help="Bogus rates date, by default 1900-01-01")
    subp.add_argument('--deviation', default='100',
                      help="Value of the deviation, by default 100,"
                      " or a formula to compute it from other fields")
    subp.add_argument('--volatility', default='0.006',
                      help="Value of the volatility, by default 0.006,"
                      " or a formula to compute it from other fields")
    subp.add_argument('--rate', default=None,
                      help="Formula to compute the player's rate, if needed")
    subp.add_argument('--description',
                      help='Description of the historical rating')
    subp.add_argument('--level', choices='0,1,2,3,4'.split(','), default="0",
                      help="Rating level, 0 by default: 0=historical, 1=international,"
                      " 2=national, 3=regional, 4=courtyard")
    subp.add_argument('--inherit', default=False, action="store_true",
                      help="Whether player's rate will be inherited from other"
                      " ratings at the same level or better, False by default")
    subp.add_argument('--map', action='append', default=[],
                      help="Specify a map between internal (SoL) field name and"
                      " external one")
    subp.add_argument('--encoding', default='utf-8',
                      help="Encoding of the CSV file, by default UTF-8")
    subp.add_argument('--tsv', default=False, action="store_true",
                      help="Fields are separated by a TAB, not by a comma")
    subp.add_argument('--dry-run', default=False, action="store_true",
                      help="Just show the result, do not actually insert data")
    subp.add_argument('config', help="Name of the configuration file")
    subp.add_argument('url',
                      help="URL from where historic CSV data will be loaded."
                      " It may also be a file:// URI")
    subp.set_defaults(func=load_historical_rating)

    subp = subparsers.add_parser('start-sound',
                                 help=start_sound.__doc__)
    subp.add_argument('sound', help="Name of the new OGG sound file")
    subp.set_defaults(func=start_sound)

    subp = subparsers.add_parser('stop-sound',
                                 help=stop_sound.__doc__)
    subp.add_argument('sound', help="Name of the new OGG sound file")
    subp.set_defaults(func=stop_sound)

    subp = subparsers.add_parser('prealarm-sound',
                                 help=prealarm_sound.__doc__)
    subp.add_argument('sound', help="Name of the new OGG sound file")
    subp.set_defaults(func=prealarm_sound)

    args = parser.parse_args(args)
    sys.exit((args.func(args) or 0) if hasattr(args, 'func') else 0)


if __name__ == '__main__':
    main()
