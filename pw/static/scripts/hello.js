"use strict";
var engine = null;

var hello = {

    HELLO_URL: "/hello/",

    name: {
        'name': null,
        'uid': null,
        'pin': null,
        'provider': null,
    },

    init: function () {
        hello.name_holder = document.getElementById('hello');
        hello.name_div = document.getElementById('hello_name');
        hello.hello();

        if (engine) {
            engine.init();
        }
    },

    hello: function () {
        var qs = Math.random().toString();
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = hello.xhr_handler;
        xhr.open('GET', hello.HELLO_URL + "?" + qs);
        xhr.send(null);
    },

    xhr_handler: function () {

        // request not ready
        if (this.readyState != 4) return;

        // bad response
        if (this.status != 200) {
            console.log("@hello.xhr_handler: oops! " + this.status + "/" + this.statusText);
            setTimeout(hello.init, 2500);
            return;
        }

        try {
            var data = JSON.parse(this.response);
            hello.name = data;
        } catch (e) {
            console.log("@hello.xhr_handler: oops! " + e.toString());
            setTimeout(hello.init, 2500);
            return;
        }

        hello.start();

    },

    start: function () {
        if (hello.name_div) {
            hello.name_div.textContent = hello.my_name_is();
            hello.name_holder.style.visibility = 'visible';
            hello.name_holder.style.opacity = 1.0;
        }

        if (engine) {
            engine.start();
        }
    },

    my_name_is: function () {
        return (hello.name && hello.name.name) ? hello.name.name : "";
    },

    my_uid_is: function () {
        return (hello.name && hello.name.uid) ? hello.name.uid : 0;
    },

    i_am_social: function () {
        return hello.name.provider;
    }

};

// 
document.addEventListener("DOMContentLoaded", hello.init);
