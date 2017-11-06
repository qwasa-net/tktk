/*
 * 
 */
function div_holder(hclass, hid, content) {

    var c = {
        div: null
    };

    c.div = document.createElement('div');

    if (hid) {
        c.div.setAttribute('id', hid);
    }

    if (hclass) {
        c.div.setAttribute('class', hclass);
    }

    if (content) {
        c.div.appendChild(content);
    }

    return c;

}

/*
 * 
 */
function div_holder_parts(hclass, hid, nparts, ninits) {

    var c = {
        div: null,
        parts: []
    };

    var i = 0;

    c.div = document.createElement('div');
    if (hid) {
        c.div.setAttribute('id', hid);
    }
    if (hclass) {
        c.div.setAttribute('class', hclass);
    }

    for (i = 0; i < nparts; i++) {
        var p = document.createElement('span');
        if (hid) {
            p.setAttribute('id', hid + '_p' + (i + 1));
        }
        if (ninits && ninits.length > i) {
            p.textContent = ninits[i];
        }
        c.parts.push(p);
        c.div.appendChild(p);
    }

    return c;

}

/*
 * 
 */
function abutton(bid, text, handler, value, klass) {

    var b = {

        div: null,
        value: null,
        state: '',
        id: null,

        disable: function () {
            this.div.onclick = null;
        },

        onclick: function (f) {
            this.div.onclick = f;
        },

        change_state: function (st) {
            if (this.state) {
                this.remove_state(this.state);
            }
            this.state = st;
            this.div.classList.add(st);
        },

        remove_state: function (st) {
            this.div.classList.remove(st);
        },

        add_state: function (st) {
            this.state = st;
            this.div.classList.add(st);
        },

        text: function (t) {

            if (t) {
                this.div.textContent = t;
                return t;
            }
            return this.div.textContent;
        },

        get_focus: function () {
            this.div.focus();
        },

        has_focus: function () {
            return (document.activeElement === this.div);
        },

        blur_focus: function () {
            this.div.blur();
        },

        fancy_hide: function (t) {
            t = t ? t : Math.random() * 1000;
            var that = this;
            setTimeout(function () {
                that.div.style.display = 'none';
            }, t);

        },

        fancy_fade: function (t, p) {
            t = t ? t : Math.random() * 1000;
            p = p ? p : 0.5;
            var that = this;
            setTimeout(function () {
                that.div.style.opacity = p;
            }, t);
        },

        fade: function (p) {
            p = p ? p : 0.5;
            this.div.style.opacity = p;
        },

        fancy_show: function (t, f) {
            t = t ? t : Math.random() * 1000;
            var that = this;
            this.div.style.visibility = 'hidden';
            if (f) {
                this.div.style.display = 'inline-block';
            }
            setTimeout(function () {
                that.div.style.visibility = 'visible';
            }, t);

        },

        hide: function (f) {
            if (f) {
                this.div.style.display = 'none';
            }
            this.div.style.visibility = 'hidden';
        }
    };

    b.id = bid;
    b.value = value;

    b.div = document.createElement('button');
    if (klass) {
        b.div.setAttribute('class', klass);
    }
    b.div.setAttribute('id', 'ab' + (bid ? bid : 0));
    b.div.textContent = text;

    if (handler) {
        b.div.onclick = function (e) {
            handler(e, b);
        };
    }

    return b;

}

/*
 * 
 */
function progressliner() {

    var t = {

        div: null,
        pbar: null,
        pnum: null,
        l: null,
        a: 0,
        n: 0,
        c: 0,

        init: function () {

            this.div = document.createElement('div');
            this.div.setAttribute('class', 'timeline');

            this.pbar = document.createElement('div');
            this.pbar.setAttribute('class', 'tl_p');
            this.div.appendChild(this.pbar);

            this.pnum = document.createElement('div');
            this.pnum.setAttribute('class', 'tl_n');
            this.div.appendChild(this.pnum);
        },

        start: function (a, n, l) {

            this.a = a || 0;
            this.n = n || 100;

            this.pbar.style.marginLeft = '-100%';

            if (l !== undefined) {
                this.l = l;
                this.pnum.textContent = l;
            }
        },

        tix: function (c, l) {
            this.a += c || 1;
            this.a = (this.a > this.n) ? this.n : this.a;
            this.pbar.style.marginLeft = (-100.0 + (this.a / this.n) * 100.0) + '%';
            if (l !== undefined) {
                this.l = l;
                this.pnum.textContent = l;
            }
        },

        label: function (l) {
            if (l !== undefined) {
                this.l = l;
                this.pnum.textContent = l;
            }
        }

    };
    t.init();
    return t;

}

/*
 * 
 */
function timeliner() {

    var t = {

        div: null,
        pbar: null,
        tix: 0,
        tm: null,
        a: 0,
        b: 0,
        scale: 60,
        x: 0,

        init: function () {

            this.div = document.createElement('div');
            this.div.setAttribute('class', 'timeliner');

            this.pbar = document.createElement('div');
            this.pbar.setAttribute('class', 'tl_p');
            this.div.appendChild(this.pbar);

        },

        /*
         * a,b
         */
        start: function (a, b, s) {

            this.a = a || 0;
            this.b = b || 0;
            this.limit = (s || 10) * 1000;

            this.x = this.a;
            this.tix = 0;

            var that = this;
            this.tm = setInterval(function (ev) {
                that.tixer(ev);
            }, this.scale);

            this.pbar.style.width = 0;

        },

        tixer: function (ev) {

            this.tix += this.scale;

            if (this.tix >= this.limit) {
                clearInterval(this.tm);
            }

            // p in [0,1]
            var p = (1 - (this.limit - this.tix) / this.limit);
            this.x = (this.b - this.a) * p + this.a;
            this.pbar.style.width = ((p) * 100.0).toString() + '%';
        },

        stop: function (hide_bar) {

            clearInterval(this.tm);
            this.tm = null;

            if (hide_bar) {
                this.pbar.style.visibility = 'hidden';
            }
        }

    };
    t.init();
    return t;

}
