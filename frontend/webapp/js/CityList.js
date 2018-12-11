let City = require('./City.js')
let CityList = {
    oninit : City.getAllAvailable,
    view : function(vnode) {
        return m('ul.list-group', vnode.attrs.cities.map(function (item) {
                return m('li.list-group-item', m("a", { href : '/tour/' + item, oncreate: m.route.link }, item))
            })
        )
    }
}

module.exports = CityList
