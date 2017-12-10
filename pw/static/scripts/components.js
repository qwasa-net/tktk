"use strict";

Vue.component('timeliner', {
    data: function() {
        return {
            tm: null,
            pc: 0,
            c: 10,
            s: 21,
            step: 100 / (10 * 21)
        };
    },
    mounted: function() {},
    methods: {
        start: function(c, a) {
            this.c = c || 10;
            this.pc = a || 0;
            this.tm = setInterval(ev => { this.tix(); }, (1000 / this.s));
            this.step = 100 / (this.c * this.s);
        },
        set: function(a) {
            this.pc = a || 0;
        },
        stop: function() {
            if (this.tm) {
                clearInterval(this.tm);
                this.tm = null;
            }
        },
        tix: function() {
            let v0 = Math.floor(this.pc);
            this.pc += this.step;
            if (v0 != Math.floor(this.pc)) {
                this.$emit('next', this.pc);
            }
            if (this.pc >= 100) {
                this.stop();
                this.pc = 100;
            }
        }
    },
    template: "<div class='timeliner stripedv'><div class='tl_p' v-bind:style=\"'width: ' + pc + '%;'\"></div></div>"
});

Vue.component('popbutton', {
    props: ['text', 'value', 'popdelay', 'getfocus'],
    data: function() {
        return {
            on: true,
            disabled: false,
            klass: []
        };
    },
    mounted: function() {
        if (this.popdelay) {
            this.klass.push('hidden');
            setTimeout(ev => { this.showme(); }, (this.popdelay == '?') ? (500 + Math.random() * 500) : this.popdelay);
        }
        if (this.getfocus) {
            this.$el.focus();
        }
    },
    methods: {
        clicked: function() {
            if (!this.disabled) {
                let payload = { value: this.value, me: this };
                this.$emit('clicked', payload);
            }
        },
        set_state: function(state, old, delay) {
            if (delay) {
                setTimeout(ev => { this.set_state(state, old, null); }, (delay == '?') ? (Math.random() * 500) : delay);
                return;
            }
            if (old) {
                this.klass = this.klass.filter(e => { return e != old; }, this.klass);
            }
            if (state) {
                this.klass.push(state);
            }
        },
        disable: function() {
            this.disabled = true;
            this.klass.push('disabled');
        },
        showme: function() {
            this.klass = this.klass.filter(e => { return e != 'hidden'; }, this.klass);
        },
        hideme: function(killme, delay) {
            if (delay) {
                setTimeout(ev => { this.hideme(false, killme); },
                    (delay == '?') ? (Math.random() * 500) : delay);
            } else {
                this.klass.push('hidden');
                this.on = !killme;
            }
        }
    },
    template: "<button v-if='on' v-on:click='clicked' v-bind:class='klass.join(\" \")'>{{ text }}</button>"
});


Vue.component('triploid', {
    props: ['a', 'b', 'c'],
    data: function() {
        return {
            klass: []
        };
    },
    created: function() {},
    methods: {
        set: function(a, b, c, delay) {
            if (delay) {
                setTimeout(ev => { this.set(a, b, c, null); },
                    (delay == '?') ? (Math.random() * 500) : delay);
                return;
            }
            if (a) {
                this.a = a;
            }
            if (b) {
                this.b = b;
            }
            if (c) {
                this.c = c || this.c;
            }
        },
        set_state: function(state, old, delay) {
            if (delay) {
                setTimeout(ev => { this.set_state(state, old, null); },
                    (delay == '?') ? (Math.random() * 500) : delay);
                return;
            }
            if (old) {
                this.klass = this.klass.filter(e => { return e != old; }, this.klass);
            }
            if (state) {
                this.klass.push(state);
            }
        },
    },
    template: "<div class='triploid' v-bind:class='klass.join(\" \")'><span class='a3'>{{a}}</span><span class='b3'>{{b}}</span><span class='c3'>{{c}}</span></div>"
});
