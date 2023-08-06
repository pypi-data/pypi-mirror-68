#!/bin/bash
# -*- coding: utf-8 -*-
# :Project:   SoL -- Docker entry point script
# :Created:   mer 30 mar 2016 21:34:31 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2018 Lele Gaifax
#

set -e

cmd=$1
shift

case $cmd in
    start)
        echo "Starting SoL server..."
        exec pserve /srv/data/config.ini
        ;;

    shell)
        echo "Starting interactive shell, Ctrl-D to terminate..."
        /bin/bash
        ;;

    initialize-db | upgrade-db)
        echo "Performing $cmd..."
        exec soladmin $cmd /srv/data/config.ini
        ;;

    restore | backup)
        echo "Performing $cmd $@..."
        exec soladmin $cmd /srv/data/config.ini "$@"
        ;;

    change-admin)
        exec soladmin update-config --admin ask --password ask --alembic-dir /usr/src/sol/alembic /srv/data/config.ini
        ;;

    *)
        echo "Could not recognize \"$cmd\" as a command!"
        echo "Valid commands are:"
        echo "  change-admin"
        echo "     change admin credentials"
        echo "  start"
        echo "     start the SoL server"
        echo "  shell"
        echo "     execute an interactive shell"
        echo "  initialize-db"
        echo "     initialize the database structure"
        echo "  upgrade-db"
        echo "     upgrade the database structure"
        echo "  restore [location]"
        echo "     load data from remote SoL server"
        echo "  backup [location]"
        echo "     perform a backup of current database content"
        ;;
esac
