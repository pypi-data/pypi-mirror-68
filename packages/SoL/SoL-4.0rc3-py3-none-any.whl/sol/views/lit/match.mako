## -*- coding: utf-8 -*-
## :Project:   SoL
## :Created:   mar 28 apr 2020, 08:50:19
## :Author:    Lele Gaifax <lele@metapensiero.it>
## :License:   GNU General Public License version 3 or later
## :Copyright: © 2020 Lele Gaifax
##

<%inherit file="base.mako" />

<%def name="header()">
  <h1 class="title centered">${self.title()}</h1>
  <h2 class="title centered">
    <a href="${request.route_path('lit_tourney', guid=tourney.guid) | n}" target="_blank">
      ${tourney.description}
    </a>,
    ${_('round $round', mapping=dict(round=currentturn))},
    ${_('board $board', mapping=dict(board=match.board))}
  </h2>
</%def>

<%def name="footer()">
</%def>

<%def name="title()">
  ${match.caption(html=False)}
</%def>

<%def name="fui_css()">
  ${parent.fui_css()}
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-button.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-form.css" />
  <link rel="stylesheet" type="text/css" href="/static/css/fomantic-ui-message.css" />
  <style type="text/css">
   h1.centered.title {
       font-size: 2em;
   }
   h2.centered.title {
       font-size: 1.6em;
   }
   input[type="number"] {
       text-align: center;
   }
   .ui.large.celled.table > thead > tr:first-child th:first-child,
   .ui.large.celled.table > thead > tr:first-child th:last-child {
       background: #bcbdbd;
   }
   @media only screen and (max-width: 1000px) and (orientation: portrait) {
       h1.centered.title {
           font-size: 3em;
       }
       h2.centered.title {
           font-size: 2em;
   }
       .ui.compact.definition.table, .ui.large.celled.table {
           font-size: 2.4em;
       }
   }
   .ui.large.celled.table td {
       padding: 10px;
   }
   input[type='radio'] {
       transform: scale(3);
   }
  </style>
</%def>

## Body

<form class="ui center aligned form${' error' if error else ''}" method="POST">
  <input type="hidden" name="turn" value="${tourney.currentturn}">
  <input type="hidden" name="score1" value="${match.score1}">
  <input type="hidden" name="score2" value="${match.score2}">
  <table class="ui large celled table">
    <thead>
      <tr>
        <th class="center aligned" colspan="4" width="50%">
          % if not match.breaker:
            <div class="checker">
              <div class="ui radio checkbox" title="${_('Break')}">
                <input type="radio" name="breaker" value="1">
              </div>
              <br/>
            </div>
          % endif
          ${match.competitor1.caption()|n}
        </th>
        <th class="center aligned" colspan="4" width="50%">
          % if not match.breaker:
            <div class="checker">
              <div class="ui radio checkbox" title="${_('Break')}">
                <input type="radio" name="breaker" value="2">
              </div>
              <br/>
            </div>
          % endif
          ${match.competitor2.caption()|n}
        </th>
      </tr>
      <tr>
        <th class="center aligned">Score</th>
        <th class="center aligned">${_('Coins')}</th>
        <th class="center aligned collapsing">Q</th>
        <th class="center aligned collapsing" colspan="2">#</th>
        <th class="center aligned collapsing">Q</th>
        <th class="center aligned">${_('Coins')}</th>
        <th class="center aligned">Score</th>
      </tr>
    </thead>

    <tbody>
      % for board in match.boards:
        <%
        if match.breaker:
            if match.breaker == '1':
                if board.number % 2:
                    c1_break = "left marked red"
                    c2_break = ""
                else:
                    c1_break = ""
                    c2_break = "right marked red"
            else:
                if board.number % 2:
                    c1_break = ""
                    c2_break = "right marked red"
                else:
                    c1_break = "left marked red"
                    c2_break = ""
        else:
            c1_break = c2_break = ""
        %>
        <tr id="board_${board.number}">
          <td class="center aligned ${c1_break}" id="score_${board.number}_1"></td>
          <td class="center aligned">
            <input type="number" name="coins_${board.number}_1"
                   min="0" max="12"
                   value="${board.coins1 or 0}" style="max-width:60px;">
          </td>
          <td class="collapsing">
            <div class="ui radio fitted checkbox center aligned" id="cb_queen_1_${board.number}">
              <input type="radio" name="queen_${board.number}" value="1"${' checked' if board.queen == '1' else ''}>
            </div>
          </td>
          <td class="grey center aligned collapsing" colspan="2">${board.number}</td>
          <td class="collapsing">
            <div class="ui radio fitted checkbox center aligned" id="cb_queen_2_${board.number}">
              <input type="radio" name="queen_${board.number}" value="2"${' checked' if board.queen == '2' else ''}>
            </div>
          </td>
          <td class="center aligned">
            <input type="number" name="coins_${board.number}_2"
                   min="0" max="12"
                   value="${board.coins2 or 0}" style="max-width:60px;">
          </td>
          <td class="center aligned ${c2_break}" id="score_${board.number}_2"></td>
        </tr>
      % endfor
      <tr>
        <td class="center aligned" id="total_1"></td>
        <td colspan="6" class="center aligned">
          <div class="ui buttons">
            <button class="ui center aligned primary massive${'' if match.breaker else ' disabled'} button" type="button">
              ${_('New board') if match.boards else _('Start game')}
            </button>
            <button class="ui center aligned positive massive disabled button" name="endgame">
              ${_('End game')}
            </button>
          </div>
        </td>
        <td class="center aligned" id="total_2"></td>
      </tr>
    </tbody>
  </table>
