let m = require('mithril')
let Map = require('./Map.js')

let settings = require('./settings.js')
let User = require('./User.js')

let Tour = {
    nodes : [],
    edges : [],

    retrieveTours : function (vnode) {
        return m.request({
            method: "GET",
            url: settings.API_SERVER + '/recommendation/' + User.current.username + '/' + vnode.attrs.city
        })
        .then(function(result) {
            Tour.nodes = []
            Tour.edges = result
            for (var i = 0; i < Tour.edges.length; i++) {
                if (!Tour.nodes.includes(Tour.edges[i][0])) Tour.nodes.push(Tour.edges[i][0])
                if (!Tour.nodes.includes(Tour.edges[i][1])) Tour.nodes.push(Tour.edges[i][1])
            }

            console.log(Tour.nodes)

        })
    },

}

module.exports = Tour
