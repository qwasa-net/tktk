var engine = {
    init: function() {},
    start: function() {
        vtopics.start();
    },
};

var vtopics = new Vue({
    el: '#vtopics',
    data: {
        topics: null,
    },
    mounted: function() {},
    methods: {
        start: function() {
            axios.get('/topics.json')
                .then((response) => {
                    this.topics = response.data;
                    this.$el.classList.remove('invisible');
                }, (error) => {
                    console.error(error);
                });

        }
    }
});

// var vheros = new Vue({
//     el: '#vheros',
//     data: {
//         heros: []
//     },
//     mounted: function() {
//         axios.get("/api/heros/").then(response => {
//             this.heros = response.data;
//         }, error => {
//             console.error(error);
//         });
//     }
// });
