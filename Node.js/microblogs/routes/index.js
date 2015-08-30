/*
module.exports = function(app) {

    app.get('/', require('./frontpage').get);

    app.get('/login', require('./login').get);
    app.post('/login', require('./login').post);

    app.get('/msg', require('./msg').get);
};
*/
var express = require('express');
var router = express.Router();


var checkAuth = require('../middleware/checkAuth');



router.use(function timeLog(req, res, next) {
  console.log('Time: ', Date.now());
  next();
});


// define the home page route
router.get('/', require('./frontpage').get//function(req, res) {
  //res.render('index', {"hello": "'body from index.js'"});
//}
);

router.get('/login', require('./login').get);
router.post('/login', require('./login').post);

router.post('/logout', require('./logout').post);

router.get('/msg', checkAuth, require('./msg').get);

/*
// define the about route
router.get('/about', function(req, res) {
  res.send('About birds');
});


router.get('/users', function(req, res, next) {
    User.find({}, function(err, users) {
        if (err) return next(err);

        res.json(users);
    });
});

router.get('/user/:id', function(req, res, next) {
    try {
        var userId = new ObjectID(req.params.id);
    } catch(e) {
        next(404);
        return;
    };

    User.findById(userId, function(err, user) {
        if (err) return next(err);

        if (user) {
            res.json(user);
        } else {
            next(new HttpError(404, 'User not found'));
        };

    });
});
*/

module.exports = router;