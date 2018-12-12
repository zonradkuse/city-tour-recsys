let m = require('mithril')
let Map = require('./Map.js')

let settings = require('./settings.js')
let User = require('./User.js')
let Constraint = require('./Constraints.js')

let Tour = {
    nodes : [],
    edges : [],
    graph  : {},

    retrieveTours : function (vnode) {
        return m.request({
            method: "GET",
            url: settings.API_SERVER + '/recommendation/' + User.current.username + '/' + vnode.attrs.city,
            data : Constraint
        })
        .then(function(result) {
            Tour.nodes = []
            Tour.edges = result
            var ids = []
            for (var i = 0; i < Tour.edges.length; i++) {
                if (!ids.includes(Tour.edges[i][0][0])) {
                    Tour.nodes.push(Tour.edges[i][0])
                    ids.push(Tour.edges[i][0][0])
                }

                if (!ids.includes(Tour.edges[i][1][0])) {
                    Tour.nodes.push(Tour.edges[i][1])
                    ids.push(Tour.edges[i][1][0])
                }

                Tour.graph[Tour.edges[i][0]] = Tour.edges[i][1] // easy access
            }

        })
    },

}

module.exports = Tour
