let m = require('mithril')

let User = require('./User.js')
let settings = require('./settings.js')
let StateVerifier = require('./StateVerifier.js')
let Tour = require('./Tour.js')

let Evaluator = {
    oninit : StateVerifier.verify,
    evaluated : [],
    like : function (item, positive) {
        return function () {
            return m.request({
                method: "PUT",
                url: settings.API_SERVER + "/review/" + item[0],
                data : {
                    username : User.current.username,
                    review : positive
                }
            })
            .then(function(result) {
                Evaluator.evaluated.push(item)
                City.searchResult = result
            })
        }
    },

    view : function (vnode) {
        console.log(Tour.nodes)
        return m('div', [
            m('h1', 'Hi! You are evaluating ' + vnode.attrs.city + '.'),
            m("table.table.table-striped", Tour.nodes.map(function(item) {
                let evaluated = Evaluator.evaluated.includes(item)

                return m("tr", [
                    m("td", item[0]),
                    m("td", item[1]),
                    !evaluated ? m("td", m("button.btn.btn-default", {onclick : Evaluator.like(item, true)}, "I like")) : '',
                    !evaluated ? m("td", m("button.btn.btn-default", {onclick : Evaluator.like(item, false)}, "I dislike")) : ''
                ])
            }))
        ])
    }
}

module.exports = Evaluator
