.. -*- coding: utf-8 -*-
.. :Project:   SoL -- Changelog of version 3
.. :Created:   ven 27 lug 2018 17:43:50 CEST
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2018 Lele Gaifax
..

Changelog of version 3
----------------------

3.40 (unreleased)
~~~~~~~~~~~~~~~~~

* Immediately show the edit window when replicating a tourney (suggested by Daniele)


3.39 (2017-03-16)
~~~~~~~~~~~~~~~~~

* Re-release to workaround a `buildout issue`__ with non-normalized requirements

__ https://github.com/buildout/buildout/issues/317


3.38 (2017-03-16)
~~~~~~~~~~~~~~~~~

* Do not allow deletion of players who are responsible of something

* Prevent silly cycle between championships

* Fix translation of player's name in the matches panel


3.37 (2016-08-03)
~~~~~~~~~~~~~~~~~

* Tweak the layout of the "boards" view to make it more readable expecially for team events

* Allow manual re-pairing of any round, not just the first

* Prevent insertion of "empty" names and descriptions


3.36 (2016-06-21)
~~~~~~~~~~~~~~~~~

* Allow removal of the player's nickname (reported by Daniele)

* Fix scorecards printout, avoiding final page full of empty scorecards (thanks again to
  Daniele)

* Take into account merged players when serving the lit pages to Google

* New lit page listing players associated to a particular club


3.35 (2016-06-08)
~~~~~~~~~~~~~~~~~

* The default filter on players subscription now shows only those who played at least one
  tourney organized by the current club in the last year (see `issue 12`__)

* Workaround to overly caching behaviour on some browsers

__ https://bitbucket.org/lele/sol/issues/12/more-effective-way-of-filtering-potential


3.34 (2016-05-31)
~~~~~~~~~~~~~~~~~

* The local IP address of the machine running SoL will be displayed on the console when the
  instance starts, when possible

* Print "page X of Y" on all printouts (asked by Daniele)

* Reduce waste of paper filling the last scorecards printout page with blank cards (asked by
  Daniele)


3.33 (2016-05-29)
~~~~~~~~~~~~~~~~~

* Show an hyperlinked QRCode on the header of most printouts that opens the corresponding Lit
  page

* When a round is playing, show a link to the countdown on the tourney's Lit page


3.32 (2016-05-15)
~~~~~~~~~~~~~~~~~

* Reimplement the `clock` window with a new `pre-countdown`, to be shown while preparing the
  next round (see `issue 11`__)

__ https://bitbucket.org/lele/sol/issues/11/new-ideas-for-the-clock


3.31 (2016-04-26)
~~~~~~~~~~~~~~~~~

* Re-release due to PyPI fault


3.30 (2016-04-26)
~~~~~~~~~~~~~~~~~

* New "all" pairing method, to allow playing tournaments with less than eight competitors
  without occasional show-stoppers


3.29 (2016-04-19)
~~~~~~~~~~~~~~~~~

* Disallow reorder on the matches panel while user is inserting scores

* Don't show competitor's rate when there is not associated rating


3.28 (2016-04-01)
~~~~~~~~~~~~~~~~~

* Add a ``--data-dir`` option to ``soladmin create-config`` to specify a different location of
  persistent state

* Recommend Python 3.5

* Initial&incomplete Docker image setup: needs further documentation and some helper tools


3.27 (2016-03-23)
~~~~~~~~~~~~~~~~~

* Fix problem that prevented loading SoL 2 dumps containing a tourney associated with old
  championship

* In the matches panel, highlight the winning competitor


3.26 (2016-02-16)
~~~~~~~~~~~~~~~~~

* ``soladmin create-config`` and ``soladmin update-config`` can change the name and the
  password of the super user

* The final badges show the player's points, bucholz and netscore


3.25 (2015-12-06)
~~~~~~~~~~~~~~~~~

* Now the admin password can be passed as an option to ``soladmin create-config``

* Request JSON format backup in ``soladmin restore`` (**N.B.**: this requires that the remote
  server is at least at version 3.23)


3.24 (2015-12-01)
~~~~~~~~~~~~~~~~~

* Fix translation glitch


3.23 (2015-12-01)
~~~~~~~~~~~~~~~~~

* Faster alternative JSON-based dumps and backups, the default is still YAML though

* Always use the serial pairing method when there are less than eight competitors


3.22 (2015-11-27)
~~~~~~~~~~~~~~~~~

* Re-release due to PyPI fault


3.21 (2015-11-27)
~~~~~~~~~~~~~~~~~