</form>

<script src="/static/jquery-3.5.1.min.js"></script>
<script src="/static/fomantic-ui-checkbox.js"></script>

<script>
 function add_board(number) {
     var breaker = "${match.breaker or '0'}", c1_break = "", c2_break = "";
     if(breaker === '0') {
         if($('input[name="breaker"][value="1"]').prop('checked'))
             breaker = '1';
         else if ($('input[name="breaker"][value="2"]').prop('checked'))
             breaker = '2';
     }
     if(breaker !== '0') {
         if(breaker === '1') {
             if(number % 2) {
                 c1_break = "left marked red";
                 c2_break = "";
             } else {
                 c1_break = "";
                 c2_break = "right marked red";
             }
         } else {
             if(number % 2) {
                 c1_break = "";
                 c2_break = "right marked red";
             } else {
                 c1_break = "left marked red";
                 c2_break = "";
             }
         }
     };

     var tr = `
  <tr id="board_<%text>${number}</%text>">
    <td class="center aligned<%text> ${c1_break}</%text>" id="score_<%text>${number}</%text>_1"></td>
    <td class="center aligned">
      <div class="field">
        <input type="number" name="coins_<%text>${number}</%text>_1" min="0" max="9" style="max-width:60px;">
      </div>
    </td>
    <td class="collapsing">
      <div class="field">
        <div class="ui radio checkbox center aligned" id="cb_queen_<%text>${number}</%text>_1">
          <input type="radio" name="queen_<%text>${number}</%text>" value="1">
        </div>
      </div>
    </td>
    <td class="grey center aligned collapsing" colspan="2"><%text>${number}</%text></td>
    <td class="collapsing">
      <div class="field">
        <div class="ui radio checkbox center aligned" id="cb_queen_<%text>${number}</%text>_2">
          <input type="radio" name="queen_<%text>${number}</%text>" value="2">
        </div>
      </div>
    </td>
    <td class="center aligned">
      <div class="field">
        <input type="number" name="coins_<%text>${number}</%text>_2" min="0" max="9" style="max-width:60px;">
      </div>
    </td>
    <td class="center aligned<%text> ${c2_break}</%text>" id="score_<%text>${number}</%text>_2"></td>
  </tr>`;
     $('form > table > tbody > tr').eq(number-1).before(tr);
     $('tbody input[name="coins_' + number + '_1"], tbody input[name="coins_' + number + '_2"], tbody input[name="queen_' + number +'"]')
         .keyup(function() {compute_scores_and_totals(parseInt($(this).attr('name').split('_')[1]));})
         .change(function() {compute_scores_and_totals(parseInt($(this).attr('name').split('_')[1]));});
     $('div.checker').hide();
     $('button.ui.center.aligned.primary.button')
         .text("${_('New board')}")
         .addClass('disabled');
 };

 function compute_scores_and_totals(board) {
     var $coins_1 = $('input[name="coins_' + board + '_1"]'),
         $coins_2 = $('input[name="coins_' + board + '_2"]'),
         $score_1 = $('#score_' + board + '_1'),
         $score_2 = $('#score_' + board + '_2'),
         boards = $('form > table > tbody > tr').length - 1,
         coins_1 = $coins_1.val(),
         coins_2 = $coins_2.val(),
         score_1, score_2,
         total_1, total_2;
     if(coins_1 !== '' && coins_1 !== '0') {
         coins_2 = '0';
         $('input[name="coins_' + board + '_2"]').val('0');
     }
     if(coins_2 !== '' && coins_2 !== '0') {
         coins_1 = '0';
         $('input[name="coins_' + board + '_1"]').val('0');
     }
     total_1 = $score_1.data('total') || 0;
     total_2 = $score_2.data('total') || 0;
     score_1 = parseInt(coins_1) || 0;
     score_2 = parseInt(coins_2) || 0;
     if(score_1 > 9) {
         $coins_1.parent().addClass('error');
     } else {
         $coins_1.parent().removeClass('error');
     }
     if(score_2 > 9) {
         $coins_2.parent().addClass('error');
     } else {
         $coins_2.parent().removeClass('error');
     }
     if(score_1 > 9 || score_2 > 9) {
         $('button.ui.center.aligned.primary.button').addClass('disabled');
         $('button.ui.center.aligned.positive.button').addClass('disabled');
         return;
     } else {
         $('button.ui.center.aligned.primary.button').removeClass('disabled');
         $('button.ui.center.aligned.positive.button').removeClass('disabled');
     }
     if(coins_1 !== '' && coins_2 !== '') {
         if(score_1 > score_2
            && total_1 < 22
            && $('input[name="queen_' + board + '"][value="1"]').prop('checked'))
             score_1 += 3;
         if(score_1 < score_2
            && total_2 < 22
            && $('input[name="queen_' + board + '"][value="2"]').prop('checked'))
             score_2 += 3;
         if(score_1 > score_2) {
             $('#score_' + board + '_1').addClass('positive');
             $('#score_' + board + '_1').removeClass('negative');
             $('#score_' + board + '_2').addClass('negative');
             $('#score_' + board + '_2').removeClass('positive');
         } else if(score_1 < score_2) {
             $('#score_' + board + '_1').addClass('negative');
             $('#score_' + board + '_1').removeClass('positive');
             $('#score_' + board + '_2').addClass('positive');
             $('#score_' + board + '_2').removeClass('negative');
         } else {
             $('#score_' + board + '_1').addClass('positive');
             $('#score_' + board + '_1').removeClass('negative');
             $('#score_' + board + '_2').addClass('positive');
             $('#score_' + board + '_2').removeClass('negative');
         }
     }
     $('#score_' + board + '_1').text(score_1);
     $('#score_' + board + '_2').text(score_2);

     total_1 = 0;
     total_2 = 0;
     for(var i = 1; i <= boards; i++) {
         var $score;

         $score = $('#score_' + i + '_1');
         $score.data('total', total_1);
         score = $score.text();
         if(score !== '') {
             total_1 += parseInt(score);
             if(total_1 > 25) total_1 = 25;
         }

         $score = $('#score_' + i + '_2');
         $score.data('total', total_2);
         score = $score.text();
         if(score !== '') {
             total_2 += parseInt(score);
             if(total_2 > 25) total_2 = 25;
         }
     }

     $('#total_1').html(`<big><strong><%text>${total_1}</%text></strong></big>`);
     $('#total_2').html(`<big><strong><%text>${total_2}</%text></strong></big>`);
     $('input[name="score1"]').val(total_1);
     $('input[name="score2"]').val(total_2);

     if(total_1 > total_2) {
         $('#total_1').addClass('positive');
         $('#total_1').removeClass('negative');
         $('#total_2').addClass('negative');
         $('#total_2').removeClass('positive');
     } else if(total_1 < total_2) {
         $('#total_1').addClass('negative');
         $('#total_1').removeClass('positive');
         $('#total_2').addClass('positive');
         $('#total_2').removeClass('negative');
     } else {
         $('#total_1').addClass('positive');
         $('#total_1').removeClass('negative');
         $('#total_2').addClass('positive');
         $('#total_2').removeClass('negative');
     }

     var q1 = $('input[name="queen_' + boards + '"][value="1"]').prop('checked'),
         q2 = $('input[name="queen_' + boards + '"][value="2"]').prop('checked');

     if((q1 || q2)
        && ((score_1 && score_2 == 0) || (score_1 == 0 && score_2))
        && boards < 9 && total_1 < 25 && total_2 < 25) {
         $('button.ui.center.aligned.primary.button').removeClass('disabled');
     } else {
         $('button.ui.center.aligned.primary.button').addClass('disabled');
     }
 };

 $(document).ready(function() {
     $('.checkbox').checkbox();
     $('button.ui.center.aligned.primary.button').click(function() {
         var board = $('form > table > tbody > tr').length,
             c1 = $('input[name="coins_' + (board - 1) + '_1"]').val(),
             c2 = $('input[name="coins_' + (board - 1) + '_2"]').val(),
             t1 = $('#total_1').text(),
             t2 = $('#total_2').text(),
             q1 = $('input[name="queen_' + (board - 1) + '"][value="1"]').prop('checked'),
             q2 = $('input[name="queen_' + (board - 1) + '"][value="2"]').prop('checked');
         if(board == 1
            || (board < 10
                && (c1 || c2)
                && parseInt(c1) < 10
                && parseInt(c2) < 10
                && (q1 || q2)
                && parseInt(t1) < 25
                && parseInt(t2) < 25)) {
             var $form = $('form.ui.form'),
                 data = $form.serialize(),
                 method = $form.attr('method'),
                 url = document.URL;
             $.ajax({
                 method: method,
                 url: url,
                 data: data
             }).done(function(result) {
                 if(!result.success) {
                     alert(result.message);
                 }
             });
             add_board(board);
         }
     });
     $('thead .checkbox').change(function() {
         $('button.ui.center.aligned.primary.button').removeClass('disabled');
     });
     for(var board=1, boards=$('form > table > tbody > tr').length - 1; board <= boards; board++) {
         compute_scores_and_totals(board);
         $('tbody input[name="coins_' + board + '_1"], tbody input[name="coins_' + board + '_2"], tbody input[name="queen_' + board +'"]')
             .keyup(function() {compute_scores_and_totals(parseInt($(this).attr('name').split('_')[1]));})
             .change(function() {compute_scores_and_totals(parseInt($(this).attr('name').split('_')[1]));});
     }
 });
</script>
