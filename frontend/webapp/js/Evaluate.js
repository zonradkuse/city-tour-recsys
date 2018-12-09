let m = require('mithril')

let User = require('./User.js')

let Evaluator = {
    like : function (item) {
        return function () {
            console.log(item)
        }
    },

    dislike : function (item) {
        return function () {
            console.log(item)
        }
    },

    view : function (vnode) {
        return m('div', [
            m('h1', 'Hi ' + User.current.username == undefined || "Guest" + '! You are evaluating ' + vnode.attrs.city + '.'),
            m("table.table.table-striped", vnode.attrs.items.map(function(item) {
                return m("tr", [
                    m("td", item.name),
                    m("td", m("button.btn.btn-default", {onclick : Evaluator.like(item)}, "I like")),
                    m("td", m("button.btn.btn-default", {onclick : Evaluator.dislike(item)}, "I dislike"))
                ])
            }))
        ])
    }
}

module.exports = Evaluator
