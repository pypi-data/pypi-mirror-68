# -*- coding: utf-8 -*-
# :Project:   SoL -- The Player entity
# :Created:   gio 27 nov 2008 13:52:39 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020 Lele Gaifax
#

from base64 import b32encode
from datetime import date
import logging
import re
from zlib import adler32

from pyramid.i18n import make_localizer
from pyramid.interfaces import ILocalizer, ITranslationDirectories
from pyramid_mailer.message import Message
from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Sequence,
    and_,
    exists,
    func,
    or_,
    select,
    )
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import aliased, backref, object_session, relationship
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.sql import union_all

from ..i18n import country_name, gettext, ngettext, translatable_string as _
from . import Base, GloballyUnique, MergedPlayer
from .domains import (
    boolean_t,
    date_t,
    email_t,
    flag_t,
    filename_t,
    intid_t,
    language_t,
    name_t,
    nationality_t,
    nickname_t,
    )
from .errors import OperationAborted
from .utils import normalize


logger = logging.getLogger(__name__)


TRAINING_URL_MESSAGE = _("""\
Hello {firstname},

you are participating to the long-distance “{tourney}” Carrom event.

In the next round you are going to play against {opponent}: following the
rules explained at {baseurl}static/manual/en/solitude.html#corona-carrom
you shall play {nboards} boards, inserting the number of errors in each board in the form
at the following address:

  {url}
{details}
Thanks for playing, happy carromming and stay safe!
""")


