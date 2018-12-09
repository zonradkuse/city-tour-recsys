let m = require('mithril')
let Map = require('./Map.js')

let Tour = {
    view : function (vnode) {
        return m(Map, {coordinates : vnode.attrs.coordinates})
    }
}

module.exports = Tour
