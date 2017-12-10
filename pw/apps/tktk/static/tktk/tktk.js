"use strict";

var TKTKEngine = new Vue({

    el: '#tktk_container',

    data: {

        config: {
            'auto_next': false,
            'auto_next_delay': 3000,
            'gamesize': 'large'
        },

        games: [], // list of tasks
        task: null, // current task
        score: 0, // game score
        points_now: 0, // active points at the moment

        state: null, // state of the game
        task_isrunning: false, // state of the task, check details in task.state, if available

        tix: 0, // global game ticks counter

        TASK_TIME_LIMIT: 25, // task time limit, seconds
        TIXER_STEP: 3, // 333ms

        tm_tixer: null, // global game timer
        tm_next_task: null, // go to next task timer
        tm_update_score: null, // score updater timer

        game_start_ts: null, // game start timestamp
        game_end_ts: null, // game start timestamp

        score_super_label: '', // fancy text label the active score
        game_time_label: '', // time
        explanation_text: '', // answer explanation

        ans_keyfocus: null, // active answer index for keyboard control

        GAME_URL: "tktk.json", // URLS
        EXIT_URL: "exit",
        PANIC_URL: "/?kernel-panic",

        SOUNDMAN_PATH: '/st/s/s', // sound settings
        SOUNDMAN_SIZE: 5,
    },

    mounted: function() {
        this.init();
        this.$el.classList.remove('invisible');
    },

    methods: {

        //
        init: function() {
            this.state = 'loading';
            this.base_url = window.location.toString();
            if (this.base_url.substr(-1) != '/') this.base_url += '/';

            let url = this.base_url + this.GAME_URL + "?" + Math.random();

            axios.get(url).then(response => {
                this.parse(response.data);
                this.start_game();
            }, error => {
                window.location = this.PANIC_URL;
            });

            if (typeof soundman !== "undefined") {
                soundman.load(this.SOUNDMAN_SIZE, this.SOUNDMAN_PATH);
            }

            window.onkeydown = this.key_down;
            window.onkeyup = this.key_up;
        },

        //
        mounted: function() {},

        //
        parse: function(data) {
            this.games = data.game.data;
            this.board_id = data.id;
            this.board_pin = data.pin;
            if (data.game.config) {
                for (var k in data.game.config) {
                    this.config[k] = data.game.config[k];
                }
            }
            this.state = 'parsed';
        },

        //
        start_game: function() {
            this.task_idx = 0;
            this.score = 0;
            this.game_start_ts = (new Date()).getTime();
            this.state = 'running';
            this.tixer_start();
            this.show_task();
        },

        //
        show_task: function() {

            let t0 = this.games[this.task_idx];
            this.task = {};
            this.task.answered = 0;
            this.task.answered_incorrect = 0;
            this.task.answered_correct = 0;
            this.task.tix = 0;
            this.task.status = 'running';

            this.task.task = t0.task;
            this.task.corrects = 0;
            this.task.answs = [];

            this.ans_keyfocus = null;

            for (let i = 0; i < t0.answs.length; i++) {
                this.task.answs.push({
                    text: t0.answs[i][0],
                    explain: t0.answs[i][1] || "",
                    correct: t0.answs[i][2],
                    idx: i,
                    key: i + this.task_idx * 1000
                });
                if (t0.answs[i][2]){
                    this.task.corrects++;
                }
            }

            this.task_isrunning = true;
            this.$refs.tl.start(this.TASK_TIME_LIMIT);

        },

        //
        answ_clicked: function(msg) {

            if (!this.task_isrunning) {
                return;
            }

            let but = msg.value;
            let popper = msg.me;

            if (typeof(but) !== 'undefined') {

                this.task.answered += 1;

                if (this.task.answs[but].correct) {
                    this.update_score(this.points_now);
                    this.task.answered_correct += 1;
                    popper.set_state('success');
                    popper.disable();
                    soundman.play(3);
                } else {
                    this.update_score(-this.points_now);
                    this.task.answered_incorrect += 1;
                    popper.set_state('danger');
                    popper.disable();
                    soundman.play(2);
                }
            }

            if (this.task.answs[but].explain){
                this.explanation_text = this.task.answs[but].explain;
            }

            if (this.task.corrects <= this.task.answered_correct) {
                this.finish_task();
            }
        },

        //
        update_score: function(points) {
            this.score += points;
            if (points > 0) {
                this.$refs.game_score.set_state('good', 'bad');
                this.score_super_label = "+" + points;
            } else {
                this.$refs.game_score.set_state('bad', 'good');
                this.score_super_label = points;
            }
            if (this.tm_update_score) {
                clearTimeout(this.tm_update_score);
            }
            this.tm_update_score = setTimeout(ev => {
                this.$refs.game_score.set_state(null, 'good');
                this.$refs.game_score.set_state(null, 'bad');
                this.score_super_label = "";
                this.explanation_text = "";
                this.tm_update_score = null;
            }, 3500);
        },

        //
        tixer_start: function() {
            this.tix = 0;
            this.tm_tixer = setInterval(ev => { this.tixer(ev); }, 1000 / this.TIXER_STEP);
        },

        //
        tixer_stop: function() {
            if (this.tm_tixer){
                clearInterval(this.tm_tixer);
                this.tm_tixer = null;
            }
        },

        //
        tixer: function() {

            this.tix++;

            if (this.tix % this.TIXER_STEP == 0) {
                let now = (new Date()).getTime();
                let tsdiff = now - this.game_start_ts;
                let m = ((tsdiff / (1000 * 60)) % 100) | 0;
                let s = ((tsdiff / 1000) % 60) | 0;
                this.game_time_label = zero_pad(m, 2) + " : " + zero_pad(s, 2);
            }

            if (this.task && this.task_isrunning) {
                this.task.tix++;
                let x = 100 - Math.floor(100 * (this.task.tix / this.TIXER_STEP) / this.TASK_TIME_LIMIT);
                this.points_now = Math.max(x, 1);
                if (!this.tm_update_score) {
                    this.score_super_label = this.points_now.toString();
                }
            }
        },

        //
        finish_task: function() {

            this.task_isrunning = false;
            this.task.status = 'done';

            // stop timeline
            this.$refs.tl.stop();

            // disable answers
            for (let i = 0; i < this.$refs.answs.length; i++) {
                if (!this.task.answs[this.$refs.answs[i].value].correct) {
                    this.$refs.answs[i].set_state('muted', null, '?');
                }
            }

            let last_task = (this.task_idx >= this.games.length - 1);

            if (!last_task) {
                let next_delay = (this.config['auto_next'] && (this.config['auto_next_delay'] || 750)) || 15000;
                console.log("nxt-delay=", next_delay);
                this.tm_next_task = setTimeout(ev => {this.next_task();}, next_delay);
            } else {
                this.finish();
            }
        },

        //
        next_task: function() {
            if (this.tm_next_task) {
                clearTimeout(this.tm_next_task);
                this.tm_next_task = null;
            }
            this.task_idx++;
            if (this.task_idx < this.games.length) {
                this.task = this.games[this.task_idx];
                this.show_task();
            } else {
                this.finish();
            }

            soundman.play(1);
        },

        //
        finish: function() {
            this.tixer_stop();
            this.state = 'end';
            // this.exit();
        },

        //
        exit: function() {

            var url = this.base_url + this.EXIT_URL;
            var headers = { headers: { 'Content-Type': 'multipart/form-data' } };
            var form = new FormData();
            form.append('score', this.score);
            form.append('id', this.board_id);
            form.append('pin', this.board_pin);

            axios({ method: 'post', url: url, data: form, config: headers })
                .then(function(response) {
                    if (response.data.status == "OK" && response.data.goto) {
                        window.location = response.data.goto;
                    }else {
                        window.location = this.PANIC_URL;
                    }
                })
                .catch(function(response) {
                    window.location = this.PANIC_URL;
                });
        },

        //
        key_up: function(ev) {
            return true;
        },

        //
        key_down: function(ev) {

            if (ev.ctrlKey || ev.shiftKey || ev.altKey) {
                return true;
            }

            if (!this.task_isrunning) {
                return true;
            }

            let dir = 0;
            let key = ev.keyCode;

            if (key === 38 || key === 37 || key === 34) { // ← ↑ pgup
                dir = -1;
            } else if (key === 40 || key === 39 || key === 33) { // → ↓ pgdn
                dir = 1;
            } else {
                return true;
            }

            // any arrow for empty screen — focus on first element
            if (this.ans_keyfocus === null) {
                this.ans_keyfocus = 0;
            } else {
                // move focus back or forward, check limits
                this.ans_keyfocus += dir;
                if (this.ans_keyfocus < 0) {
                    this.ans_keyfocus = this.task.answs.length - 1;
                } else if (this.ans_keyfocus >= this.task.answs.length) {
                    this.ans_keyfocus = 0;
                }
            }
            // set focus on button
            this.$refs.answs[this.ans_keyfocus].$el.focus();

            return false;
        },

        //
        soundonoff: function(ev) {
            if (typeof soundman !== "undefined" && ev.target) {
                soundman.toggle();
                if (soundman.enabled) {
                    ev.target.classList.add('on');
                    ev.target.classList.remove('off');
                } else {
                    ev.target.classList.remove('on');
                    ev.target.classList.add('off');
                }
            }
        },

    }
});

function zero_pad(n, l) {
    return n.toString().padStart(l, '00000000000');
}
