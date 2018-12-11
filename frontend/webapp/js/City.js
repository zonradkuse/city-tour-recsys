let m = require('mithril')
let settings = require('./settings.js')

let City = {
    searchResult : [],

    search: function (query) {
        return m.request({
            method: "GET",
            url: settings.API_SERVER + "/search/" + query,
        })
        .then(function(result) {
            City.searchResult = result
        })
    },

    allCities : [],
    getAllAvailable : function () {
        return m.request({
            method : "GET",
            url : settings.API_SERVER + '/city'
        }).then(function (result) {
            City.allCities = result
        })
    }
}

module.exports = City
