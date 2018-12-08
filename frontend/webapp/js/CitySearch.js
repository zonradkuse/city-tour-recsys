let m = require('mithril')

let settings = require('./settings.js')

let CitySearch = {
    input : {},
    searchResult : [],
    search: function () {
        m.request({
            method: "GET",
            url: settings.API_SERVER + "/search/" + CitySearch.input.query,
        })
        .then(function(result) {
            CitySearch.searchResult = result
        })
    },
    view : function() {
        return m("#_search", [
            m("form", {onsubmit : function (e) {
                e.preventDefault();
            }}, [
                m(".form-group", [
                    m("label" , {"for" : "searchInput"}, "Search for your city here!"),
                    m('input.form-control#searchInput[placeholder="Your City"][aria-described-by="inputHelp"]',
                        {
                            value : CitySearch.input.query,
                            oninput : function (e) {
                                CitySearch.input.query = e.target.value
                            }
                        }),
                    m("small.form-text.text-muted#searchHelp", "We check whether we already have data for your city. Otherwise we download data from OSM.")
                ]),
                m("button.btn[type=submit]", "Search!")
            ]),
            m("ul.list-group", [
                CitySearch.searchResult.map(function (item) {
                    return m("li.list-group-item", item)
                })
            ])
        ])
    }
}

module.exports = CitySearch
