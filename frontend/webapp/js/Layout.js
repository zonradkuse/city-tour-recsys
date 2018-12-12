let m = require('mithril')

let User = require('./User.js')

let Layout = {
    view: function(vnode) {
        return m(".main", [
            m("nav.navbar.navbar-expand-lg.navbar-light.bg-light", [
                m("a[href='/'].nav-link", {oncreate: m.route.link}, "Home"),
                m("a[href='/list'].nav-link", {oncreate: m.route.link}, "Available Cities"),
                // fetching new cities is slow and we hence, we did not implement the endpoint.
                // m("a[href='/search'].nav-link", {oncreate: m.route.link}, "Search"),
            ]),
            m(".container", vnode.children)
        ])
    }
}

module.exports = Layout
