.. -*- coding: utf-8 -*-
.. :Project:   SoL
.. :Created:   mer 25 dic 2013 12:19:30 CET
.. :Author:    Lele Gaifax <lele@metapensiero.it>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2013, 2014, 2015, 2016, 2018, 2020 Lele Gaifax
..

.. _gestione torneo:

Gestione torneo
===============

.. figure:: torneo.png

   Gestione torneo

Il cuore dell'applicazione è in questa finestra, composta da quattro *pannelli*.

Sulla sinistra ci sono i `concorrenti`_, dove possono essere inseriti nuovi giocatori, ritirati
quelli presenti oppure organizzati in squadre se :guilabel:`giocatori per squadra` del
:ref:`campionato <giocatori per squadra>` è maggiore di 1 (è possibile farlo solo al primo
turno).

Sulla destra c'è il pannello con la classifica_ attuale.
.. , possibilmente raggruppata per nazionalità.

In basso c'è una vista che consente di :ref:`cambiare manualmente <ricombinazione manuale>` gli
abbinamenti di un nuovo turno generati automaticamente: generalmente questo è necessario solo
per il primo turno, ma *se sai quello che stai facendo* è possibile modificare le combinazioni
di qualsiasi nuovo turno tenendo premuto il tasto :kbd:`ALT` mentre si clicca sul pulsante di
espansione del pannello.

Lo spazio rimanente al centro è dedicato agli incontri_.

I tre pannelli ai bordi possono essere minimizzati, massimizzando così lo spazio disponibile
per gli incontri_. In particolare, il pannello di sinistra e quello in basso vengono usati solo
subito prima e immediatamente dopo la creazione del primo turno, e pertanto vengono minimizzati
automaticamente.

.. _pannello concorrenti:

.. figure:: concorrenti_1.png
   :figclass: float-right

   Pannello concorrenti

Concorrenti
-----------

Questo pannello viene usato principalmente quando si comincia un nuovo torneo, per comporre il
gruppo di giocatori che vi parteciperanno. Usando il *drag&drop* è possibile trascinarci dentro
nuovi giocatori, oppure riorganizzadone le squadre, come mostrato dalla figura: si possono
trascinare singoli giocatori da una squadra all'altra, oppure aggiungerne di nuovi
trascinandoli dalla finestra dei :ref:`giocatori <gestione giocatori>`. Il pulsante
:guilabel:`aggiungi…` mostra quella finestra, con i soli giocatori **non ancora** iscritti al
torneo.

.. note:: È possibile aggiungere nuovi giocatori in qualsiasi momento, anche quando il torneo è
          già cominciato e sono stati già giocati degli incontri: sebbene nei tornei ufficiali
          non sia consentito, in quelli amatoriali può succedere che un giocatore arrivi tardi,
          oppure che uno spettatore chieda di poter entrare nel gioco. In tal caso, il nuovo
          giocatore viene inserito in fondo alla classifica, con zero punti.

.. figure:: concorrenti_2.png
   :figclass: float-left

   Correzione squadre

La figura successiva mostra che una nuova squadra (e quindi con un un sfondo di colore verde) è
stata completata; una squadra è incomplete, con un solo giocatore: questo non ha alcun impatto
sulle operazioni successive (cioè, il torneo può essere giocato comunque), sebbene sia una
situazione piuttosto anomala; un'altra ancora verrà cancellata (sfondo rosso) perché entrambi i
suoi giocatori sono stati spostati.

.. hint:: I giocatori possono essere rimossi dal pannello trascinandoli e rilasciandoli su uno
          spazio vuoto del pannello (oppure sulla sua scrollbar, se il pannello è completamente
          occupato): l'icona associata all'operazione di drag riflette la situazione.

.. important:: Non è possibile, per ovvie ragioni, modificare la composizione di una squadra
               dopo che il primo turno è stato giocato.

.. warning:: Sebbene l'interfaccia consenta di accumulare svariate modifiche e di confermarle
             in un'unica transazione, quando si renda necessario ricombinare i giocatori
             spostandoli da una squadra all'altra, si raccomanda di effettuare e confermare una
             modifica alla volta, per evitare di incorrere in possibili errori di integrità.

.. figure:: ritira.png
   :figclass: float-right

   Conferma del ritiro

In qualsiasi momento, un iscritto può essere ritirato con un doppio clic e confermando
l'azione: questo significa che non parteciperà a ulteriori partite. Verrà comunque mostrato
nella classifica.

.. topic:: Squadre

   Dal punto di vista dell'applicazione, il numero di giocatori che compongono un singolo
   concorrente **non** fa alcuna differenza. Ogni partita coinvolge *due* distinti concorrenti,
   indipendentemente dal numero di giocatori che li compongono.

   Quando si organizzano dei campionati a squadre, tenere conto che una squadra è determinata
   sia dai singoli giocatori che la compongono **sia** dal loro ordine: la squadra `Giovanni e
   Paolo` è **diversa** da quella formata da `Paolo e Giovanni`, vale a dire dalle stesse
   persone ma in ordine inverso! È qui che si rivela particolarmente utile la funzionalità di
   `replica` di un torneo.

   .. note:: La :guilabel:`nazionalità` di una squadra è determinata da quella del suo primo
             giocatore, quindi l'ordine è *importante* quando si intende fare una classifica
             per nazionalità: assicurati di trascinare i giocatori nella sequenza giusta.


