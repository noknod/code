/*var MongoClient = require('mongodb').MongoClient
  , assert = require('assert')
  , format = require('util').format;

// Connection URL
var url = 'mongodb://localhost:27017/chat';
// Use connect method to connect to the Server
MongoClient.connect(url, function(err, db) {
  assert.equal(null, err);
  console.log("Connected correctly to server");

    var collection = db.collection('test_insert');
    collection.insert({"a": 2}, function(err, docs) {

        collection.count(function(err, count) {
            console.log(format('count = %s", count'));
        });

        collection.find().toArray(function(err, results) {
            console.dir(results);
            db.close();
        });
    });
});
*/

/*
var User = require('./models/user').User;

var user = new User({
  "username": "Tester",
  "password": "secret"
});

user.save(function(err, user, affected) {
  if (err) throw err;
  console.log(arguments);
});
*/

var config = require('./config');
var mongoose = require('./lib/mongoose');

var async = require('async');

/*
function createDatabase() {
    console.log('function createDataBase: ' + mongoose.connection.readyState);
   
    db.dropDatabase(function(err) {
        if (err) throw err;
        console.log('database dropped');

        users = []
        callback = function(err, results) {
            console.log(arguments);
            // 3. close connection
            mongoose.disconnect();
            console.log('users created');
        };

        config.get('users').forEach(function(configUser) {
            console.log(JSON.stringify(configUser));
            users.push(function(callback) {
                var user = new User({"username": configUser.username, 
                                     "password": configUser.password});
                user.save(function(err) {
                    callback(err, user);
                });
            }
            );
        });
        console.log('users pushed');

        async.parallel(users, callback);
    });
};
*/

function open(callback) {
    mongoose.connection.on('open', callback);
};

function dropDatabase(callback) {
    // 1. drop database
    var db = mongoose.connection.db;
    db.dropDatabase(callback);
};


function requireModels(callback) {
    require('./models/user');

    async.each(
        Object.keys(mongoose.models), 
        function(modelName, callback) {
            mongoose.models[modelName].ensureIndexes(callback);
        },
        callback
    );
};


function createUsers(callback) {
    // 2. create & save 3 users
    //users = []
    /*callbackUsers = function(err, results) {
        if (err) {
            console.log('error at CreateUsers:\n' + err);
            callback(err);
        };

        console.log('users created');
        callback(results);
    };*/
    //var User = require('./models/user').User;

    async.each(
        config.get('users'), 
        function(userData, callback) {
            var user = new mongoose.models.User(userData);
            user.save(callback);
        },
        callback
    );

    /*config.get('users').forEach(function(configUser) {
        console.log(JSON.stringify(configUser));
        users.push(function(callback) {
            var user = new User({"username": configUser.username, 
                                 "password": configUser.password});
            user.save(function(err) {
                callback(err, user);
            });
        });
    });*/
    console.log('users pushed');

    //async.parallel(users, callback);
};


async.series([
        open, 
        dropDatabase, 
        requireModels, 
        createUsers
    ],
    //function(err, results) {
    function(err) {
        console.log(arguments);
        console.log('users created');
        // 3. close connection
        mongoose.disconnect();
        process.exit(err ? 255 : 0);
    });