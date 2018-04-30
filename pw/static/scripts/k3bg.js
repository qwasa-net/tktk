function k3bg(do_resize, do_addmeto, cid, cclass, colors) {

    var ccc = {

        div: null,
        colors: ["rgba(237,237,237, 0.35)", 'rgba(255,255,255,0.5)', "rgba(47,79,79,0.25)"],

        init: function (cid, cclass) {

            this.div = document.createElement('canvas');

            if (cid) {
                this.div.setAttribute('id', cid);
            }
            if (cclass) {
                this.div.setAttribute('class', cclass);
            }

            this.ctx = this.div.getContext("2d");

        },

        redraw_tm: null,

        set_auto_resize: function (delay, parent) {

            var p = parent || window;
            var that = this;
            p.addEventListener("resize", function () {
                if (!that.redraw_tm) {
                    that.redraw_tm = setTimeout(that.redraw, delay, that);
                }
            });
        },

        redraw: function (that) {
            if (that !== undefined) {
                that.redraw_tm = null;
                that.draw();
            }
        },

        draw: function (idx, w, h) {

            var p = this.div.parentElement;

            // update sizes
            if (!w) {
                w = p.width || p.clientWidth;
            }

            if (!h) {
                h = p.height || p.clientHeight;
            }

            this.div.setAttribute('width', w);
            this.div.setAttribute('height', h);

            // stage 1
            this.ctx.fillStyle = this.colors[0];
            this.ctx.strokeStyle = this.colors[1];

            for (var j = 5; j > 0; j--) {

                this.ctx.lineWidth = (j + 1) * 2;

                for (var i = 0; i < 10 * (5 - j + 1); i++) {

                    var x = w * (Math.random());
                    var y = h * (Math.random());

                    this.ctx.beginPath();
                    this.ctx.arc(x, y, w / (26 - j * j) * (0.25 + 0.75 * Math.random()), 0, 2 * Math.PI);
                    this.ctx.fill();
                    this.ctx.stroke();
                }
            }

            // stage 2
            this.ctx.fillStyle = this.colors[2];

            var i = 0;
            var h0 = 0; //(h/50) | 1;
            var w0 = Math.ceil(w / 600.0);
            while (i <= w) {

                var a = w0 * Math.random() * 2 | 1;
                var b = h / 33 * Math.pow(Math.random() * 2, 2) | 1;
                this.ctx.lineWidth = 1;
                //this.ctx.beginPath();
                this.ctx.fillRect(i, h - b - h0, a, b + h0);

                i += a;


            }
        }


    };

    cid = cid || "k3bg";
    cclass = cclass || "k3bg";

    ccc.init(cid, cclass);

    if (colors) {
        ccc.colors = colors;
    }

    if (do_resize) {
        ccc.set_auto_resize(250);
    }

    if (do_addmeto) {
        let cdiv = document.createElement('div');
        cdiv.setAttribute('id', cid);
        cdiv.setAttribute('class', cclass);
        cdiv.appendChild(ccc.div);
        document.body.appendChild(cdiv);
        ccc.draw();
    }

    return ccc;

}
