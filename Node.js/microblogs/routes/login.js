var async = require('async');


var User = require('../models/user').User;
var AuthError = require('../models/user').AuthError;
var HttpError = require('../error').HttpError;



exports.get = function(req, res) {
    res.render('login');
};


exports.post = function(req, res, next) {
    var username = req.body.username;
    var password = req.body.password;

    /*async.waterfall([
        function(callback) {
            User.findOne({"username": username}, callback);
        },
        function(user, callback) {
            if (user) {
                if (user.checkPassword(password)) {
                    callback(null, user)
                } else {
                    next(new HttpError(403, 'Пароль не верен'));
                };
            } else {
                /*var user = new User({"username": username, "password": password});
                user.save(function(err) {
                    if (err) return next(err);
                    callback(null, user);
                });*//*
                next(new HttpError(403, 'Пользователь не найден'));
            };
    }],
    function(err, user) {
        if (err) return next(err);
        req.session.user = user._id;
        res.send({});
    });*/

    User.authorize(username, password, function(err, user) {
        if (err) {
            if (err instanceof AuthError) {
                return next(new HttpError(403, err.message));
            } else {
                return next(err);
            };
        };

        req.session.user = user._id;
        res.send({});
    });
};
