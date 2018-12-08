let m = require('mithril')
let Map = require('./Map.js')
let Layout = require('./Layout.js')
let CityList = require('./CityList.js')
let CitySearch = require('./CitySearch.js')

m.route(document.body, "/search" ,{
    "/search" : {
        render : function () { return m(Layout, m(CitySearch)) }
    },
    "/list" : {
        render : function () { return m(Layout, m(CityList)) }
    },
    "/tour/:user/:city" : {
        render : function () { return m(Layout, m("h2", "The Tour")) }
    }
})
