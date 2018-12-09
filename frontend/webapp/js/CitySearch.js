let m = require('mithril')

let CityList = require('./CityList.js')
let City = require('./City.js')

let settings = require('./settings.js')
let StateVerifierMiddleware = require('./StateVerifier.js')

let CitySearch = {
    input : {},

    view : function() {
        StateVerifierMiddleware.verify()

        return m("#_search", [
            m("form", {onsubmit : function (e) {
                City.search(CitySearch.input.query)
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
                    m("small.form-text.text-muted#searchHelp", "We check whether we already have data for your city. Otherwise we download data from OSM. This will take a while! After that we will generate recommendations for the city you selected. You will be able to select between different routes. Please bear in mind that your Recommendations get better the more items you rated. For a start we recommend searching for a city you know already. Rate your favorite spots!")
                ]),
                m("button.btn[type=submit]", "Search!")
            ]),
            m(CityList, {
                cities : City.searchResult.map(function (item) {
                    return item.display_name
                })
            })
        ])
    }
}

module.exports = CitySearch
