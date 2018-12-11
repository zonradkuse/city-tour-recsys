let m = require('mithril')
let Map = require('./Map.js')

let settings = require('./settings.js')
let User = require('./User.js')

let Tour = {
    nodes : [],

    retrieveTours : function (vnode) {
        return m.request({
            method: "GET",
            url: settings.API_SERVER + '/recommendation/' + User.current.username + '/' + vnode.attrs.city
        })
        .then(function(result) {
            Tour.nodes = result
        })
    },

}

module.exports = Tour
