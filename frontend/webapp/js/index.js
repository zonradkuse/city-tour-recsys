let m = require('mithril')
let Map = require('./Map.js')
let Layout = require('./Layout.js')
let CityList = require('./CityList.js')
let CitySearch = require('./CitySearch.js')
let Evaluator = require('./Evaluate.js')
let Welcome = require('./Welcome.js')
let City = require('./City.js')

m.route(document.body, "/" ,{
    "/" : {
        render : function () { return m(Layout, m(Welcome)) }
    },
    "/search" : {
        render : function () { return m(Layout, m(CitySearch)) }
    },
    "/list" : {
        render : function () { return m(Layout, m(CityList, {
            oninit : City.getAllAvailable,
            cities : City.allCities
        })) }
    },
    "/tour/:user/:city" : {
        render : function () { return m(Layout, m("h2", "The Tour")) }
    },
    "/evaluate/:city" : {
        render : function (vnode) { return m(Layout, m(Evaluator, {
            ...vnode.attrs,
            items : [
                {name : "Test", id : "test" },
                {name : "Test1", id : "test1" }
            ]})) }
    }
})
