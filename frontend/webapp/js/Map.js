let Tour = require('./Tour.js')

var Map = {
    map : null,
    oncreate: function (vnode) {
        Map.map = L.map("_map");
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
            '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
        }).addTo(Map.map);
    },

    view : function () {
        Tour.nodes.forEach(function(item) {
            Map.map.setView([Tour.nodes[0][3], Tour.nodes[0][2]], 11);
            coords = [item[3], item[2]]
            var marker = L.marker(coords).addTo(Map.map)
            marker.bindPopup(item[1]).openPopup();
        })
        return m(".map", {id : "_map"})
    }
};

module.exports = Map;
