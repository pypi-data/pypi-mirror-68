// -*- coding: utf-8 -*-
// :Project:   SoL -- Matches panel of the tourney management
// :Created:   gio 20 nov 2008 18:23:54 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2008, 2009, 2010, 2013, 2014, 2015, 2016, 2018, 2020 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/
/*jsl:declare MP*/
/*jsl:declare window*/
/*jsl:declare SoL*/


Ext.define('SoL.view.Matches.Actions', {
    extend: 'MP.action.StoreAware',
    uses: [
        'Ext.Action',
        'MP.window.Notification',
    ],

    statics: {
        NEW_TURN_ACTION: 'new_turn',
        FINAL_TURN_ACTION: 'final_turn',
        SHOW_PRE_COUNTDOWN_ACTION: 'show_pre_countdown',
        SHOW_COUNTDOWN_ACTION: 'show_countdown',
        PRINT_CARDS_ACTION: 'print_cards',
        PRINT_RESULTS_ACTION: 'print_results',
        PRINT_ALL_RESULTS_ACTION: 'print_all_results',
        PRINT_MATCHES_ACTION: 'print_matches',
        SEND_TRAINING_MATCH_EMAILS_ACTION: 'send_training_match_emails',
        RECOMPUTE_RANKING_ACTION: 'recompute_ranking',
        REFRESH_ACTION: 'refresh',
        EDIT_MATCH_ACTION: 'edit_match'
    },

    initActions: function() {
        var me = this,
            ids = me.statics(),
            tourney = me.module.tourney;

        me.callParent();

        me.newTurnAction = me.addAction(new Ext.Action({
            itemId: ids.NEW_TURN_ACTION,
            text: _('New round'),
            tooltip: _('Create next round.'),
            iconCls: 'new-turn-icon',
            disabled: tourney.currentturn != tourney.rankedturn,
            hidden: tourney.readOnly,
            scope: me.component,
            handler: me.component.newTurn
        }));

        me.finalTurnAction = me.addAction(new Ext.Action({
            itemId: ids.FINAL_TURN_ACTION,
            text: _('Final round'),
            tooltip: _('Create final round.'),
            iconCls: 'new-turn-icon',
            disabled: tourney.currentturn != tourney.rankedturn,
            hidden: tourney.readOnly || !tourney.finals || tourney.system === 'knockout',
            scope: me.component,
            handler: me.component.finalTurn
        }));

        me.showPreCountdownAction = me.addAction(new Ext.Action({
            itemId: ids.SHOW_PRE_COUNTDOWN_ACTION,
            text: _('Prepare'),
            tooltip: _('Show a countdown while preparing for the next round.'),
            iconCls: 'pre-countdown-icon',
            disabled: tourney.readOnly,
            hidden: tourney.readOnly,
            scope: me.component,
            handler: me.component.showPreCountdown
        }));

        me.showCountdownAction = me.addAction(new Ext.Action({
            itemId: ids.SHOW_COUNTDOWN_ACTION,
            text: _('Play'),
            tooltip: _('Show a countdown for the current round.'),
            iconCls: 'countdown-icon',
            disabled: tourney.readOnly,
            hidden: tourney.readOnly,
            scope: me.component,
            handler: me.component.showGameCountdown
        }));

        me.printCardsAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_CARDS_ACTION,
            text: _('Scorecards'),
            tooltip: _('Print current round scorecards.'),
            iconCls: 'print-icon',
            disabled: tourney.readOnly,
            hidden: tourney.readOnly,
            scope: me.component,
            handler: me.component.printCards
        }));

        me.printResultsAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_RESULTS_ACTION,
            text: _('Results'),
            tooltip: _('Print selected round results.'),
            iconCls: 'print-icon',
            handler: function() {
                var turn = me.component.filteredTurn,
                    url = '/pdf/results/' + tourney.idtourney;
                if(turn) url += '?turn=' + turn;
                window.location.assign(url);
            }
        }));

        me.printAllResultsAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_ALL_RESULTS_ACTION,
            text: _('All results'),
            tooltip: _('Print results of all played rounds.'),
            iconCls: 'print-icon',
            handler: function() {
                var url = '/pdf/results/' + tourney.idtourney + '?turn=all';
                window.location.assign(url);
            }
        }));

        me.printMatchesAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_MATCHES_ACTION,
            text: _('Matches'),
            tooltip: _('Print selected round matches.'),
            iconCls: 'print-icon',
            disabled: tourney.readOnly,
            hidden: tourney.readOnly,
            handler: function() {
                var turn = me.component.filteredTurn,
                    url = '/pdf/matches/' + tourney.idtourney;
                if(turn) url += '?turn=' + turn;
                window.location.assign(url);
            }
        }));

        me.sendTrainingURLs = me.addAction(new Ext.Action({
            itemId: ids.SEND_TRAINING_MATCH_EMAILS_ACTION,
            text: _('Send emails'),
            tooltip: _('Send training match emails to each competitor.'),
            iconCls: 'send-email-icon',
            disabled: tourney.readOnly || tourney.currentturn != tourney.rankedturn,
            hidden: tourney.readOnly || !tourney.TrainingBoards,
            scope: me.component,
            handler: me.component.sendTrainingURLs
        }));

        me.recomputeRanking = me.addAction(new Ext.Action({
            itemId: ids.RECOMPUTE_RANKING_ACTION,
            text: _('Recompute ranking'),
            tooltip: _('Recompute current ranking.'),
            iconCls: 'recompute-ranking-icon',
            disabled: tourney.readOnly,
            hidden: tourney.readOnly || !tourney.TrainingBoards,
            scope: me.component,
            handler: me.component.updateRanking
        }));

        me.refresh = me.addAction(new Ext.Action({
            itemId: ids.REFRESH_ACTION,
            text: _('Refresh'),
            tooltip: _('Reload matches from the database.'),
            icon: '/desktop/extjs/resources/ext-theme-classic/images/grid/refresh.gif',
            disabled: tourney.readOnly,
            hidden: tourney.readOnly || !tourney.TrainingBoards,
            handler: function() {
                me.module.matches_grid.store.reload();
            }
        }));

        me.editMatch = me.addAction(new Ext.Action({
            itemId: ids.EDIT_MATCH_ACTION,
            text: _('Modify'),
            tooltip: _('Edit per-board results of the selected match.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            hidden: tourney.readOnly,
            needsOneSelectedRow: true,
            handler: function() {
                if(!tourney.TrainingBoards) {
                    var record = me.component.getSelectionModel().getSelection()[0];
                    me.component.showEditMatchWindow(record);
                }
            }
        }));
    },

    attachActions: function() {
        var me = this,
            tourney = me.module.tourney;

        me.callParent();

        var tbar = me.component.child('#ttoolbar');

        tbar.add(0,
                 me.editMatch,
                 me.showPreCountdownAction,
                 me.newTurnAction,
                 me.finalTurnAction,
                 tourney.TrainingBoards ? me.sendTrainingURLs : null,
                 tourney.TrainingBoards ? me.recomputeRanking : null,
                 me.printMatchesAction,
                 me.printCardsAction,
                 me.showCountdownAction,
                 me.printResultsAction,
                 me.printAllResultsAction);

        tbar.add(tbar.items.length-2,
                 me.refresh);

        me.component.on({
            itemdblclick: function() {
                if(!me.editMatch.isDisabled())
                    me.editMatch.execute();
            }
        });
    },

    shouldDisableAction: function(act) {
        var me = this,
            statics = me.statics(),
            disable = false;

        if(act.itemId == statics.EDIT_MATCH_ACTION) {
            var tourney = me.module.tourney,
                grid = me.component;
            disable = (tourney.TrainingBoards
                       || tourney.prized
                       || tourney.readOnly
                       || !tourney.currentturn
                       || tourney.currentturn == tourney.rankedturn
                       || grid.getSelectionModel().getSelection().length != 1
                       || (!grid.allowEditPreviousTurns
                           && grid.getSelectionModel().getSelection()[0].get("turn") < tourney.currentturn));
        }

        return disable;
    }
});

