var crypto = require('crypto');
var async = require('async');


var mongoose = require('../lib/mongoose'),
    Schema = mongoose.Schema;

var schema = new Schema({
    "username": {
        "type": String,
        "unique": true,
        "required": true
    },
    "hashedPassword": {
        "type": String,
        "required": true
    },
    "salt": {
        "type": String,
        "require": true
    },
    "created": {
        "type": Date,
        "default": Date.now
    }
});

schema.methods.encryptPassword = function(password) {
    return crypto.createHmac('sha1', this.salt).update(password).digest('hex');
};

schema.virtual('password')
    .set(function(password) {
        this._plainPassword = password;
        this.salt = Math.random() + '';
        this.hashedPassword = this.encryptPassword(password);
    })
    .get(function() { return this._plainPassword; });

schema.methods.checkPassword = function(password) {
    return this.encryptPassword(password) === this.hashedPassword;
};

schema.statics.authorize = function(username, password, callback) {
    var User = this;

    async.waterfall([
        function(callback) {
            User.findOne({"username": username}, callback);
        },
        function(user, callback) {
            if (user) {
                if (user.checkPassword(password)) {
                    callback(null, user)
                } else {
                    callback(new AuthError('Пароль не верен'));
                };
            } else {
                /*var user = new User({"username": username, "password": password});
                user.save(function(err) {
                    if (err) return next(err);
                    callback(null, user);
                });*/
                callback(new AuthError('Пользователь не найден'));
            };
        }],
        callback);
};


exports.User = mongoose.model('User', schema);



var path = require('path');
var util = require('util');


// ошибки для отображения пользователю
function AuthError(message) {
    Error.apply(this, arguments);
    Error.captureStackTrace(this, AuthError);

    this.message = message || 'Error';
};

util.inherits(AuthError, Error);

AuthError.prototype.name = 'AuthError';

exports.AuthError = AuthError;