.. -*- coding: utf-8 -*-
.. :Project:   SoL
.. :Created:   mer 25 dic 2013 11:12:34 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2013, 2014, 2015, 2018, 2020 Lele Gaifax
..

.. _gestione club:

Gestione club
-------------

.. index::
   pair: Gestione; Club

Un *club* è l'entità che organizza uno o più *campionati* di *tornei*. Può anche avere un
elenco di *giocatori* associati.

.. index:: Federazioni nazionali

Un club può anche essere una *federazione nazionale*, che solitamente coordina vari club di un
certo paese. Molto spesso i tornei internazionali vengono ospitati a turno da questa o quella
federazione e in genere è richiesto che i partecipanti a questi tornei siano affiliati a una
particolare federazione.

.. contents::


Voci del menu
~~~~~~~~~~~~~

Oltre alle :ref:`azioni standard <pulsanti-standard>` il menu contiene queste voci:

.. figure:: club.png
   :figclass: float-right

   Gestione club

:guilabel:`Campionati`
  Apre la :ref:`gestione dei campionati <gestione campionati>` organizzati dal club selezionato

:guilabel:`Giocatori`
  Apre la :ref:`gestione dei giocatori <gestione giocatori>` associati al club selezionato

:guilabel:`Scarica`
  Permette di scaricare i dati di tutti i tornei organizzati dal club selezionato

:guilabel:`Assegna`
  Assegna la responsabilità dei club selezionati: è possibile selezionare uno o più
  club tenendo premuto il tasto :kbd:`Ctrl` ed estendere la selezione premendo il tasto
  :kbd:`Shift`

L'amministratore e l'utente responsabile di un club possono trovare una ulteriore azione nel
menu che appare premendo il tasto destro del mouse su un particolare club:

:guilabel:`Utenti`
  Apre la :ref:`gestione associazione utenti di un club <gestione associazione club-utenti>`,
  che permette di selezionare quali altri utenti possono creare altre entità legate al club,
  in particolare nuovi tornei.


Inserimento e modifica
~~~~~~~~~~~~~~~~~~~~~~

.. index::
   pair: Inserimento e modifica; Club

Descrizione
+++++++++++

Ogni club ha una :guilabel:`descrizione` che deve essere univoca: non ci possono essere due
club con la stessa descrizione.

Nazionalità, sito web e email
+++++++++++++++++++++++++++++

Sia :guilabel:`nazionalità`, che :guilabel:`URL del sito web` che :guilabel:`email` sono
facoltativi. Quest'ultimo può essere eventualmente utilizzato per inviare messaggi di posta
elettronica al responsabile del club.

Valutazione
+++++++++++

La :guilabel:`valutazione` viene usata come valore di default quando si creano nuovi campionati
organizzati da questo club: generalmente, ma non sempre, tutti i campionati di un club fanno
riferimento ad una medesima valutazione; è comunque l':ref:`impostazione sul torneo
<valutazione torneo>` ad essere determinante, in quanto può verificarsi che un particolare
evento faccia sì parte di un campionato ma usi una diversa valutazione, ad esempio quando c'è
un torneo *open*.

Federazione
+++++++++++

Un club può essere contrassegnato come :guilabel:`federazione`: per poter partecipare a tornei
internazionali spesso si richiede che il singolo giocatore sia affiliato ad una federazione
nazionale.

Abbinamenti e premiazioni
+++++++++++++++++++++++++

Il :guilabel:`metodo abbinamenti` e il :guilabel:`metodo premiazione` sono usati come valori
di default nella creazione di nuovi campionati organizzati dal club.

Responsabile
++++++++++++

Il :guilabel:`responsabile` generalmente indica l'utente che ha inserito quel particolare club:
i dati del club potranno essere modificati solo da lui (oltre che dall'*amministratore* del
sistema.).

.. _stemma:

Stemma
++++++

Ad ogni club può essere assegnata un'immagine (nei formati ``.png``, ``.jpg`` o ``.gif``)
utilizzata come :guilabel:`stemma` che verrà stampato sulle :ref:`tessere` personali. Sebbene
venga automaticamente scalata alla bisogna, si raccomanda di usare immagini di dimensioni
ragionevoli\ [#]_.

.. [#] Il programma impone un limite di 512Kb, considerando la dimensione dell'immagine
       *grezza*: sebbene dipenda dal browser, solitamente viene convertita nel formato ``PNG``,
       quindi in generale *non* corrisponde a quella dell'immagine originale selezionata.