Primo turno
-----------

Una volta completato l'elenco dei concorrenti si passa alla generazione del primo turno del
torneo, che a seconda se questo è associato o meno a una particolare :ref:`valutazione
<gestione valutazioni glicko>` verrà generato tenendo conto della valutazione di ciascun
giocatore piuttosto che con degli abbinamenti casuali.

.. _ricombinazione manuale:

.. figure:: primoturno.png
   :figclass: float-left

   Ricombinazione manuale

L'`arbitro` può comunque decidere che la combinazione generata dall'applicazione per il primo
turno non è adeguata e deve essere ritoccata manualmente.

.. note::

   In circostanze eccezionali può essere necessario modificare anche gli abbinamenti dei turni
   successivi, ad esempio quando si sta inserendo un torneo già giocato senza l'ausilio di SoL.

   Se **sai quel che stai facendo**, puoi farlo tenendo premuto il tasto :kbd:`ALT` mentre
   clicchi sul pulsante che espande questo pannello.

Per farlo, basta espandere il pannello in basso :guilabel:`Abbinamenti turno corrente` e
ricombinare arbitrariamente gli incontri scambiando tra loro i vari concorrenti con il
drag&drop.

.. hint::

   Quando ci sono dozzine di tavoli, aumenta l'altezza del pannello trascinando il suo bordo
   superiore.

   Dovendo scambiare due giocatori molto distanti l'uno dall'altro, puoi usare la rotellina del
   mouse per far scorrere i tavoli **mantenendo** premuto il pulsante del mouse durante il
   trascinamento.

L'associazione tra i singoli incontri e il tavolo da gioco è casuale, per il primo turno. Dal
secondo in poi ``SoL`` cerca di far giocare ogni singolo giocatore su un tavolo diverso ad ogni
turno, seguendo l'ordine in classifica. Questo garantisce che i giocatori più forti giocheranno
di preferenza su tavoli diversi con numero basso, mentre quelli in fondo alla classifica sui
tavoli con numerazione più alta; in particolare quando ci sono pochi giocatori (e quindi pochi
tavoli) sarà più probabile che ai giocatori meno forti venga assegnato più volte lo stesso
tavolo.

.. _pannello incontri:

Incontri
--------

Il pannello centrale è dove si svolgono la maggior parte delle operazioni: lì, iterativamente,
viene creato il turno successivo, inseriti i risultati e calcolata la nuova classifica. I
pulsanti sulla sinistra del pannello consentono di rivedere i risultati di qualsiasi turno
giocato: anche il pannello con la classifica viene ricaricato per mostrare quella
corrispondente.

.. topic:: Risultati dettagliati di un incontro

   Un singolo incontro tra due concorrenti viene disputato su una o più *partite* e per
   calcolare la classifica è sufficiente inserirne solo il risultato cumulato finale.

   A volte potrebbe essere preferibile inserire anche i risultati dettagliati delle singole
   partite, vuoi per poter avere interessanti statistiche sugli *slam* e sulle *regine*, o più
   pragmaticamente per delegare l'onere dell'inserimento ai giocatori stessi, visto che
   ovviamente si tratta di una operazione che richiederebbe molto tempo.

   Con un doppio clic su un incontro apparirà una finestra che consente di inserire il
   dettaglio dei risultati con un calcolo automatico del punteggio finale.

   È possibile invece far sì che siano i concorrenti stessi ad inserirli, offrendogli in
   pratica una versione *digitale* dei cartellini di gioco: all'inizio del torneo puoi stampare
   le *etichette tavoli* (vedi :ref:`ulteriori azioni <ulteriori azioni tornei>` nella finestra
   di :ref:`gestione dei tornei <gestione tornei>`) e attaccarle ai singoli tavoli; l'etichetta
   riporta un ``QRCode`` che può essere usato da uno dei due concorrenti per aprire il modulo
   dove poter inserire i dettagli.

   Un caso diverso è quello delle `partite di allenamento`, dove i singoli giocatori possono
   inserire i propri risultati: solitamente questo avviene inviandogli una email ad ogni turno,
   contenente l'indirizzo del modulo che gli consente di farlo. Alternativamente, cliccando col
   punsante destro del mouse su un incontro puoi aprire tali moduli e inviarne l'indirizzo per
   altra via.