* Refresh package dependencies


3.20 (2015-06-07)
~~~~~~~~~~~~~~~~~

* New menu action to assign ownership of multiple records at once

* New "owners admin" permission to permit normal users to adjust ownership of everything


3.19 (2015-05-26)
~~~~~~~~~~~~~~~~~

* Fix URL generation when filtering active players

* Do not fail badly when trying to merge players while importing data

* Handle the case of retired players, while recomputing the rating


3.18 (2015-04-04)
~~~~~~~~~~~~~~~~~

* Handle the "around midnight" case when asking the estimated start time

* Fix a long standing bug with dictionary-based field editors


3.17 (2015-03-22)
~~~~~~~~~~~~~~~~~

* Fix the ordering used to compute the next round when delay of top players pairing is disabled

* Ask the estimated start time when printing the scorecards

* Quicker interaction with the grid filters when adding players to a tournament


3.16 (2015-02-28)
~~~~~~~~~~~~~~~~~

* Allow rectification of any round results

* Fix visualization of notification windows


3.15 (2015-02-20)
~~~~~~~~~~~~~~~~~

* Fix default values in several places

* Rectify assignment of highest numbered board to phantom matches

* Use single click to edit values when entering scores and final bounties

* Show the actual rank used to compute the next turn


3.14 (2015-01-21)
~~~~~~~~~~~~~~~~~

* Fix distribution, including the new robots.txt file


3.13 (2015-01-20)
~~~~~~~~~~~~~~~~~

* Use the OGG format instead of MP3 for the sound files

* Fix tourney replication

* Always assign the highest numbered board to phantom matches


3.12 (2014-12-24)
~~~~~~~~~~~~~~~~~

* Integrate the initial French translation, thanks to Stéphane Cano

* Fix visibility of buttons after deletion of final round

* Use "bounty" instead of "final prize", hopefully reducing confusion


3.11 (2014-12-06)
~~~~~~~~~~~~~~~~~

* Fix import of championships chain

* Workaround to an annoying bug in ExtJS 4.2.1 grid TAB handling

* Fix strange problem with logout quickly followed by a new login (experienced by Elisa)

* Add missing article related to the Queen to the italian rules (reported by Daniele)


3.10 (2014-11-21)
~~~~~~~~~~~~~~~~~

* Fix ratings modelization that prevented database dumps

* Rectify opponents matches Lit page, showing only direct matches


3.9 (2014-11-08)
~~~~~~~~~~~~~~~~

* Fix glitch in victories computation in the wins trend chart


3.8 (2014-11-08)
~~~~~~~~~~~~~~~~

* Allow to restrict rating usage to a single club

* Add player's opponents summaries to the Lit interface


3.7 (2014-10-19)
~~~~~~~~~~~~~~~~

* Fix matches panel title, when focusing on a single competitor

* Properly populate the responsible field when showing duplicated players

* Disallow merging of not owned players


3.6 (2014-09-13)
~~~~~~~~~~~~~~~~

* Raise the pageSize parameter of the Board view to 999


3.5 (2014-09-12)
~~~~~~~~~~~~~~~~

* Do not show "my" items shortcuts for the guest user


3.4 (2014-09-11)
~~~~~~~~~~~~~~~~

* Fix localization issues related to reloading the translations catalog, when the user's
  language is different from the browser's default

* Fix ranking printouts, widening the prize column

* Omit the QRCode after more than three days since the event's date

* New actions to easily open tourney's championship and championship's club


3.3 (2014-09-10)
~~~~~~~~~~~~~~~~

* Add a QRCode on the first page of some printouts, pointing to the "equivalent" Lit page

* Minor tweaks to the font sizes of the personal badges printout


3.2 (2014-09-07)
~~~~~~~~~~~~~~~~

* Filter out future tourneys by default, to avoid confusion

* Change the "asis" prizing method: it now assigns a decreasing sequence of integer numbers

* New "centesimal" prizing method: similar to the millesimal, but starting from 100

* New variant of top level windows, showing "my" items, launched by shortcuts on the desktop


3.1 (2014-09-04)
~~~~~~~~~~~~~~~~

* Protect the clock against accidental stops

* Store the timestamp of the countdown start in the database

* Reset the filters when showing possibly duplicated players

* Handle tournament finals, either simple ones or "best of three" matches

* Parametrize the delay of top players pairing


3.0 (2014-08-31)
~~~~~~~~~~~~~~~~

* Tiny fix to the italian translation catalog

* Final 3.0 release, at last!
