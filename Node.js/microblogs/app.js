var express = require('express');
var http = require('http');
var path = require('path');


var config = require('./config');
var log = require('./lib/log')(module);


var app = express();

app.engine('ejs', require('ejs-locals'));
app.set('views', path.join(__dirname, 'templates'));
app.set('view engine', 'ejs');

// Middleware
var favicon = require('serve-favicon');
app.use(favicon(__dirname + '/public/favicon.ico'));

var morgan = require('morgan')
if (config.get('env') == 'development') {
    app.use(morgan('dev'));
} else {
    app.use(morgan('combined'));
};

var bodyParser = require('body-parser');
// parse application/x-www-form-urlencoded 
app.use(bodyParser.urlencoded({ extended: false })); 
// parse application/json 
app.use(bodyParser.json());

var cookieParser = require('cookie-parser');
app.use(cookieParser())

var session = require('express-session');
var MongoStore = require('connect-mongo')(session);
var mongoose = require('./lib/mongoose');
app.use(session({
    "secret": config.get('session:secret'),
    "resave": false,
    "saveUninitialized": true,
    "key": config.get('session:key'),
    "cookie": config.get('session:cookie'),
    "store": new MongoStore({"mongooseConnection": mongoose.connection})
}));

app.use(require('./middleware/sendHttpError'));

app.use(require('./middleware/loadUser'));

var index = require('./routes');
app.use('/', index);

app.use('', express.static(path.join(__dirname, 'public')));


var errorhandler = require('errorhandler');
var HttpError = require('./error').HttpError;
app.use(clientErrorHandler);
function clientErrorHandler(err, req, res, next) {
/*  if (res.headersSent) {
    return next(err);
  }
  res.status(500);
  res.render('error', { error: err });
*/
    if (typeof err == 'number') {
      err = new HttpError(err);
    };

    if (err instanceof HttpError) {
        res.sendHttpError(err);
    } else if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
        // old express.errorHandler()(err, req, res, next);
        //errorhandler(err, req, res, next);
        next(err, req, res);
    } else {
        console.error('*console: ' + err);
        log.error(err);
        err = new HttpError(500);
        res.sendHttpError(err);
    };
};

var notifier = require('node-notifier');
//if ((process.env.NODE_ENV === 'development') {
if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    // only use in development
    app.use(errorhandler({log: errorNotification}));
};
function errorNotification(err, str, req) {
    var title = 'Error in ' + req.method + ' ' + req.url;
 
    console.log('\n***\n' + err + '\n');
    notifier.notify({"title": title, "message": str});
};

/*
var User = require('./models/user').User;
app.get('/users', function(req, res, next) {
    User.find({}, function(err, users) {
        if (err) return next(err);

        res.json(users);
    });
});
app.get('/user/:id', function(req, res, next) {
    User.findById(req.params.id, function(err, user) {
        console.log('\n' + user + '\n');
        if (!user) {
            next(new HttpError(404, 'User not found'));
        };
        if (err) return next(err);

        res.json(user);
    });
});
*/

app.set('port', config.get('port'));


http.createServer(app).listen(config.get('port'), function() {
    console.info('*console* Express server listening on port ' + config.get('port'));
    log.info('Express server listening on port ' + config.get('port'));
});