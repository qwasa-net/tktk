"use strict";

var GAME_URL = "tktk.json";
var EXIT_URL = "exit";
var PANIC_URL = "/?kernel-panic";

var tktk = {

    gb: {}, // gameboard elements

    games: null, // tasks and answers

    config: { 'auto_next': false, 'auto_next_delay': 900, 'butsize': 'large' },
    base_url: '/tktk/',

    game_isrunning: false,

    tm_next_task: null,
    tm_tixer: null,

    score: 0, // game score

    tix: 0, // ticks counter
    task_tix: 0, // task ticks max
    task_tix_limit: 25, // task time limit
    game_start_ts: null, // game start timestamp
    game_end_ts: null, // game start timestamp

    //
    init: function () {

        //
        var url = window.location.toString();
        if (url[url.length - 1] != '/') {
            url += "/";
        }
        tktk.base_url = url;
    },

    start: function () {
        tktk.load();
        window.onkeydown = tktk.key_down;
        window.onkeyup = tktk.key_up;
    },

    //
    build: function () {

        tktk.gb.container = document.getElementById('gboard_container');
        tktk.gb.container.innerHTML = '';

        // [board]
        tktk.gb.board = document.createElement('div');
        tktk.gb.board.setAttribute('id', 'gboard');
        tktk.gb.board.style.visibility = 'hidden';
        tktk.gb.container.appendChild(tktk.gb.board);

        // task holder = [ [iline] [task] ]
        var task_holder = div_holder('task_holder', null, null);

        // [iline]
        tktk.gb.iline = document.createElement('div');
        tktk.gb.iline.setAttribute('id', 'iline');
        task_holder.div.appendChild(tktk.gb.iline);

        tktk.gb.score = div_holder_parts('w33 lblcnt', 'score', 3, ['счёт:', '', '']);
        tktk.gb.iline.appendChild(tktk.gb.score.div);

        tktk.gb.gprgrss = div_holder_parts('w33 lblcnt', 'gprgrss', 3, ['вопрос:', '', '']);
        tktk.gb.iline.appendChild(tktk.gb.gprgrss.div);

        tktk.gb.clock = div_holder_parts('w33 lblcnt', 'gprgrss', 2, ['время:', '', '00:00']);
        tktk.gb.iline.appendChild(tktk.gb.clock.div);

        // [task]
        tktk.gb.task = document.createElement('div');
        tktk.gb.task.setAttribute('id', 'task');
        tktk.gb.task.setAttribute('class', tktk.config.butsize);
        task_holder.div.appendChild(tktk.gb.task);

        // 
        tktk.gb.board.appendChild(task_holder.div);

        // answers holder = [ [aprgrss] [answs] ]
        var answs_holder = div_holder('answs_holder', null, null);

        tktk.gb.aprgrss = div_holder_parts('w55 lblcnt', 'aprgrss', 3, ['ответов:', '', '']);
        answs_holder.div.appendChild(tktk.gb.aprgrss.div);

        //
        tktk.gb.answs = document.createElement('div');
        tktk.gb.answs.setAttribute('id', 'answs');
        answs_holder.div.appendChild(tktk.gb.answs);

        tktk.gb.board.appendChild(answs_holder.div);

        // buts = [[sound-ctl] [next] [help]]
        tktk.gb.buts = document.createElement('div');
        tktk.gb.buts.setAttribute('id', 'buts');

        tktk.gb.timeline = timeliner();
        tktk.gb.buts.appendChild(tktk.gb.timeline.div);

        tktk.gb.next_but = abutton("next", "дальше", tktk.next_task, null,
            "primary pocus striped8 " + tktk.config.butsize);
        tktk.gb.next_but.hide(true);
        tktk.gb.buts.appendChild(tktk.gb.next_but.div);

        tktk.gb.exit_but = abutton("next", "закончить", tktk.next_task, null,
            "gold pocus striped8 " + tktk.config.butsize);
        tktk.gb.exit_but.hide(true);
        tktk.gb.buts.appendChild(tktk.gb.exit_but.div);

        var butsleft_holder = div_holder('onleft', null, null);
        tktk.gb.buts.appendChild(butsleft_holder.div);

        tktk.gb.buts.style.visibility = 'hidden';
        tktk.gb.board.appendChild(tktk.gb.buts);

    },

    //
    load: function () {

        var url = tktk.base_url + GAME_URL + "?" + Math.random();
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = this.xhr_handler;
        xhr.open('GET', url);
        xhr.send(null);

    },

    xhr_handler: function () {

        var rc = false;
        var data = null;
        if (this.readyState !== 4) {
            return;
        }

        if (this.status !== 200) {
            console.log("@xhr_handler: oops! " + this.status + "/" + this.statusText);
            // window.location = PANIC_URL;
            return;
        }

        try {
            data = JSON.parse(this.response);
            rc = tktk.parse(data);
        } catch (e) {
            console.log("@xhr_handler: oops! " + e.toString());
            // window.location = PANIC_URL;
            return;
        }

        if (rc) {
            tktk.start_game();
        }
    },

    //
    parse: function (data) {
        tktk.games = data.games;
        tktk.board_id = data.board_id;
        tktk.board_pin = data.board_pin;
        //tktk.config = data.config || {'butsize': 'large'};

        if (data.config) {
            for (var k in data.config) {
                tktk.config[k] = data.config[k];
            }
        }

        return true;
    },

    //
    start_game: function () {

        tktk.build();

        // 1st task
        tktk.task_idx = 0;
        tktk.task = tktk.games[tktk.task_idx];

        // timestamp
        tktk.game_start_ts = (new Date()).getTime();

        //
        tktk.score = 0;
        tktk.gb.gprgrss.parts[2].textContent = "из " + tktk.games.length;

        // time starts
        tktk.tixer_start();

        // show something
        if (tktk.config && tktk.config.xxl) {
            tktk._bsizes = "huge";
        }

        tktk.gb.board.style.visibility = 'visible';
        tktk.show_task();

    },

    clear_board: function () {

        tktk.gb.next_but.hide(true);
        tktk.gb.next_but.disable();
        tktk.gb.buts.style.visibility = 'hidden';

        tktk.gb.task.classList.remove('done');
        tktk.gb.answs.classList.remove('done');

        tktk.reset_update_score();

        while (tktk.gb.task.firstChild) {
            tktk.gb.task.removeChild(tktk.gb.task.firstChild);
        }

        tktk.gb.answs_buts = [];
        while (tktk.gb.answs.firstChild) {
            tktk.gb.answs.removeChild(tktk.gb.answs.firstChild);
        }

        tktk.ans_focus = null;

    },

    //
    show_task: function () {

        var g = tktk.task;
        var i = 0;

        tktk.clear_board();

        tktk.gb.task.innerHTML = g.task;

        var l = g.answs.length;
        for (i = 0; i < l; i++) {

            var iamc = tktk.task.correct.indexOf(i) >= 0;
            var btn = abutton(i, g.answs[i], tktk.answ_clicked, iamc,
                "default pocus striped8 " + tktk.config.butsize);

            btn.fancy_show((i + 3) * (500 / l));

            tktk.gb.answs_buts.push(btn);
            tktk.gb.answs.appendChild(btn.div);
        }

        tktk.gb.buts.style.visibility = 'visible';

        tktk.answered = 0;
        tktk.answered_incorrect = 0;
        tktk.answered_correct = 0;
        tktk.task_tix = 0;

        tktk.answers = g.answs.length;
        tktk.answers_correct = g.correct.length;
        tktk.answers_incorrect = g.answs.length - g.correct.length;

        tktk.game_isrunning = true;

        tktk.gb.timeline.start(100, 0, tktk.task_tix_limit);

        tktk.gb.aprgrss.parts[2].textContent = "из " + tktk.task.correct.length;

        tktk.update_status();
        tktk.ping();
    },

    tixer_start: function () {
        tktk.tix = 0;
        tktk.tm_tixer = setInterval(tktk.tixer, 120);
    },

    //
    tixer: function () {

        tktk.tix++;
        tktk.task_tix++;

        var now = (new Date()).getTime();
        var tsdiff = now - tktk.game_start_ts;

        var m = ((tsdiff / (1000 * 60)) % 100) | 0;
        var s = ((tsdiff / 1000) % 60) | 0;
        var tl_label = zero_pad(m, 2) + " : " + zero_pad(s, 2);

        tktk.gb.clock.parts[1].textContent = tl_label;

        if (tktk.update_score_timer === null) {
            tktk.gb.score.parts[2].textContent = tktk.points_now();
        }

    },

    update_score: function (points) {

        tktk.score += points;

        var sp = tktk.gb.score.parts[2];

        if (points > 0) {
            sp.textContent = "+" + points;
            sp.classList.remove('wrong');
            sp.classList.add('correct');
        } else {
            sp.textContent = points;
            sp.classList.remove('correct');
            sp.classList.add('wrong');
        }

        if (tktk.update_score_timer) {
            clearTimeout(tktk.update_score_timer);
        }

        tktk.update_score_timer = setTimeout(tktk.reset_update_score, 2500);

    },

    reset_update_score: function () {
        tktk.update_score_timer = null;
        tktk.gb.score.parts[2].classList.remove('wrong');
        tktk.gb.score.parts[2].classList.remove('correct');
        tktk.gb.score.parts[2].textContent = tktk.points_now();
    },

    points_now: function () {
        var t = tktk.gb.timeline.x | 1;
        return (t > 0) ? t : 1;
    },

    //
    ping: function () {
    },

    //
    pong: function () {
    },

    //
    update_status: function () {

        tktk.gb.score.parts[1].textContent = tktk.score;
        tktk.gb.aprgrss.parts[1].textContent = tktk.answered_correct;
        tktk.gb.gprgrss.parts[1].textContent = (tktk.task_idx + 1);

    },

    //
    answ_clicked: function (e, o) {

        if (!tktk.game_isrunning) {
            return;
        }

        o.disable();
        o.blur_focus();
        var bid = o.id;

        var points = tktk.points_now();

        if (bid !== null) {

            if (o.value) {

                o.change_state("success");
                tktk.update_score(points);
                tktk.answered_correct += 1;

            } else {

                o.change_state("danger");
                tktk.update_score(-points);
                tktk.answered_incorrect += 1;

            }

            tktk.answered += 1;

        }

        tktk.update_status();

        var r = tktk.task.correct.length - tktk.answered_correct;

        if (r <= 0) {
            tktk.finish_task();
        }

    },

    ans_focus: null,

    //
    finish_task: function () {

        tktk.game_isrunning = false;

        tktk.gb.task.classList.add('done');
        tktk.gb.answs.classList.add('done');
        tktk.gb.timeline.stop();

        // disable answers
        for (var i = 0; i < tktk.gb.answs_buts.length; i++) {
            if (!tktk.gb.answs_buts[i].value) {
                tktk.gb.answs_buts[i].fancy_fade();
            }
        }

        var last_task = (tktk.task_idx >= tktk.games.length - 1);

        if (!last_task && tktk.config['auto_next']) {
            tktk.tm_next_task = setTimeout(tktk.next_task,
                tktk.config['auto_next_delay'] || 750);

        } else {

            // show [next] button
            var nb = last_task ? tktk.gb.exit_but : tktk.gb.next_but;
            nb.onclick(tktk.next_task);
            nb.fancy_show(1100, true);
            tktk.tm_next_task = setTimeout(tktk.next_task, 15000);
        }

    },

    //
    next_task: function () {

        if (tktk.tm_next_task) {
            clearTimeout(tktk.tm_next_task);
            tktk.tm_next_task = null;
        }

        tktk.task_idx++;

        if (tktk.task_idx < tktk.games.length) {
            tktk.task = tktk.games[tktk.task_idx];
            tktk.show_task();
        } else {
            tktk.finish();
        }


    },

    //
    finish: function () {

        if (tktk.tm_tixer) {
            clearInterval(tktk.tm_tixer);
        }

        tktk.gb.exit_but.disable();
        tktk.exit();

    },

    //
    exit: function () {

        var XHR = new XMLHttpRequest();

        var form = new FormData();
        form.append('score', tktk.score);
        form.append('board_id', tktk.board_id);
        form.append('board_pin', tktk.board_pin);
        form.append('user_name', hello.my_name_is());
        form.append('user_uid', hello.my_uid_is());

        XHR.addEventListener('load', function (event) {
            if (event.target.status === 200) {
                var abc = event.target.response.substring(0, 3);
                var url = event.target.response.substring(3);
                if (abc == "OK!") {
                    window.location = url;
                } else {
                    window.location = PANIC_URL;
                }
            } else {
                window.location = PANIC_URL;
            }
        });

        XHR.addEventListener('error', function (event) {
            window.location = PANIC_URL;
        });

        var url = tktk.base_url + EXIT_URL
        XHR.open('POST', url);
        XHR.send(form);

    },

    key_up: function (ev) {

        // on stopped game move focus to NEXT button on any key pressed
        if (!tktk.game_isrunning) {
            if (!tktk.gb.next_but.has_focus()) {
                tktk.gb.next_but.get_focus();
                return (ev.keyCode !== 32 && ev.keyCode !== 13);
            }
            return true;
        }
    },

    key_down: function (ev) {

        if (ev.ctrlKey || ev.shiftKey || ev.altKey) {
            return true;
        }

        if (!tktk.game_isrunning) {
            return true;
        }

        var dir = 0;

        if (ev.keyCode === 38 || ev.keyCode === 37 || ev.keyCode === 34) {
            // ← ↑ pgup
            dir = -1;
        } else if (ev.keyCode === 40 || ev.keyCode === 39 || ev.keyCode === 33) {
            // → ↓ pgdn
            dir = 1;
        }

        if (dir === 0) {
            return true;
        }

        // any arrow for empty screen — focus on first element
        if (tktk.ans_focus === null) {
            tktk.ans_focus = 0;
        } else {

            // move focus back or forward
            tktk.ans_focus += dir;

            // stay in limits
            if (tktk.ans_focus < 0) {
                tktk.ans_focus = tktk.task.answs.length - 1;
            } else if (tktk.ans_focus >= tktk.task.answs.length) {
                tktk.ans_focus = 0;
            }
        }

        // set focus on button
        tktk.gb.answs_buts[tktk.ans_focus].get_focus();
        return false;

    }
};

function zero_pad(n, l) {
    return n.toString().padStart(l, '00000000000');
}