.. attention::

   Normalmente solo l'**ultimo** turno risulta modificabile, visto che gli abbinamenti di
   ciascun turno dipendono dai risultati dei turni precedenti. È quindi importante prestare
   particolare attenzione nell'inserimento degli *score*.

     .. note:: Nei tornei importanti è obbligatorio stampare i risultati e lasciarli in mostra
               per qualche minuto (oppure visualizzarli sullo schermo).

               I vincitori **devono** controllare la correttezza, **prima** di generare il
               turno successivo.

   Tuttavia può accadere che per un errore di qualsiasi genere siano stati inseriti risultati
   sbagliati e sia pertanto necessario correggere in qualche modo la situazione.

   Se l'errore è stato commesso nell'ultimo turno giocato e quello successivo non è ancora
   iniziato, è sufficiente *cancellare* l'ultimo turno (se è già stato generato), apportare le
   rettifiche del caso e procedere normalmente.

   .. figure:: cancellaturno.png
      :figclass: float-right

      Cancellazione ultimo turno

   Qualora invece ci si accorgesse di errori nei risultati di turni precedenti e siano già
   stati giocati ulteriori turni, è comunque possibile modificarli (SoL chiede esplicita
   conferma quando si tenta di farlo): la classifica verrà ricalcolata, ma ovviamente le
   combinazioni dei turni successivi **non verranno alterate**.

   Infine, se l'errore viene rilevato solo quando il torneo è terminato, l'unica soluzione
   possibile è intervenire manualmente sui punteggi finali, ottenendo un ordine corretto nella
   classifica del torneo e di conseguenza anche in quella di campionato.

.. hint::

   Per inserire i risultati di ogni turno, vi sono due strategie:

     a. ordinare i cartellini di gioco per numero di tavolo crescente, procedendo quindi
        all'inserimento dei singoli punteggi: in questo caso, può essere utile il tasto
        :kbd:`TAB` che sposta il *focus* di inserimento da un campo al successivo;

     b. quando il numero di tavoli è elevato (e quindi l'ordinamento manuale dei cartellini di
        gioco risulta troppo laborioso), è utile il poter “saltare” direttamente
        all'inserimento dei risultati di un particolare tavolo: avendo il *focus* nel pannello
        degli incontri (ma **non** in modifica di un risultato), semplicemente digitando il
        numero di tavolo il *focus* verrà spostato sulla riga con il tavolo in questione,
        entrando direttamente in modifica del punteggio del primo giocatore di quell'incontro.

Mentre si sta preparando il turno successivo, cioè mentre vengono inseriti i punteggi
dell'ultimo turno giocato, si controllano i risultati e si genera il nuovo turno, è possibile
mostrare un `conto alla rovescia` in una nuova scheda del browser usando la voce
:guilabel:`Prepara` del menu.

Quando il nuovo turno è pronto, è possibile mostrare un :ref:`conto alla rovescia <countdown>`
leggermente diverso con la voce :guilabel:`Gioca`.

.. _turno finale:

Turno finale
~~~~~~~~~~~~

Nei tornei maggiori è possibile giocare un ulteriore turno per determinare le prime due (o
quattro) posizioni della classifica.

Storicamente SoL non consentiva di inserire i risultati di questi incontri finali e l'unico
modo per influenzare la classifica era quello di correggere manualmente i premi finali del
torneo. Nella versione 3.1 è stato introdotto un meccanismo per gestirli, che è controllato dal
:ref:`campo finali <campo finali>` del torneo.

Quando viene impostato a ``1`` oppure a ``2``, un pulsante :guilabel:`Turno finale` appare nel
menu: esso genera il turno finale con un incontro tra i primi due concorrenti nella classifica
e, quando è impostato a ``2``, un altro tra il terzo e quarto concorrente, dove potranno essere
inseriti i risultati delle finali. Quando :guilabel:`Tipo di finale` del torneo è impostato a
``Al meglio di tre incontri``, potranno essere generati fino a un massimo di tre ulteriori
round, usando il consueto pulsante :guilabel:`Nuovo turno` nel menu.

Non appena i risultati di tutti i turni sono stati inseriti, i premi finali vengono assegnati
automaticamente e il torneo è terminato.

..
   .. figure:: classnazione.png
      :figclass: float-right

      Classifica raggruppata per nazionalità

Classifica
----------

Ogni qualvolta si modificano e confermano i risultati dell'ultimo round la classifica viene
automaticamente ricalcolata e mostrata qui. La colonna :guilabel:`premio` è generalmente
visibile solo dopo aver effettuato la *premiazione finale*.

.. È possibile vedere la *classifica per nazione*, raggruppando i dati per nazionalità. Il
   pulsante di :guilabel:`stampa` tiene conto della modalità attiva e quindi crea la classifica
   normale oppure quella raggruppata.

.. hint:: Con un doppio clic su un giocatore il pannello degli incontri_ si focalizza
          mostrando solo gli incontri effettuati da quel giocatore. È possibile mostrare il
          dettaglio di altri giocatori, sempre col doppio clic sul nome. La vista tradizionale
          viene ripristinata sia facendo doppio clic una seconda volta sul medesimo giocatore
          e comunque quando viene creato un nuovo turno di gioco.

Dopo aver effettuato la :guilabel:`Premiazione` la colonna :guilabel:`premio` può essere
modificata, consentendo così di forzare i premi assegnati, piuttosto che scambiare
eventualmente l'ordine dei giocatori in testa in base all'esito della finale.
