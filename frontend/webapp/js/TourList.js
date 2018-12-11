let m = require('mithril')
let Map = require('./Map.js')

let settings = require('./settings.js')
let User = require('./User.js')
let Tour = require('./Tour.js')

let TourList = {
    oninit : Tour.retrieveTours,

    view : function (vnode) {
        return m("div", [
            m("a", { href : '/evaluate/' + vnode.attrs.city, items: Tour.nodes, oncreate: m.route.link }),
            m(Map, { nodes : Tour.nodes })
        ])
    }
}

module.exports = TourList
