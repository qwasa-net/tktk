function k4bg(do_resize, do_addmeto, cid, cclass, colors) {

    let ccc = {

        div: null,
        colors: ["rgba(232,232,232, 1)", 'rgba(240,240,240, 0.9)'],
        super_colors: ["rgba(47,79,79,0.2)", "rgba(102,0,0,0.2)", "rgba(153,102,0,0.2)" ],
        grid_size: 22,
        drop_some: true,

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

            let p = parent || window;
            let that = this;
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

        mosaic_tile: function (wt, ht, w0, h0, colors, lineWidth, fctr, flip, flop) {

            let tile = document.createElement('canvas');
            tile.width = wt;
            tile.height = ht;
            let tile_ctx = tile.getContext("2d");
            tile_ctx.fillStyle = colors[0];
            tile_ctx.strokeStyle = colors[1];
            tile_ctx.lineJoin = "miter";
            tile_ctx.lineWidth = (typeof(lineWidh) == 'undefined')? lineWidth : wt / 25;
            tile_ctx.beginPath();

            let ax0 = (wt - w0) / 2;
            let ay0 = (ht - h0) / 2;
            let ax1 = ax0 + w0;
            let ay1 = ay0 + h0;
            fctr = (typeof(fctr) == 'undefined')? 6: fctr;

            let whrad = w0 / Math.sqrt(2 * Math.abs(fctr));

            if (flip){
                tile_ctx.translate(wt, 0);
                tile_ctx.scale(-1, 1);
            }

            if (flop){
                tile_ctx.translate(0, ht);
                tile_ctx.scale(1, -1);
            }

            tile_ctx.moveTo(ax0, ay0);
            tile_ctx.lineTo(ax0, ay0);
            tile_ctx.arcTo(ax1 - w0 / fctr, ay0 + h0 / fctr, ax1, ay0, whrad);
            tile_ctx.lineTo(ax1, ay0);

            tile_ctx.arcTo(ax1 - w0 / fctr, ay1 - h0 / fctr, ax1, ay1, whrad);
            tile_ctx.lineTo(ax1, ay1);

            tile_ctx.arcTo(ax1 - w0 / fctr, ay1 + h0 / fctr, ax0, ay1, whrad);
            tile_ctx.lineTo(ax0, ay1);

            tile_ctx.arcTo(ax0 - w0 / fctr, ay1 - h0 / fctr, ax0, ay0, whrad);
            tile_ctx.lineTo(ax0, ay0);

            tile_ctx.stroke();
            tile_ctx.fill();

            return tile;

        },

        arc_tile: function (wt, ht, w0, h0, colors, xshift, yshift, lineWidth) {

            let tile = document.createElement('canvas');
            tile.width = wt;
            tile.height = ht;
            let tile_ctx = tile.getContext("2d");
            tile_ctx.fillStyle = colors[0];
            tile_ctx.strokeStyle = colors[1];
            tile_ctx.lineJoin = "round";
            tile_ctx.lineWidth = (typeof(lineWidh) == 'undefined')? lineWidth : wt / 18;
            tile_ctx.beginPath();

            //
            tile_ctx.arc(wt / 2, ht / 2, w0 / 2.1, 0, 2 * Math.PI);

            tile_ctx.stroke();
            tile_ctx.fill();

            return tile;

        },

        rect_tile: function (wt, ht, w0, h0, colors, xshift, yshift, lineWidth) {

            let tile = document.createElement('canvas');
            tile.width = wt;
            tile.height = ht;

            let tile_ctx = tile.getContext("2d");
            tile_ctx.fillStyle = colors[0];
            tile_ctx.strokeStyle = colors[1];
            tile_ctx.lineJoin = "miter";
            tile_ctx.lineWidth = (typeof(lineWidh) == 'undefined')? lineWidth : wt / 25;
            tile_ctx.beginPath();

            let xtoff = xshift || 0;
            let ytoff = yshift || 0;

            let ax0 = (wt - w0) / 2;
            let ay0 = (ht - h0) / 2;
            let ax1 = ax0 + w0 - tile_ctx.lineWidth;
            let ay1 = ay0 + h0 - tile_ctx.lineWidth;

            tile_ctx.moveTo(ax0, ay0);
            tile_ctx.lineTo(ax1, ay0+ytoff);
            tile_ctx.lineTo(ax1+xtoff, ay1+ytoff);
            tile_ctx.lineTo(ax0+xtoff, ay1);
            tile_ctx.lineTo(ax0, ay0);

            tile_ctx.stroke();
            tile_ctx.fill();

            return tile;

        },

        draw: function (idx, w, h) {

            let p = this.div.parentElement;

            // update sizes
            w = w || p.width || p.clientWidth;
            h = h || p.height || p.clientHeight;

            this.div.setAttribute('width', w);
            this.div.setAttribute('height', h);

            // stage 1
            this.ctx.fillStyle = this.colors[0];
            this.ctx.strokeStyle = this.colors[1];

            let N = this.grid_size + 1;
            let w0 = Math.max(Math.ceil(w / N), Math.ceil(h / N));
            let h0 = w0; // square tiles

            let m0 = w0 * 0.025;

            // tile
            let wt = 2 * w0;
            let ht = 2 * h0;

            let tiles = [];
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 6));
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 6, false, true));
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 6, true, false));
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 4));
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 8));
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 8, false, true));
            tiles.push(this.mosaic_tile(wt, ht, w0*0.96, h0*0.96, this.colors, 0, 8, true, false));
            tiles.push(this.arc_tile(wt, ht, w0*0.7, h0*0.7, this.colors));
            tiles.push(this.arc_tile(wt, ht, w0*0.8, h0*0.8, this.colors));
            tiles.push(this.arc_tile(wt, ht, w0*0.9, h0*0.9, this.colors));
            tiles.push(this.rect_tile(wt, ht, w0*0.8, h0*0.8, this.colors, 0, 0, 0));
            tiles.push(this.rect_tile(wt, ht, w0*0.8, h0*0.8, this.colors, 0, wt/10, 0));
            tiles.push(this.rect_tile(wt, ht, w0*0.8, h0*0.8, this.colors, 0, -wt/10, 0));
            tiles.push(this.rect_tile(wt, ht, w0*0.8, h0*0.8, this.colors, ht/10, 0, 0));

            let tidx = Math.floor(tiles.length*Math.random());

            for (let i = 0; i < N + 1; i++) {
                for (let j = 0; j < N + 1; j++) {

                    if (this.drop_some && Math.random()>0.925){
                        continue;
                    }

                    let x = (w0+1) * i - w0 / 2;
                    let y = (h0+1) * j - ht / 2
                    this.ctx.globalAlpha = 0.1 + 0.9 * Math.random();

                    this.ctx.drawImage(tiles[tidx], x - wt / 4, y - ht / 4);
                }
            }

            // stage 2
            this.ctx.lineWidth = 0;
            this.ctx.globalAlpha = 1.0;

            let i = 0;
            h0 = 0; //(h/50) | 1;
            w0 = Math.ceil(w / 150.0);
            while (i <= w) {

                let a = w0 * Math.random() * 2 | 1;
                let b = h / 33 * Math.pow(Math.random() * 2, 2) | 1;

                let ci = Math.floor(this.super_colors.length * Math.random());
                this.ctx.fillStyle = this.super_colors[ci];
                this.ctx.beginPath();
                this.ctx.arc(i, h-b-h0, a, 0, 2 * Math.PI);
                this.ctx.fill();
                i += a*2;

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
