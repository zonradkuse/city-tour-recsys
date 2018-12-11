let m = require('mithril')

let User = require('./User.js')
let settings = require('./settings.js')

let Evaluator = {
    evaluated : [],
    like : function (item, positive) {
        return function () {
            return m.request({
                method: "PUT",
                url: settings.API_SERVER + "/evaluate/" + item.id,
                data : {
                    username : User.current.username,
                    evaluation : positive
                }
            })
            .then(function(result) {
                Evaluator.evaluated.append(item)
                City.searchResult = result
                console.log(result)
            })
        }
    },

    view : function (vnode) {
        return m('div', [
            m('h1', 'Hi ' + User.current.username == undefined || "Guest" + '! You are evaluating ' + vnode.attrs.city + '.'),
            m("table.table.table-striped", vnode.attrs.items.map(function(item) {
                let evaluated = Evaluator.evaluated.includes(item)
                console.log(evaluated)

                return m("tr", [
                    m("td", item.name),
                    !evaluated ? m("td", m("button.btn.btn-default", {onclick : Evaluator.like(item, true)}, "I like")) : '',
                    !evaluated ? m("td", m("button.btn.btn-default", {onclick : Evaluator.like(item, false)}, "I dislike")) : ''
                ])
            }))
        ])
    }
}

module.exports = Evaluator
