let m = require('mithril')
let Map = require('./Map.js')

let settings = require('./settings.js')
let User = require('./User.js')
let Tour = require('./Tour.js')
let StateVerifier = require('./StateVerifier.js')
let Evaluator = require('./Evaluate.js')

let TourList = {
    oncreate: StateVerifier.verify,
    oninit : Tour.retrieveTours,

    view : function (vnode) {
        console.log(Tour.nodes)

        return m(".row", [
            m(".col", m(Evaluator, {...vnode.attrs, nodes : Tour.nodes})),
            //m("a", { href : '/evaluate/' + vnode.attrs.city, items: Tour.nodes, oncreate: m.route.link }, "Go to Evaluation"),
            m(".col", m(Map, { nodes : Tour.nodes }))
        ])
    }
}

module.exports = TourList
