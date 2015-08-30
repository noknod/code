var ObjectID = require('mongodb').ObjectID;


var User = require('../models/user').User;



module.exports = function(req, res, next) {
    req.user = res.locals.user = null;

    if (!req.session.user) return next();

    try {
        var userId = new ObjectID(req.session.user);
    } catch(e) {
        next();
        return;
    };

    User.findById(userId, function(err, user) {
        if (err) return next(err);

        req.user = res.locals.user = user;
        next();
    });
};