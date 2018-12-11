let User = require('./User.js')
let Constraint = require('./Constraints.js')

let Welcome = {
    view : function () {
        contBtn = m('button.btn.btn-default', {
            onclick: function () {
                m.route.set('/list')
            }
        } , 'Continue to Search')
        let renderButton = User.current.username != undefined && User.current.username != ''

        return m('div', [
            m('h1', 'Welcome! Who are you?'),
            m('input[type=text][placeholder="Your Username"].form-control', {
                value : User.current.username,
                oninput : function (e) {
                    User.current.username = e.target.value
                }
            }),
            m('p', "Choose a name which is unique. This is a prototype without any warranty to work. Be aware that we did not invest any effort into privacy protection. However, we only save your username and your evaluations to provide better recommendations. You can review the sourcecode on GitHub."),
            renderButton ? contBtn : '',
            m("h2", "Constraints"),
            m("p", 'Optionally, you can specify a maximal tour length in kilometers. We take this into account when finding your path through the city.'),
            m('input[type=number][placeholder="Your maximal Tourlength"].form-control', {
                value : Constraint.maxDistance,
                oninput : function (e) {
                    Constraint.maxDistance = e.target.value
                }
            }),
        ])
    }
}

module.exports = Welcome