class Player(GloballyUnique, Base):
    """A single person."""

    __tablename__ = 'players'
    "Related table."

    @declared_attr
    def __table_args__(cls):
        return (GloballyUnique.__table_args__(cls) +
                (Index('%s_uk' % cls.__tablename__,
                       'lastname', 'firstname', 'nickname',
                       unique=True),))

    ## Columns

    idplayer = Column(
        intid_t, Sequence('gen_idplayer', optional=True),
        primary_key=True,
        nullable=False,
        info=dict(label=_('Player ID'),
                  hint=_('Unique ID of the player.')))
    """Primary key."""

    firstname = Column(
        name_t,
        nullable=False,
        info=dict(label=_('First name'),
                  hint=_('First name of the player.')))
    """Player's first name."""

    lastname = Column(
        name_t,
        nullable=False,
        info=dict(label=_('Last name'),
                  hint=_('Last name of the player.')))
    """Player's last name."""

    nickname = Column(
        nickname_t,
        nullable=False,
        default='',
        info=dict(label=_('Nickname'),
                  hint=_('Nickname of the player, to disambiguate homonyms.')))
    """Player's nickname."""

    sex = Column(
        flag_t,
        info=dict(label=_('Gender'),
                  hint=_('The gender of the player, used to compute different rankings.'),
                  dictionary=dict(F=_('Female'),
                                  M=_('Male'))))
    """Player's gender: ``F`` means *female*, ``M`` means *male*."""

    birthdate = Column(
        date_t,
        info=dict(label=_('Birthdate'),
                  hint=_('Date of birth of the player, needed for “Junior” rankings.')))
    """Date of birth of the player."""

    nationality = Column(
        nationality_t,
        info=dict(label=_('Country'),
                  hint=_('The country the player plays for.')))
    """
    `ISO country code <http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3>`_
    to compute national rankings.
    """

    citizenship = Column(
        boolean_t,
        nullable=False,
        default=True,
        info=dict(label=_('Citizenship'),
                  hint=_('Whether the player belongs legally to the given'
                         ' country or not.')))
    """Whether the player belongs legally to the given country or not."""

    agreedprivacy = Column(
        flag_t,
        nullable=False,
        default=' ',
        info=dict(label=_('Agreed privacy'),
                  hint=_('Whether the player explicitly accepted the privacy policy.'),
                  dictionary={' ': _('Did not say anything yet'),
                              'A': _('Agreed'),
                              'N': _('Did not agree')}))
    """
    Whether the player explicitly accepted the privacy policy: ``A`` means *agreed*, ``N``
    means *did not agree*.

    When left blank, this gets implicitly inferred from whether the person participated to a
    tournament after January 1, 2020.

    His name and other details will be dimmed if he did not agree.
    """

    language = Column(
        language_t,
        info=dict(label=_('Language'),
                  hint=_('The code of the preferred language by the player.')))
    """
    The `ISO code <http://en.wikipedia.org/wiki/ISO_639-1>`_ of the preferred
    language of the player.
    """

    email = Column(
        email_t,
        info=dict(label=_('Email'),
                  hint=_('Email address of the player.')))
    """Email address of the player."""

    idclub = Column(
        intid_t, ForeignKey('clubs.idclub', name='fk_player_club'),
        info=dict(label=_('Club ID'),
                  hint=_('ID of the club the player is member of.')))
    """Membership club's ID."""

    idfederation = Column(
        intid_t, ForeignKey('clubs.idclub', name='fk_player_federation'),
        info=dict(label=_('Federation ID'),
                  hint=_('ID of the federation the player is associated with.')))
    """Membership federation's ID."""

    portrait = Column(
        filename_t,
        info=dict(label=_('Portrait'),
                  hint=_('File name of the PNG, JPG or GIF portrait of the player.')))
    """
    Picture of the player, used by lit.

    This is just the filename, referencing a picture inside the
    ``sol.portraits_dir`` directory.
    """

    idowner = Column(
        intid_t, ForeignKey('users.iduser', use_alter=True, name='fk_player_owner',
                            ondelete="SET NULL"),
        info=dict(label=_('Owner ID'),
                  hint=_('ID of the user that is responsible for this record.')))
    """ID of the :py:class:`user <.User>` that is responsible for this record."""

    ## Relations

    merged = relationship('MergedPlayer', backref='player',
                          cascade="all, delete-orphan")
    """A possibly empty list of ``MergedPlayer`` that has been merged into this one."""

    owner = relationship('User', backref=backref('owned_players'))
    """The :py:class:`owner <.User>` of this record, `admin` when ``None``."""

    @classmethod
    def find(klass, session, lastname, firstname, nickname, guid=None):
        """Find a player, even after it has been merged into another.

        :param session: an SQLAlchemy session
        :param lastname: a string, the last name of the player
        :param firstname: a string, the first name of the player
        :param nickname: a string, the nick name of the player
        :param guid: the hex string of an UUID
        :rtype: a tuple

        This tries to find the given player by looking for it first in the ``players``
        table then in the ``merged_players`` table, either by `guid` or by name.

        If found, it returns a tuple with the **current** player (that is, the eventual target
        of the merge) and a boolean flag, ``False`` when it is current or ``True`` if it has
        been merged.

        If not found it returns a ``(None, False)`` tuple.
        """

        query = session.query
        merged_into = False
        player = None

        if guid is not None:
            player = query(klass).filter_by(guid=guid).one_or_none()
            if player is None:
                merged_into = query(MergedPlayer).filter_by(guid=guid).one_or_none()
                if merged_into is not None:
                    player = merged_into.player

        kwargs = None
        if player is None:
            kwargs = dict(firstname=firstname, lastname=lastname)
            if nickname is not None:
                kwargs['nickname'] = nickname
            player = query(klass).filter_by(**kwargs).one_or_none()

        if player is None:
            merged_into = query(MergedPlayer).filter_by(**kwargs).one_or_none()
            if merged_into is not None:
                player = merged_into.player

        return player, bool(merged_into)

    @classmethod
    def check_insert(klass, session, fields, user_id):
        "Prevent duplicated players."

        from .club import Club, clubusers

        try:
            lname = normalize(fields['lastname'])
            fname = normalize(fields['firstname'])
        except KeyError:
            raise OperationAborted(_('For a new player both the "firstname"'
                                     ' and the "lastname" fields are mandatory'))

        if not lname or not fname:
            raise OperationAborted(_('For a new player both the "firstname"'
                                     ' and the "lastname" fields are mandatory'))

        nname = fields.get('nickname')
        if nname:
            nname = nname.strip()

        try:
            existing, merged = klass.find(session, lname, fname, nname)
        except MultipleResultsFound:  # pragma: no cover
            if not nname:
                raise OperationAborted(
                    _('There are other players named «$lname $fname», please double check'
                      ' and if it is effectively correct (that is, he is a different person),'
                      ' specify a different nickname to disambiguate',
                      mapping=dict(lname=lname, fname=fname)))
            else:
                existing = None

        if existing is not None:
            if merged:
                raise OperationAborted(
                    _('It seems that «$lname $fname» is a bad spelling of «$newname»: please'
                      ' double check and if it is effectively correct (that is, he is a'
                      ' different person), specify a different nickname to disambiguate',
                      mapping=dict(lname=lname, fname=fname, newname=existing.description)))
            else:
                if not nname:
                    raise OperationAborted(
                        _('A player named «$name» is already present: please double check'
                          ' and if the new player is effectively a different person'
                          ' specify a nickname to disambiguate',
                          mapping=dict(name=existing.description)))
                elif nname == existing.nickname:
                    raise OperationAborted(
                        _('A player named «$name» is already present: please double check'
                          ' and if the new player is effectively a different person'
                          ' specify a different nickname to disambiguate',
                          mapping=dict(name=existing.description)))

        if user_id != 'admin':
            idclub = fields.get('idclub')
            clubs = Club.__table__
            if idclub is not None:
                if not session.scalar(select([True])
                                      .where(or_(
                                          exists()
                                          .where(clubs.c.idclub == idclub)
                                          .where(clubs.c.idowner == user_id),
                                          exists()
                                          .where(clubusers.c.idclub == idclub)
                                          .where(clubusers.c.iduser == user_id)))):
                    raise OperationAborted(_('You are not allowed to add a player to the'
                                             ' selected club'))

            idclub = fields.get('idfederation')
            if idclub is not None:
                if not session.scalar(select([True])
                                      .where(or_(
                                          exists()
                                          .where(clubs.c.idclub == idclub)
                                          .where(clubs.c.idowner == user_id),
                                          exists()
                                          .where(clubusers.c.idclub == idclub)
                                          .where(clubusers.c.iduser == user_id)))):
                    raise OperationAborted(_('You are not allowed to add a player to the'
                                             ' selected federation'))

    def check_update(self, fields):
        "Perform any check before updating the instance."

        if 'lastname' in fields:
            lname = normalize(fields['lastname'])
            if not lname:
                raise OperationAborted(_('The "lastname" field of a player cannot be empty'))

        if 'firstname' in fields:
            fname = normalize(fields['firstname'])
            if not fname:
                raise OperationAborted(_('The "firstname" field of a player cannot be empty'))

    def delete(self):
        "Prevent deletion if this player is involved in some tourney."

        from . import Competitor

        sess = object_session(self)

        ct = Competitor.__table__
        tourneys = sess.execute(select([ct.c.idtourney],
                                       or_(ct.c.idplayer1 == self.idplayer,
                                           ct.c.idplayer2 == self.idplayer,
                                           ct.c.idplayer3 == self.idplayer,
                                           ct.c.idplayer4 == self.idplayer))
                                .distinct()).fetchall()
        nt = len(tourneys)
        if nt > 0:
            raise OperationAborted(ngettext(
                'Deletion not allowed: $player is a competitor in $count tourney!',
                'Deletion not allowed: $player is a competitor in $count tourneys!',
                nt, mapping=dict(player=self.description, count=nt)))

        super().delete()

    @property
    def country(self):
        "The name of the player's country."

        return country_name(self.nationality)

    def shouldOmitNickName(self, _non_word_letters=re.compile(r'\W')):
        "Determine if the nickname should be omitted because redundant."

        if self.nickname:
            # Nickname is used also for login purposes: don't insert it in the description if
            # it's the same (ignoring case) as the first or last name of the player, or if
            # if it's the common combinations of one of those plus the first letter of the
            # other
            nnlower = self.nickname.lower()

            fnlower = self.firstname.lower()
            lnlower = self.lastname.lower()

            cases = [fnlower, lnlower]

            cases.append(fnlower + lnlower[0])
            cases.append(lnlower[0] + fnlower)
            cases.append(lnlower + fnlower[0])
            cases.append(fnlower[0] + lnlower)

            if _non_word_letters.search(fnlower) or _non_word_letters.search(lnlower):
                fnlower = _non_word_letters.sub('', fnlower)
                lnlower = _non_word_letters.sub('', lnlower)
                cases.append(fnlower + lnlower[0])
                cases.append(lnlower[0] + fnlower)
                cases.append(lnlower + fnlower[0])
                cases.append(fnlower[0] + lnlower)

            if nnlower not in cases:
                return False
        return True

    def acceptedDiscernibility(self):
        """Determine whether the player's name should be obfuscated or not.

        The player may have already explicitly stated his privacy policy agreement, and in such
        case we honor his will, showing the full name only when he agrees.

        Otherwise, we check if he participated to any tournaments after January 1, 2020: if so,
        assume he implicitly accepted the common clause that requires one to agree in order to
        play in public tourneys.
        """

        from . import Competitor, Tourney

        explicitly_agreed = self.agreedprivacy

        if explicitly_agreed == ' ':
            agreed = getattr(self, '_implicitly_agreed', None)

            if agreed is None:
                sess = object_session(self)

                ct = Competitor.__table__
                tt = Tourney.__table__
                pid = self.idplayer

                q = (select([True])
                     .where(exists(from_obj=ct.join(tt))
                            .where(or_(ct.c.idplayer1 == pid,
                                       ct.c.idplayer2 == pid,
                                       ct.c.idplayer3 == pid,
                                       ct.c.idplayer4 == pid))
                            .where(tt.c.date >= date(2020, 1, 1))))

                agreed = self._implicitly_agreed = bool(sess.scalar(select([q])))

            return agreed
        else:
            return explicitly_agreed == 'A'

    def _obfuscate(self, name):
        if not name:
            return name

        if self.guid:
            random_seed = self.guid.encode('ascii')
        else:
            random_seed = b'%d' % id(self)
        a32 = adler32(name.encode('ascii', errors='xmlcharrefreplace') + random_seed)
        suffix = b32encode(a32.to_bytes(4, 'little')).rstrip(b'=').decode('ascii')
        return name[0] + suffix.lower()

    @property
    def obfuscatedFirstname(self):
        return self._obfuscate(self.firstname)

    @property
    def obfuscatedLastname(self):
        return self._obfuscate(self.lastname)

    @property
    def obfuscatedNickname(self):
        return self._obfuscate(self.nickname)

    def __repr__(self):
        "Return a representation of the entity, mostly for debugging and log purposes."

        return '<%s "%s">' % (self.__class__.__name__,
                              self.caption(html=False, localized=False, ignore_privacy=True))

    def caption(self, html=None, localized=True, css_class=None, ignore_privacy=False):
        "Description of the player, made up concatenating his names."

        if not ignore_privacy:
            sas = object_session(self)
            if ((sas is not None and sas.info.get('ignore_privacy')
                 or self.acceptedDiscernibility())):
                ignore_privacy = True

        if ignore_privacy:
            lastname = self.lastname
            firstname = self.firstname
            nickname = self.nickname
        else:
            lastname = self.obfuscatedLastname
            firstname = self.obfuscatedFirstname
            nickname = self.obfuscatedNickname

        if nickname == '' or self.shouldOmitNickName():
            nickname = ''
            if html is None or html:
                format = _('<b>$lastname</b> $firstname')
            else:
                format = _('$lastname $firstname')
        else:
            nickname = '“%s”' % nickname
            if html is None or html:
                format = _('<b>$lastname</b> $firstname $nickname')
            else:
                format = _('$lastname $firstname $nickname')

        result = gettext(format, just_subst=not localized,
                         mapping=dict(lastname=lastname, firstname=firstname,
                                      nickname=nickname))
        if (html is None or html) and css_class:
            result = '<span class="%s">%s</span>' % (css_class, result)
        return result

    description = property(caption)

    def mergePlayers(self, other_players, clogger=None):
        """Merge multiple players into a single one.

        :param other_players: a sequence of players ids or guids, or tuples like
                              ``(guid, lastname, firstname, nickname)``
        :rtype: a list of replaced players descriptions

        This will replace the specified players with this one wherever
        they participated to a game, either in singles or team events.

        This is obviously possible only when the specified players didn't
        play together in any tourney.

        The old names are stored in the table ``merged_players`` with a reference to the
        current player (that is, `self`), so that they can be correctly resolved in the future.
        """

        from . import Competitor, Rate
        from .utils import njoin

        if clogger is None:
            from .bio import changes_logger as clogger

        s = object_session(self)
        merged_guids = set()
        merged_names = set()
        for m in self.merged:
            merged_guids.add(m.guid)
            merged_names.add((m.lastname, m.firstname, m.nickname))

        mpt = MergedPlayer.__table__
        pt = self.__table__
        other_ids = []
        for other_player in other_players:
            if isinstance(other_player, (tuple, list)):
                id_or_guid = other_player[0]
            else:
                id_or_guid = other_player

            if isinstance(id_or_guid, str):
                # Is it already merged?
                if id_or_guid in merged_guids:
                    continue

                midr = s.execute(select([pt.c.idplayer])
                                 .where(pt.c.guid == id_or_guid)).first()
                if midr is None:
                    # The merged player is not present in the db: this
                    # is the case when we are loading a backup, so no
                    # check is needed, just take note of the fact

                    already_merged = s.execute(select([mpt.c.idmergedplayer])
                                               .where(mpt.c.guid == id_or_guid)).first()
                    if already_merged is not None:  # pragma: nocover
                        # We already know she's been merged
                        continue

                    if isinstance(other_player, (tuple, list)):
                        lastname, firstname, nickname = other_player[1:]
                        if (lastname, firstname, nickname) in merged_names:  # pragma: nocover
                            continue

                        s.add(MergedPlayer(guid=id_or_guid,
                                           lastname=lastname,
                                           firstname=firstname,
                                           nickname=nickname,
                                           player=self))
                    else:
                        s.add(MergedPlayer(guid=id_or_guid, player=self))
                else:
                    other_ids.append(midr[0])
            else:
                mp = s.query(Player).get(id_or_guid)
                if mp is None or mp.guid in merged_guids:  # pragma: nocover
                    continue
                other_ids.append(id_or_guid)

        if not other_ids:
            return

        # Load all competitors referencing any of the source players
        ctors = s.query(Competitor).filter(
            or_(Competitor.idplayer1.in_(other_ids),
                Competitor.idplayer2.in_(other_ids),
                Competitor.idplayer3.in_(other_ids),
                Competitor.idplayer4.in_(other_ids))).all()

        # Collect the single tourneys
        tourneys = set([c.tourney for c in ctors])
        sourceids = set(other_ids)

        for t in tourneys:
            # Target player must not be present in any of the tourneys
            allplayers = set([p.idplayer for p in t.allPlayers()])
            if self.idplayer in allplayers:
                raise OperationAborted(_('Cannot merge given people'
                                         ' because "$player" is present in'
                                         ' tourney "$tourney"',
                                         mapping=dict(player=self.description,
                                                      tourney=t.description)))

            # There cannot be a tourney where two or more of the source
            # players are present
            count = len(allplayers & sourceids)
            if count > 1:
                raise OperationAborted(_('Cannot merge given people'
                                         ' because $count of them are'
                                         ' playing in tourney "$tourney"',
                                         mapping=dict(count=count,
                                                      tourney=t.description)))

        # Ok, replace 'em
        for c in ctors:
            if c.idplayer1 in other_ids:
                c.player1 = self
            elif c.idplayer2 is not None and c.idplayer2 in other_ids:  # pragma: nocover
                c.player2 = self
            elif c.idplayer3 is not None and c.idplayer3 in other_ids:  # pragma: nocover
                c.player3 = self
            elif c.idplayer4 is not None and c.idplayer4 in other_ids:  # pragma: nocover
                c.player4 = self

        # Update rates too
        s.query(Rate).filter(Rate.idplayer.in_(other_ids)).update({"idplayer": self.idplayer},
                                                                  synchronize_session=False)

        # Finally remove 'em, taking note of the merged guids
        replaced = []
        for i in sourceids:
            p = s.query(Player).get(i)

            already_merged = s.execute(select([mpt.c.idmergedplayer])
                                       .where(mpt.c.guid == p.guid)
                                       .where(mpt.c.idplayer == self.idplayer)).first()
            if already_merged is not None:  # pragma: nocover
                continue

            m = MergedPlayer(guid=p.guid,
                             lastname=p.lastname,
                             firstname=p.firstname,
                             nickname=p.nickname,
                             player=self)
            s.add(m)

            # If he was already a target of a merge, relink to this player
            s.query(MergedPlayer).filter_by(idplayer=p.idplayer) \
                                 .update({"idplayer": self.idplayer},
                                         synchronize_session=False)

            for f in ('sex', 'birthdate', 'nationality', 'citizenship',
                      'language', 'email', 'idclub', 'idfederation', 'portrait'):
                if getattr(self, f) is None:
                    mv = getattr(p, f)
                    if mv is not None:
                        setattr(self, f, mv)

            s.flush()

            replaced.append(p.caption(False, localized=False))
            s.delete(p)

        clogger.info('Player%s %s has been merged into %r',
                     '' if len(replaced) == 1 else 's',
                     njoin(replaced, localized=False),
                     self)

        self.modified = func.now()

        return replaced

    def participations(self):
        "Return the list of :py:class:`competitors <.Competitor>` involving this player."

        from . import Competitor

        s = object_session(self)

        ctors = s.query(Competitor).filter(
            or_(Competitor.idplayer1 == self.idplayer,
                Competitor.idplayer2 == self.idplayer,
                Competitor.idplayer3 == self.idplayer,
                Competitor.idplayer4 == self.idplayer)).all()
        ctors.sort(key=lambda c: c.tourney.date)
        return ctors

    def matchesSummary(self):
        "Return the number of won, lost, tied and single matches."

        from . import Competitor, Match

        s = object_session(self)

        ct1 = Competitor.__table__.alias()
        ct2 = Competitor.__table__.alias()
        mt = Match.__table__.alias()

        wins = 0
        losts = 0
        ties = 0
        singles = 0

        qm = union_all(
            select([mt.c.score1, mt.c.score2,
                    ct1.c.idplayer2, ct1.c.idplayer3, ct1.c.idplayer4,
                    ct2.c.idplayer2, ct2.c.idplayer3, ct2.c.idplayer4],
                   or_(ct1.c.idplayer1 == self.idplayer,
                       ct1.c.idplayer2 == self.idplayer,
                       ct1.c.idplayer3 == self.idplayer,
                       ct1.c.idplayer4 == self.idplayer),
                   from_obj=mt
                   .join(ct1, mt.c.idcompetitor1 == ct1.c.idcompetitor)
                   .join(ct2, mt.c.idcompetitor2 == ct2.c.idcompetitor)),
            select([mt.c.score2, mt.c.score1,
                    ct1.c.idplayer2, ct1.c.idplayer3, ct1.c.idplayer4,
                    ct2.c.idplayer2, ct2.c.idplayer3, ct2.c.idplayer4],
                   or_(ct2.c.idplayer1 == self.idplayer,
                       ct2.c.idplayer2 == self.idplayer,
                       ct2.c.idplayer3 == self.idplayer,
                       ct2.c.idplayer4 == self.idplayer),
                   from_obj=mt
                   .join(ct1, mt.c.idcompetitor1 == ct1.c.idcompetitor)
                   .join(ct2, mt.c.idcompetitor2 == ct2.c.idcompetitor)))

        for m in s.execute(qm):
            if m[0] > m[1]:
                wins += 1
            elif m[0] == m[1]:
                ties += 1
            else:
                losts += 1
            if m[2] is m[3] is m[4] is m[5] is m[6] is m[7] is None:
                singles += 1

        return (wins, losts, ties, singles)

    def opponents(self):
        "Return a summary of the opponents this player met, in singles."

        from . import Competitor, Match

        s = object_session(self)

        ct1 = Competitor.__table__.alias()
        ct2 = Competitor.__table__.alias()
        mt = Match.__table__.alias()

        qm = union_all(
            select([ct2.c.idplayer1, mt.c.score1, mt.c.score2],
                   and_(ct1.c.idplayer1 == self.idplayer,
                        ct1.c.idplayer2 == None,
                        ct2.c.idplayer2 == None,
                        (or_(mt.c.score1 != 0, mt.c.score2 != 0))),
                   from_obj=mt
                   .join(ct1, mt.c.idcompetitor1 == ct1.c.idcompetitor)
                   .join(ct2, mt.c.idcompetitor2 == ct2.c.idcompetitor)),
            select([ct1.c.idplayer1, mt.c.score2, mt.c.score1],
                   and_(ct2.c.idplayer1 == self.idplayer,
                        ct1.c.idplayer2 == None,
                        ct2.c.idplayer2 == None,
                        (or_(mt.c.score1 != 0, mt.c.score2 != 0))),
                   from_obj=mt
                   .join(ct1, mt.c.idcompetitor1 == ct1.c.idcompetitor)
                   .join(ct2, mt.c.idcompetitor2 == ct2.c.idcompetitor)))

        summary = {}

        for m in s.execute(qm):
            opponent, ps, os = m
            data = summary.setdefault(opponent, [0, 0, 0, 0, 0])
            if ps > os:
                data[0] += 1
            elif ps < os:
                data[1] += 1
            else:
                data[2] += 1
            data[3] += ps
            data[4] += os

        result = [(s.query(Player).get(o), d[0], d[1], d[2], d[3], d[4])
                  for o, d in summary.items()]

        return sorted(result,
                      key=lambda i: (-(i[1] + i[2] + i[3]), i[0].lastname, i[0].firstname))

    def opponentMatches(self, opponent):
        "Return the list of :py:class:`matches <.Match>` against the `opponent`."

        from . import Competitor, Match

        s = object_session(self)
        c1 = aliased(Competitor)
        c2 = aliased(Competitor)

        matches = (s.query(Match)
                   .join(c1, Match.idcompetitor1 == c1.idcompetitor)
                   .join(c2, Match.idcompetitor2 == c2.idcompetitor)
                   .filter(or_(Match.score1 != 0, Match.score2 != 0))
                   .filter(or_(and_(c1.idplayer1 == self.idplayer,
                                    c1.idplayer2 == None,
                                    c2.idplayer1 == opponent.idplayer,
                                    c2.idplayer2 == None),
                               and_(c1.idplayer1 == opponent.idplayer,
                                    c1.idplayer2 == None,
                                    c2.idplayer1 == self.idplayer,
                                    c2.idplayer2 == None)))).all()

        return sorted(matches, key=lambda m: m.tourney.date)

    _FORCE_DISCERNABILITY = False
    _FORCE_PRIVACY_AGREEMENT_FOR_SERIALIZATION_TESTS = False

    def serialize(self, serializer):
        """Reduce a single player to a simple dictionary.

        :param serializer: a :py:class:`.Serializer` instance
        :rtype: dict
        :returns: a plain dictionary containing a flatified view of this player
        """

        if self._FORCE_DISCERNABILITY or self.acceptedDiscernibility():
            lastname = self.lastname
            firstname = self.firstname
            nickname = self.nickname
        else:
            lastname = self.obfuscatedLastname
            firstname = self.obfuscatedFirstname
            nickname = self.obfuscatedNickname

        simple = {}
        simple['guid'] = self.guid
        simple['modified'] = self.modified
        simple['firstname'] = firstname
        simple['lastname'] = lastname
        if nickname:
            simple['nickname'] = nickname
        if self.sex:
            simple['sex'] = self.sex
        if self.nationality:
            simple['nationality'] = self.nationality
        if self.language:
            simple['language'] = self.language
        if not self.citizenship:
            simple['citizenship'] = self.citizenship
        if self._FORCE_PRIVACY_AGREEMENT_FOR_SERIALIZATION_TESTS:
            simple['agreedprivacy'] = 'A'
        else:
            simple['agreedprivacy'] = self.agreedprivacy
        if self.portrait:
            simple['portrait'] = self.portrait
        if self.email:
            simple['email'] = self.email
        if self.birthdate:
            simple['birthdate'] = self.birthdate
        if self.idclub:
            simple['club'] = serializer.addClub(self.club)
        if self.idfederation:
            simple['federation'] = serializer.addClub(self.federation)
        if self.idowner:
            simple['owner'] = serializer.addUser(self.owner)

        merged = self.merged
        if merged:
            simple['merged'] = [(m.guid, m.lastname, m.firstname, m.nickname)
                                for m in merged]

        return simple

    def sendTrainingURL(self, request, match, cnum, opponent):
        language = self.language or request.registry.settings['default_locale_name']
        loc = request.registry.queryUtility(ILocalizer, name=language)
        if loc is None:
            tdirs = request.registry.queryUtility(ITranslationDirectories, default=[])
            loc = make_localizer(language, tdirs)
        t = loc.translate
        oname = t(opponent.caption(html=False, ignore_privacy=True))
        nboards = match.tourney.championship.trainingboards
        if match.tourney.socialurl:
            details = "\n" + t(_('Remember to upload your video on ${socialurl}',
                                 mapping=dict(socialurl=match.tourney.socialurl))) + "\n"
        else:
            details = ""
        url = match.getEditCompetitorURL(request, cnum)
        body = t(TRAINING_URL_MESSAGE).format(firstname=self.firstname,
                                              baseurl=request.route_url('app'),
                                              tourney=match.tourney.description,
                                              opponent=oname, nboards=nboards,
                                              url=url, details=details)
        message = Message(subject=t(_('Your next SoLitude-Carrom match')),
                          recipients=[self.email],
                          body=body)
        request.mailer.send(message)
        logger.debug('Sent self-edit link to %r: %s', self, url)