Ext.define('SoL.view.Matches', {
    extend: 'MP.grid.Panel',

    alias: 'widget.matches-grid',

    requires: [
        'SoL.view.Matches.Actions'
    ],

    clicksToEdit: 1,

    statics: {
        ordinal: function(num) {
            var r;

            switch(num) {
                case  1: r = _('the first'); break;
                case  2: r = _('the second'); break;
                case  3: r = _('the third'); break;
                case  4: r = _('the fourth'); break;
                case  5: r = _('the fifth'); break;
                case  6: r = _('the sixth'); break;
                case  7: r = _('the seventh'); break;
                case  8: r = _('the eighth'); break;
                case  9: r = _('the nineth'); break;
                case 10: r = _('the tenth'); break;
                case 11: r = _('the eleventh'); break;
                case 12: r = _('the twelfth'); break;
                case 13: r = _('the thirteenth'); break;
                case 14: r = _('the fourteenth'); break;
                case 15: r = _('the fifteenth'); break;
                case 16: r = _('the sixteenth'); break;
                default:
                    r = num+'';
                    break;
            }
            return r;
        },

        ordinalp: function(num) {
            var r;
            switch(num) {
                case  1: r = _('of the first'); break;
                case  2: r = _('of the second'); break;
                case  3: r = _('of the third'); break;
                case  4: r = _('of the fourth'); break;
                case  5: r = _('of the fifth'); break;
                case  6: r = _('of the sixth'); break;
                case  7: r = _('of the seventh'); break;
                case  8: r = _('of the eighth'); break;
                case  9: r = _('of the nineth'); break;
                case 10: r = _('of the tenth'); break;
                case 11: r = _('of the eleventh'); break;
                case 12: r = _('of the twelfth'); break;
                case 13: r = _('of the thirteenth'); break;
                case 14: r = _('of the fourteenth'); break;
                case 15: r = _('of the fifteenth'); break;
                case 16: r = _('of the sixteenth'); break;
                default:
                    r = num+'';
                    break;
            }
            return r;
        },

        getConfig: function(callback, errorcb, config) {
            //jsl:unused errorcb
            var me = this, /* NB: this is the Tourney module */
                ordinal = SoL.view.Matches.ordinal,
                ordinalp = SoL.view.Matches.ordinalp,
                cfg = config.Matches = {
                    dataURL: '/tourney/matches',
                    filters: [{
                        id: 'turn',
                        property: 'turn',
                        value: config.tourney.currentturn,
                        operator: '='
                    }],
                    header: true,
                    layout: 'fit',
                    lbar: [],
                    noAddAndDelete: true,
                    noBottomToolbar: true,
                    noFilterbar: true,
                    pageSize: 999,
                    plugins: [
                        Ext.create('SoL.view.Matches.Actions', {
                            module: me
                        })
                    ],
                    saveChangesURL: '/bio/saveChanges',
                    sorters: ['turn', 'board'],
                    title: (config.tourney.currentturn === 0
                            ? _('Matches')
                            : Ext.String.format(
                                _('Matches {0} round'),
                                ordinalp(config.tourney.currentturn))),
                    xtype: 'matches-grid'
                };

            function apply_filter(btn) {
                me.matches_grid.filterOnTurn(btn.turn);
            }

            for(var i=1; i <= config.tourney.currentturn; i++) {
                cfg.lbar.push({
                    itemId: 'turn-' + i,
                    text: i,
                    cls: i==config.tourney.currentturn ? 'active-turn' : '',
                    tooltip: Ext.String.format(
                        _('Show the matches {0} round.'), ordinalp(i)),
                    turn: i,
                    handler: apply_filter
                });
            }

            cfg.lbar.push('-', {
                iconCls: 'icon-cross',
                tooltip: _('Remove last round.'),
                handler: function(btn) {
                    var grid = btn.up().up();
                    var turn = config.tourney.currentturn;

                    if(turn) {
                        var title = _('Delete last round?');
                        var msg = Ext.String.format(
                            _('Do you really want to delete {0} round?<br/>This is <b>NOT</b> revertable!'),
                            ordinal(turn));
                        Ext.Msg.confirm(title, msg, function(response) {
                            if('yes' == response) {
                                grid.deleteTurn(turn);
                            }
                        });
                    }
                }
            });

            function decorate_winner(val, meta, record, rowIndex, colIndex, store) {
                if(record.get('score1') > record.get('score2'))
                    meta.tdCls += ' winner1';
                else if(record.get('score1') < record.get('score2'))
                    meta.tdCls += ' winner2';
                return val;
            };

            function decorate_winner_c1(val, meta, record, rowIndex, colIndex, store) {
                if(record.get('score1') > record.get('score2'))
                    meta.tdCls += ' winner';
                return val;
            };

            function decorate_winner_c2(val, meta, record, rowIndex, colIndex, store) {
                if(record.get('score1') < record.get('score2'))
                    meta.tdCls += ' winner';
                return val;
            };

            MP.data.MetaData.fetch(cfg.dataURL
                                   + '?filter_by_idtourney=' + config.tourney.idtourney,
                                   me, function(metadata) {
                var overrides = {
                    description: { renderer: decorate_winner },
                    score1: { renderer: decorate_winner_c1,
                              editor: { hideTrigger: true } },
                    score2: { renderer: decorate_winner_c2,
                              editor: { hideTrigger: true } }
                };

                Ext.apply(cfg, {
                    metadata: metadata,
                    fields: metadata.fields(overrides),
                    columns: metadata.columns(overrides),
                    idProperty: metadata.primary_key,
                    totalProperty: metadata.count_slot,
                    successProperty: metadata.success_slot,
                    rootProperty: metadata.root_slot
                });
                callback(cfg);
            });
        }
    },

    initEvents: function() {
        var me = this, tourney = me.module.tourney;

        me.callParent();

        me.on("beforeedit", function(editor, event) {
            var ordinal = SoL.view.Matches.ordinal,
                ordinalp = SoL.view.Matches.ordinalp;

            if(tourney.prized)
                return false;

            var rec = event.record,
                phantom = rec.get("idcompetitor2") === null;

            if(!me.allowEditPreviousTurns && rec.get("turn") < tourney.currentturn) {
                Ext.Msg.confirm(
                    _('Confirm edit of old round results'),
                    Ext.String.format(
                        _('Do you confirm you want to edit the results {0} round, even if the'
                          + ' ranking is currently at {1}?<br/>Doing so the ranking will be'
                          + ' updated but following rounds pairing will remain unchanged!'),
                        ordinalp(rec.get("turn")),
                        ordinal(tourney.currentturn)),
                    function(response) {
                        if(response == 'yes') {
                            me.allowEditPreviousTurns = true;
                            me.editingPlugin
                                .startEdit(event.rowIdx, me.getColumnByName('score1'));
                            Ext.create("MP.window.Notification", {
                                position: 'tl',
                                title: _('Changing old results'),
                                html: Ext.String.format(
                                    _('You are now allowed to change the results {0} round'),
                                    ordinalp(rec.get("turn"))),
                                iconCls: 'info-icon'
                            }).show();
                        }
                    }
                );
            }

            return (!phantom && (rec.get("turn") == tourney.currentturn
                                 || me.allowEditPreviousTurns === true));
        });

        // Install a KeyMap on the grid that allows jumping to a given record
        // (and eventually start editing its score1 column) simply by digiting
        // its position

        var rownum = '',
            gotoRowNum = Ext.Function.createBuffered(function() {
                var sm = me.getSelectionModel(),
                    row = parseInt(rownum, 10) - 1,
                    ep = me.editingPlugin;

                sm.select(row);
                if(ep) {
                    ep.startEdit(row, me.getColumnByName('score1'));
                }

                rownum = '';
            }, 400);

        me.jumpToRecordKeyMap = new Ext.util.KeyMap({
            target: me.getView(),
            eventName: 'itemkeydown',
            processEvent: function(view, record, node, index, event) {
                return event;
            },
            binding: {
                key: "1234567890",
                fn: function(keyCode, e) {
                    rownum = rownum + (e.getKey() - 48);
                    gotoRowNum();
                }
            }
        });
    },

    classifyRecord: function(rec, rowIndex, rowParams, store) {
        var result = store.classifyRecord(rec);
        if(result === '' && rec.get('score1') == 0 && rec.get('score2') == 0) {
            result = 'incomplete-record';
        }
        return result;
    },

    onDestroy: function() {
        if(this.jumpToRecordKeyMap) {
            Ext.destroy(this.jumpToRecordKeyMap);
            delete this.jumpToRecordKeyMap;
        }
        this.callParent();
    },

    newTurn: function() {
        var me = this,
            ordinalp = me.statics().ordinalp,
            tourney = me.module.tourney,
            lbar = me.child('toolbar[dock="left"]');

        me.allowEditPreviousTurns = false;

        if(me.focusedCompetitor) {
            lbar.show();
            me.getColumnByName('turn').hide();
            me.getColumnByName('board').show();
            me.filterOnTurn(tourney.currentturn);
            me.focusedCompetitor = null;
        }

        Ext.Ajax.request({
            url: '/tourney/newTurn',
            params: { idtourney: tourney.idtourney },
            success: function (r) {
                var res = Ext.decode(r.responseText);
                if(!res) {
                    Ext.MessageBox.alert(
                        _("Comunication error"),
                        _('Cannot decode JSON object'));
                } else {
                    if(res.success) {
                        var cturn = res.currentturn;

                        tourney.currentturn = cturn;
                        tourney.rankedturn = res.rankedturn;
                        tourney.prized = res.prized;

                        lbar.insert(cturn-1, Ext.create('Ext.button.Button', {
                            itemId: 'turn-' + cturn,
                            text: cturn,
                            tooltip: Ext.String.format(
                                _('Show the matches {0} round.'),
                                ordinalp(cturn)),
                            turn: cturn,
                            handler: function(btn) {
                                me.filterOnTurn(btn.turn);
                            }
                        }));
                        me.filterOnTurn(cturn);
                        me.updateActions();
                    } else {
                        Ext.MessageBox.alert(_('Error'), res.message);
                    }
                }
            }
        });
    },

    finalTurn: function() {
        var me = this,
            ordinalp = me.statics().ordinalp,
            tourney = me.module.tourney,
            lbar = me.child('toolbar[dock="left"]');

        me.allowEditPreviousTurns = false;

        if(me.focusedCompetitor) {
            lbar.show();
            me.getColumnByName('turn').hide();
            me.getColumnByName('board').show();
            me.filterOnTurn(tourney.currentturn);
            me.focusedCompetitor = null;
        }

        Ext.Ajax.request({
            url: '/tourney/finalTurn',
            params: { idtourney: tourney.idtourney },
            success: function (r) {
                var res = Ext.decode(r.responseText);
                if(!res) {
                    Ext.MessageBox.alert(
                        _("Comunication error"),
                        _('Cannot decode JSON object'));
                } else {
                    if(res.success) {
                        var cturn = res.currentturn;

                        tourney.currentturn = cturn;
                        tourney.rankedturn = res.rankedturn;
                        tourney.finalturns = res.finalturns;
                        tourney.prized = res.prized;

                        lbar.insert(cturn-1, Ext.create('Ext.button.Button', {
                            itemId: 'turn-' + cturn,
                            text: cturn,
                            tooltip: Ext.String.format(
                                _('Show the matches {0} round.'),
                                ordinalp(cturn)),
                            turn: cturn,
                            handler: function(btn) {
                                me.filterOnTurn(btn.turn);
                            }
                        }));
                        me.filterOnTurn(cturn);
                        me.updateActions();
                    } else {
                        Ext.MessageBox.alert(_('Error'), res.message);
                    }
                }
            }
        });
    },

    deleteTurn: function(turn) {
        var me = this,
            tourney = me.module.tourney;

        me.allowEditPreviousTurns = false;

        Ext.Ajax.request({
            url: '/tourney/deleteFromTurn',
            params: { idtourney: tourney.idtourney, fromturn: turn },
            success: function (r) {
                var res = Ext.decode(r.responseText);
                if(!res) {
                    Ext.MessageBox.alert(
                        _("Comunication error"),
                        _('Cannot decode JSON object'));
                } else {
                    if(res.success) {
                        var lbar = me.child('toolbar[dock="left"]');

                        tourney.currentturn = res.currentturn;
                        tourney.rankedturn = res.rankedturn;
                        tourney.finalturns = res.finalturns;
                        tourney.prized = res.prized;

                        if(turn > 1) {
                            me.filterOnTurn(turn - 1);
                        } else {
                            me.setTitle(_('Matches'));
                            me.store.removeAll();
                            me.module.reloadRanking();
                        }
                        lbar.remove('turn-' + turn, true);

                        me.updateActions();
                    } else {
                        Ext.MessageBox.alert(_('Error'), res.message);
                    }
                }
            }
        });
    },

    filterOnTurn: function(turn) {
        var me = this,
            store = me.store,
            tourney = me.module.tourney;

        if(store.isModified()) {
            Ext.MessageBox.alert(
                _('Uncommitted changes'),
                _('There are uncommitted changes, cannot switch to a different round!'));
            return;
        }

        me.allowEditPreviousTurns = false;

        store.filter({
            id: 'turn',
            property: 'turn',
            value: turn,
            operator: '='
        });

        me.child('toolbar[dock="left"]').cascade(function(btn) {
            if(btn.turn == turn) {
                btn.addCls('active-turn');
            } else {
                btn.removeCls('active-turn');
            }
        });

        me.module.reloadRanking(turn);

        if(turn != tourney.currentturn) {
            me.filteredTurn = turn;
        } else {
            delete me.filteredTurn;
        }
    },

    printCards: function() {
        var me = this,
            tourney = me.module.tourney,
            url = '/pdf/scorecards/' + tourney.idtourney,
            win, form,
            winWidth = 215,
            winHeight = 110,
            now = new Date(),
            minValue = now,
            maxValue = Ext.Date.add(now, Ext.Date.HOUR, 2);

        if(minValue.getDate() != maxValue.getDate()) {
            // This happens after 10pm, when maxValue crosses midnight and thus its
            // time value becomes smaller than the minValue time value: the timefield
            // does not handle this, and there is no easy workaround other than
            // showing all times...
            minValue = maxValue = undefined;
        }

        var handler = function() {
            var frm = form.getForm();
            if(frm.isValid()) {
                var startts = frm.getFields().items[0].getValue(),
                    starttime = startts.getTime(),
                    tzoffset = startts.getTimezoneOffset();
                url += '?starttime=' + starttime + '&tzoffset=' + tzoffset;
                win.destroy();
                window.location.assign(url);
            }
        };

        var onKeyDown = function(field, event) {
            if (event.keyCode === event.RETURN || event.keyCode === 10) {
                handler();
            }
        };

        form = new Ext.form.Panel({
            frame: true,
            bodyPadding: '10 10 0',
            defaults: {
                labelWidth: 50,
                anchor: '100%'
            },
            items: [{
                xtype: 'timefield',
                itemId: 'starttime',
                increment: 5,
                allowBlank: false,
                minValue: minValue,
                maxValue: maxValue,
                value: Ext.Date.add(now, Ext.Date.MINUTE, 10 + (5 - now.getMinutes() % 5)),
                enableKeyEvents: true,
                listeners: {
                    keydown: onKeyDown,
                    scope: me
                }

            }],
            buttons: [{
                text: _('Cancel'),
                handler: function() {
                    win.destroy();
                }
            }, {
                text: _('Confirm'),
                formBind: true,
                handler: handler
            }]
        });

        win = me.module.app.getDesktop().createWindow({
            title: _('Estimated start'),
            width: winWidth,
            height: winHeight,
            layout: 'fit',
            minimizable: false,
            maximizable: false,
            items: [form],
            defaultFocus: 'starttime'
        });

        win.show();
    },

    commitChanges: function() {
        var me = this,
            complete_scores = true;

        me.store.each(function(rec) {
            if(rec.get("score1") === 0 && rec.get("score2") === 0) {
                complete_scores = false;
                me.getSelectionModel().select([rec]);
                Ext.create("MP.window.Notification", {
                    position: 'tl',
                    width: 260,
                    title: _('Incomplete scores'),
                    html: _('There is at least one match without result: the ranking will <strong>not</strong> be recomputed until you insert all of them!'),
                    iconCls: 'alert-icon'
                }).show();
                return false;
            } else
                return true;
        });

        me.store.commitChanges(me.saveChangesURL, 'idmatch', function() {
            if(complete_scores)
                me.updateRanking();
        });
    },

    updateRanking: function() {
        var me = this,
            tourney = me.module.tourney;

        Ext.Ajax.request({
            url: '/tourney/updateRanking',
            params: { idtourney: tourney.idtourney },
            success: function (r) {
                var res = Ext.decode(r.responseText);
                if(!res) {
                    Ext.MessageBox.alert(
                        _("Comunication error"),
                        _('Cannot decode JSON object'));
                } else {
                    if(res.success) {
                        tourney.currentturn = res.currentturn;
                        tourney.rankedturn = res.rankedturn;
                        tourney.finalturns = res.finalturns;
                        tourney.prized = res.prized;
                        me.module.reloadRanking();
                        me.updateActions();
                    } else {
                        Ext.MessageBox.alert(_('Error'), res.message);
                    }
                }
            }
        });
    },

    sendTrainingURLs: function() {
        var me = this,
            tourney = me.module.tourney;

        Ext.Ajax.request({
            url: '/tourney/sendTrainingURLs',
            params: { idtourney: tourney.idtourney },
            success: function (r) {
                var res = Ext.decode(r.responseText);
                if(!res) {
                    Ext.MessageBox.alert(
                        _("Comunication error"),
                        _('Cannot decode JSON object'));
                } else {
                    if(res.success) {
                        Ext.create("MP.window.Notification", {
                            position: 'tl',
                            width: 260,
                            title: _('Emails have been sent…'),
                            html: _('All competitors have been notified with a link to insert their results.'),
                            iconCls: 'info-icon'
                        }).show();
                    } else {
                        Ext.MessageBox.alert(_('Error'), res.message);
                    }
                }
            }
        });
    },

    showGameCountdown: function() {
        var me = this,
            tourney = me.module.tourney,
            url = '/tourney/countdown?idtourney=' + tourney.idtourney;

        window.open(url, "SoL Countdown");
    },

    showPreCountdown: function() {
        var me = this,
            tourney = me.module.tourney,
            url = '/tourney/pre_countdown?idtourney=' + tourney.idtourney,
            win, form,
            winWidth = 245,
            winHeight = 140;

        var handler = function() {
            var frm = form.getForm();
            if(frm.isValid()) {
                var flds = frm.getFields(),
                    duration = flds.items[0].getValue(),
                    prealarm = flds.items[1].getValue();
                url += '&duration=' + duration + '&prealarm=' + prealarm;
                win.destroy();
                window.open(url, "SoL Countdown");
            }
        };

        var onKeyDown = function(field, event) {
            if (event.keyCode === event.RETURN || event.keyCode === 10) {
                handler();
            }
        };

        form = new Ext.form.Panel({
            frame: true,
            bodyPadding: '10 10 0',
            defaults: {
                labelWidth: 50,
                anchor: '100%'
            },
            items: [{
                xtype: 'numberfield',
                itemId: 'duration',
                fieldLabel: _('Minutes'),
                allowBlank: false,
                allowDecimals: false,
                minValue: 1,
                value: 15,
                step: 5,
                enableKeyEvents: true,
                listeners: {
                    keydown: onKeyDown,
                    scope: me
                }

            }, {
                xtype: 'numberfield',
                itemId: 'prealarm',
                fieldLabel: _('Prealarm'),
                allowBlank: false,
                allowDecimals: false,
                minValue: 0,
                value: 2,
                enableKeyEvents: true,
                listeners: {
                    keydown: onKeyDown,
                    scope: me
                }

            }],
            buttons: [{
                text: _('No'),
                handler: function() {
                    win.destroy();
                }
            }, {
                text: _('Yes'),
                formBind: true,
                handler: handler
            }]
        });

        win = me.module.app.getDesktop().createWindow({
            title: _('Show countdown to next round?'),
            width: winWidth,
            height: winHeight,
            layout: 'fit',
            minimizable: false,
            maximizable: false,
            items: [form],
            defaultFocus: 'duration'
        });

        win.show();
    },

    updateActions: function() {
        var me = this,
            tourney = me.module.tourney,
            pre = me.findActionById('show_pre_countdown'),
            nta = me.findActionById('new_turn'),
            fta = me.findActionById('final_turn'),
            clk = me.findActionById('show_countdown'),
            mtc = me.findActionById('print_matches'),
            pca = me.findActionById('print_cards'),
            res = me.findActionById('print_results'),
            all = me.findActionById('print_all_results'),
            save = me.findActionById('save'),
            restore = me.findActionById('restore'),
            stme = me.findActionById('send_training_match_emails'),
            rr = me.findActionById('recompute_ranking'),
            em = me.findActionById('edit_match'),
            lbar = me.child('toolbar[dock="left"]');

        pre.setDisabled(tourney.currentturn != 0
                        && (tourney.prized
                            || tourney.readOnly
                            || tourney.currentturn == tourney.rankedturn));
        pre.setHidden(tourney.prized || tourney.readOnly);

        nta.setDisabled(!tourney.participants
                        || (tourney.currentturn > 0
                            && tourney.currentturn != tourney.rankedturn));
        nta.setHidden(tourney.prized
                      || tourney.readOnly
                      || (tourney.system == 'knockout'
                          && tourney.currentturn == Math.log2(tourney.participants)));

        fta.setDisabled(!tourney.participants
                        || tourney.finalturns
                        || (tourney.currentturn > 0
                            && tourney.currentturn != tourney.rankedturn));
        fta.setHidden(tourney.prized
                      || !tourney.finals
                      || tourney.readOnly
                      || tourney.system === 'knockout');

        clk.setDisabled(tourney.prized
                        || tourney.readOnly
                        || tourney.currentturn == tourney.rankedturn);
        clk.setHidden(tourney.prized || tourney.readOnly);

        mtc.setDisabled(tourney.currentturn == 0);

        pca.setDisabled(tourney.currentturn == 0);
        pca.setHidden(tourney.prized || tourney.readOnly);

        res.setDisabled(tourney.rankedturn == 0);

        all.setDisabled(tourney.rankedturn == 0);

        save.setHidden(tourney.prized || tourney.readOnly);

        restore.setHidden(tourney.prized || tourney.readOnly);

        stme.setDisabled(tourney.prized
                         || tourney.readOnly
                         || tourney.currentturn == tourney.rankedturn);

        rr.setDisabled(tourney.prized
                       || tourney.readOnly
                       || tourney.currentturn == tourney.rankedturn);

        em.setHidden(tourney.prized || tourney.readOnly);

        lbar.cascade(function(btn) {
            if(btn.xtype == 'tbseparator' || btn.iconCls == 'icon-cross') {
                btn.setVisible(!tourney.readOnly
                               && ((!tourney.prized && tourney.currentturn > 0)
                                   || tourney.finalturns));
            }
        });
    },

    recomputeScores: function(field, newValue, oldValue) {
        var me = this,
            trainingboards = !!me.module.tourney.TrainingBoards,
            total1 = 0,
            total2 = 0,
            columns = me.matchEditForm.child('container').query('container'),
            c1column, c2column, qcolumn;

        if(trainingboards) {
            c1column = columns[0];
            c2column = columns[1];
            qcolumn = null;
        } else {
            c1column = columns[0];
            c2column = columns[2];
            qcolumn = columns[1];
        }

        for(var i = 1; ; i++) {
            var coins1 = c1column.getComponent('coins1_' + i),
                coins2 = c2column.getComponent('coins2_' + i),
                queen = qcolumn && qcolumn.getComponent('queen_' + i);

            if(!coins1)
                break;

            if(!trainingboards && coins1.getValue() && coins2.getValue()) {
                Ext.Msg.alert(_('Error'),
                              Ext.String.format(_('Result of board {0} is not valid!'), i));
                break;
            }

            if(coins1.getValue() > coins2.getValue()) {
                if(!trainingboards && queen.getValue() == '1')
                    if(total1 < 22)
                        total1 += 3;
                total1 += coins1.getValue();
            } else if(coins1.getValue() < coins2.getValue()) {
                if(!trainingboards && queen.getValue() == '2')
                    if(total2 < 22)
                        total2 += 3;
                total2 += coins2.getValue();
            }
        }

        if(total1 > 25) total1 = 25;
        if(total2 > 25) total2 = 25;

        c1column.getComponent('score1').setValue(total1);
        c2column.getComponent('score2').setValue(total2);
    },

    showEditMatchWindow: function(record) {
        var me = this,
            desktop = me.module.app.getDesktop(),
            win = desktop.getWindow('edit-match-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        var metadata = me.module.matches_grid.metadata,
            trainingboards = !!me.module.tourney.TrainingBoards,
            size = desktop.getReasonableWindowSize(trainingboards ? 400 : 600, 150),
            editors = metadata.editors({
                '*': { editor: MP.form.Panel.getDefaultEditorSettingsFunction('100%') }
            }),
            column1 = [],
            column2 = trainingboards ? null : [],
            column3 = [],
            form, tabindex = 1;

        for(var i=1; i<10; i++) {
            var c1 = editors['coins1_' + i],
                c2 = editors['coins2_' + i],
                q;
            if(c1 && c2) {
                if(!trainingboards) {
                    q = editors['queen_' + i];
                    if(i > 1 && q)
                        q.plugins = [];
                }
                if(i > 1) {
                    c1.plugins = [];
                    c2.plugins = [];
                    size.height += 35;
                } else {
                    size.height += 60;
                }
                c1.itemId = 'coins1_' + i;
                c1.tabIndex = tabindex++;
                column1.push(c1);
                if(!trainingboards) {
                    q.itemId = 'queen_' + i;
                    q.tabIndex = tabindex++;
                    column2.push(q);
                }
                c2.itemId = 'coins2_' + i;
                c2.tabIndex = tabindex++;
                column3.push(c2);
                c1.listeners = {
                    change: {
                        fn: me.recomputeScores,
                        scope: me
                    }
                };
                c2.listeners = {
                    change: {
                        fn: me.recomputeScores,
                        scope: me
                    }
                };
                if(!trainingboards)
                    q.listeners = {
                        change: {
                            fn: me.recomputeScores,
                            scope: me
                        }
                    };
            } else break;
        }
        editors.score1.tabIndex = tabindex++;
        editors.score2.tabIndex = tabindex++;
        editors.score1.itemId = 'score1';
        editors.score2.itemId = 'score2';
        column1.push(editors.score1);
        column3.push(editors.score2);

        form = Ext.create('MP.form.Panel', {
                autoScroll: true,
                fieldDefaults: {
                    labelWidth: 40,
                    margin: '15 10 0 10'
                },
                items: [{
                    xtype: 'container',
                    layout: 'hbox',
                    items: [{
                        xtype: 'container',
                        layout: 'anchor',
                        flex: 1,
                        items: column1
                    }, column2 !== null ? {
                        xtype: 'container',
                        layout: 'anchor',
                        width: 210,
                        items: column2
                    } : null, {
                        xtype: 'container',
                        layout: 'anchor',
                        flex: 1,
                        items: column3
                    }]
                }],
                buttons: [{
                    text: _('Cancel'),
                    handler: function() {
                        win.close();
                    }
                }, {
                    text: _('Confirm'),
                    formBind: true,
                    handler: function() {
                        if(form.isValid()) {
                            form.updateRecord(record);
                            win.close();
                            Ext.create("MP.window.Notification", {
                                position: 't',
                                width: 260,
                                title: _('Changes have been applied…'),
                                html: _('Your changes have been applied <strong>locally</strong>.<br/><br/>To make them permanent you must click on the <blink>Save</blink> button.'),
                                iconCls: 'info-icon'
                            }).show();
                        }
                    }
                }]
            });

        me.matchEditForm = form;

        win = desktop.createWindow({
            id: 'edit-match-win',
            title: record.get('description'),
            iconCls: me.module.iconCls,
            width: size.width,
            height: size.height,
            modal: true,
            items: form,
            closable: false,
            minimizable: false,
            maximizable: false,
            resizable: false
        });

        form.loadRecord(record);

        win.show();
    }
});
