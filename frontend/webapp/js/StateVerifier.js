let User = require('./User.js')

module.exports = {
    verify : function () {
        if (User.current.username == "" || User.current.username == undefined) {
            m.route.set('/')
        }
    }
}
