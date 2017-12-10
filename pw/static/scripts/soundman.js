/**
 * soundman — примитивный "менеджер" звуков: загружает и содержит в себе набор
 * звуков, проигрывает их.
 */
var soundman = {

    sounds: [],
    LIBRARY_SIZE: 0,

    button: null,
    enabled: false,

    loaded: function () {
    },

    init: function () {

    },

    load: function (lsize, baseurl) {

        // в браузерах с поддержкой <AUDIO…> просто создаётся объект
        // все остальные случаи игнорируются
        if (typeof window.Audio !== 'undefined') {

            this.enabled = true;

            var va;
            var atype = null;

            for (var i = 0; i < lsize; i++) {

                va = new Audio();
                va.setAttribute('preload', 'auto');

                if (atype === null) {
                    if (va.canPlayType('audio/ogg')) {
                        atype = "ogg"
                    } else if (va.canPlayType('audio/mpeg')) {
                        atype = 'mp3';
                    } else
                        break;
                }

                va.src = baseurl + i.toString() + '.' + atype;

                va.load();
                this.sounds.push(va);

            }

        }

    },

    play: function (i) {

        if (!this.enabled) return;

        try {
            if (this.sounds.length > i) {
                if (this.sounds[i].readyState > 1) {
                    this.sounds[i].play();
                }
            }
        } catch (e) {
            console.log(e);
        }

    },

    enable: function () {
        this.enabled = true;
    },

    disable: function () {
        this.enabled = false;
    },

    toggle: function () {
        this.enabled = !this.enabled;
    },

    add_button: function (obj, bs) {
        this.button = obj;
        this.button.onclick(soundman.handle_button);
        soundman.button.change_state('on');
    },

    handle_button: function (ev) {
        soundman.toggle();
        if (soundman.enabled) {
            soundman.button.change_state('on');
        } else {
            soundman.button.change_state('off');
        }

    }

};
