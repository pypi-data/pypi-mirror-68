.. -*- coding: utf-8 -*-
.. :Project:   -- SoL
.. :Created:   mer 25 dic 2013 11:13:02 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2013, 2014, 2015, 2018, 2020 Lele Gaifax
..

.. _gestione campionati:

Gestione campionati
-------------------

.. index::
   pair: Gestione; Campionati

Un *campionato* raggruppa uno o più *tornei*, organizzati dallo stesso *club*, con regole di
gioco omogenee: tutti i tornei di uno stesso campionato sono necessariamente tutti *singoli*
**oppure** a *squadre* e usano il medesimo metodo di assegnazione dei premi finali.

.. contents::


Voci del menu
~~~~~~~~~~~~~

Oltre alle :ref:`azioni standard <pulsanti-standard>` il menu contiene queste voci:

.. figure:: campionati.png
   :figclass: float-right

   Gestione campionati

:guilabel:`Tornei`
  Apre la :ref:`gestione dei tornei <gestione tornei>` organizzati nell'ambito del campionato
  selezionato

:guilabel:`Club`
  Apre la :ref:`gestione dei club <gestione club>` filtrata sul club che organizza il
  campionato selezionato

:guilabel:`Scarica`
  Permette di scaricare i dati di tutti i tornei organizzati nell'ambito del campionato
  selezionato

:guilabel:`Classifica`
  Produce un documento PDF con la classifica del campionato selezionato

:guilabel:`Assegna`
  Assegna la responsabilità dei campionati selezionati: è possibile selezionare uno o più
  campionati tenendo premuto il tasto :kbd:`Ctrl` ed estendere la selezione premendo il tasto
  :kbd:`Shift`


.. _inserimento e modifica campionati:

Inserimento e modifica
~~~~~~~~~~~~~~~~~~~~~~

.. index::
   pair: Inserimento e modifica; Campionato

Club e descrizione
++++++++++++++++++

Ogni campionato appartiene a un particolare :guilabel:`club` e ha una :guilabel:`descrizione`
che deve essere univoca per lo stesso club.

.. _giocatori per squadra:

Giocatori
+++++++++

:guilabel:`Giocatori per squadra` determina il numero massimo di giocatori che compongono un
singolo :ref:`concorrente <pannello concorrenti>`: 1 per i singoli, 2 per il doppio e fino a 4
per i tornei a squadre.

Scarta
++++++

Con :guilabel:`ignora i peggiori risultati` si specifica quanti risultati *peggiori* di ogni
giocatore verranno ignorati nel calcolo della classifica di fine campionato. In genere viene
usato per consentire ai giocatori di non partecipare a **tutte** le tappe di un campionato e di
rimanere comunque in competizione.

.. _campionato partite solitarie:

Partite solitarie
+++++++++++++++++

Di solito lasciato in bianco, se inserito è il numero di partite che dovranno essere giocate da
ciascun partecipante a un :ref:`torneo in solitudine <corona carrom>` associato al campionato.

In questo tipo di tornei, lo *score* di ciascun giocatore viene calcolato dalla *media dei tiri
sbagliati*, cioè dal numero di tiri che *non* imbucano nessuna pedina, nel corso di diverse
partite consecutive.

Quei valori possono essere inseriti come al solito, oppure inseriti direttamente dai giocatori
stessi, usando un modulo che devono compilare alla fine di ciascun turno: ogni volta che il
gestore del torneo genera un nuovo turno, può usare l'azione :guilabel:`Invia email` del
:ref:`pannello incontri <pannello incontri>` (visibile *solo* in questo tipo di tornei) per
spedire a ciascun concorrente una mail con l'URL da visitare.

È chiaramente compito del gestore del torneo controllare che i valori immessi siano corretti:
di tanto in tanto dovrà usare l'azione :guilabel:`Aggiorna` per ricaricare gli incontri, e
quando tutti i punteggi siano stati inseriti correttamente potrà usare l'azione
:guilabel:`Ricalcola classifica` e poi procedere alla generazione del turno successivo.

.. _valutazione campionato:

Valutazione
+++++++++++

La :guilabel:`valutazione` viene usata come valore di default quando si creano nuovi tornei nel
campionato: generalmente, ma non sempre, tutti i tornei di un campionato fanno riferimento ad
una medesima valutazione; è comunque l':ref:`impostazione sul torneo <valutazione torneo>` ad
essere determinante, in quanto può verificarsi che un particolare evento faccia sì parte di un
campionato ma usi una diversa valutazione, ad esempio quando c'è un torneo *open*.

Abbinamenti
+++++++++++

Il :guilabel:`metodo abbinamenti` viene usato come valore di default quando si creano nuovi
tornei nel campionato e determina come verranno create le coppie di avversari ad ogni nuovo
turno (vedi :ref:`sistema di generazione abbinamenti <abbinamenti>` del torneo per i
dettagli).

.. index:: Premi finali

Premi
+++++

Il :guilabel:`metodo premiazione` determina come verranno assegnati i premi finali. Tali premi
hanno due funzioni primarie:

1. uniformare, rendendo quindi `sommabili`, i risultati dei singoli tornei per produrre la
   classifica del campionato

2. essendo di fatto liberamente assegnabili, consentono di invertire la posizione dei primi due
   (o quattro) giocatori qualora l'eventuale `finale` tra il primo e il secondo classificato (e
   tra il terzo e il quarto) dovesse così stabilire

Un caso particolare è il valore ``Nessun premio finale``, che in pratica significa la
premiazione assegnerà semplicemente una sequenza decrescente di numeri interi a cominciare dal
numero di concorrenti fino a 1 come premio finale, solo al fine di consentire l'aggiustamento
delle posizioni in classifica al termine dei turni finali del torneo. Questo premi non
compariranno nella stampa della classifica del torneo. Inoltre, nella classifica del campionato
non verranno considerati i premi finali dei concorrenti, bensì il loro punteggio.

I rimanenti quattro valori identificano altrettanti metodi di generazione dei premi finali:

``Premi fissi``
  assegna 18 punti al primo, 16 al secondo, 14 al terzo, 13 al quarto e così via fino al
  sedicesimo piazzamento;

``40 premi fissi``
  assegna 1000 punti al primo, 900 al secondo, 800 al terzo, 750 al quarto e così via, fino a
  un punto per il quarantesimo classificato;

``Millesimale classico``
  assegna 1000 punti al vincitore e un premio proporzionale a tutti gli altri; in genere è il
  metodo preferito quando il numero di concorrenti è maggiore di 20 o giù di lì;

``Centesimale``
  assegna 100 punti al vincitore, 1 punto all'ultimo classificato, interpolando linearmente il
  premio da assegnare agli altri concorrenti.

.. _campionato concluso:

Concluso
++++++++

Il campo :guilabel:`concluso` indica se il campionato è terminato: in questo caso nessun altro
torneo potrà esservi associato e pertanto il selettore di campionato (ad esempio inserendo
nuovi :ref:`tornei <gestione tornei>`) mostrerà solo quelli ancora attivi.

Campionato precedente
+++++++++++++++++++++

Il campo :guilabel:`campionato precedente` consente di consultare le varie stagioni di
tornei. È possibile selezionare solo campionati *conclusi*.

Responsabile
++++++++++++

Il :guilabel:`responsabile` generalmente indica l'utente che ha inserito quel particolare
campionato: i dati del campionato potranno essere modificati solo da lui (oltre che
dall'*amministratore* del sistema.).
