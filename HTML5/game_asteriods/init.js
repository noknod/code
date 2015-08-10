var canvas, ctx;

var x = 0; dx = 0;

var imageObj = new Image();
var loaded = false;


// globals for user interface
var WIDTH = 800;
var HEIGHT = 600;
var score = 0;
var lives = 3;
var time = 0;
var started = false;
var pause = false;

// constants for game logic
var ROCK_DIST_MULT = 5;
var ROCK_QUANTITY = 12;
var ROCK_VEL_MULT = 0.5;
var SCORE_LEVEL = 5;

// globals for game logic
var my_ship = null;
var rock_group = new Set();
var missile_group = new Set();
var explosion_group = new Set();
var level = 1;
var score_for_level = ROCK_QUANTITY;

// globals for velocity
var SHIP_ANGLE_VELOCITY = 0.05; //1.0 / 20
var SHIP_THRUST_MULTYPLY = 0.1; //0.2
var SHIP_ANGLE_KEY = {"right" : 1, "left" : -1};
var SHIP_THRUST_KEY = {"up" : 1};
//var SHIP_SHOOT_KEY = {"space" : 1};
var SHIP_SHOOT_KEY = "space";
var SHIP_FRICTION = 0.01; //.99 //0.025
var MISSILE_VELOCITY = 6; //3
var ROCK_VEL = 0.3;
var ROCK_ANGLE_VEL = 0.1;
var KEY_MAP = {"space" : 32, "right" : 39, "left" : 37, "up" : 38};



function pick(arg, def) {
   return (typeof arg === 'undefined' ? def : arg);
}



function ImageInfo(center, size, radius, lifespan, animated) {
        this.center = center
        this.size = size
        this.radius = pick(radius, 0);
        this.lifespan = pick(lifespan, Infinity);
        this.animated = pick(animated, false);
}

ImageInfo.prototype.get_center = function() {
        return this.center
}

ImageInfo.prototype.get_size = function() {
        return this.size
}

ImageInfo.prototype.get_radius = function() {
        return this.radius
}

ImageInfo.prototype.get_lifespan = function() {
        return this.lifespan
}

ImageInfo.prototype.get_animated = function() {
        return this.animated
}



// art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
// debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
//                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
var debris_info = new ImageInfo([0, 0], [640, 480]);
debris_image = new Image();

// nebula images - nebula_brown.png, nebula_blue.png
var nebula_info = new ImageInfo([0, 0], [800, 600])
var nebula_image = new Image();

// splash image
var splash_info = new ImageInfo([0, 0], [400, 300])
var splash_image = new Image();

// ship image
var ship_info = new ImageInfo([0, 0], [90, 90], 35)
var ship_image = new Image();

// missile image - shot1.png, shot2.png, shot3.png
var missile_info = new ImageInfo([0, 0], [10, 10], 3, 50)
var missile_image = new Image();

// asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
var asteroid_info = new ImageInfo([0, 0], [90, 90], 40)
var asteroid_image = new Image();

// animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
var explosion_info = new ImageInfo([0, 0], [128, 128], 17, 24, true)
var explosion_image = new Image();

var images_to_load = 7;
var images_loaded = 0;



function onload_do() {
          // Draw the image only when we have the guarantee 
          // that it has been loaded
            images_loaded += 1;
            if (images_loaded === images_to_load) {loaded = true;}
         };



Set.prototype.difference_update = function(a) {
    return this.filter(function(i) {return a.indexOf(i) < 0;});
};



// helper functions to handle transformations
function angle_to_vector(ang) {
    return [Math.cos(ang), Math.sin(ang)]
}


function dist(p, q) {
    return Math.sqrt(Math.pow((p[0] - q[0]), 2) + Math.pow((p[1] - q[1]), 2))
}


function process_sprite_group(canvas, sprite_group) {
    // draw sprite_group
    for (index = 0, len = sprite_group.length; index < len; ++index) {
        a_sprite = sprite_group[index];
        a_sprite.draw(canvas);
    }
    // global pause
    if (started && (!pause)) {
        // update sprite_group
        remove = new Set();
        for (index = 0, len = sprite_group.length; index < len; ++index) {
            a_sprite = sprite_group[index];
            if (a_sprite.update()) {
                remove.add(a_sprite);
            }
        }
        sprite_group.difference_update(remove);
    }
}


function group_collide(sprite_group, other_object) {
    //global explosion_group
    collided = new Set();
    for (index = 0, len = sprite_group.length; index < len; ++index) {
        a_sprite = sprite_group[index];
        if (a_sprite.collide(other_object)) {
            collided.add(a_sprite);
            explosion_group.add(new Sprite(a_sprite.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound));
        }
    }
    sprite_group.difference_update(collided)
    return (collided.length > 0)
}


function group_group_collide(first_group, second_group) {
    collided = new Set();
    for (index = 0, len = first_group.length; index < len; ++index) {
        other_object = first_group[index];
        if (group_collide(second_group, other_object)) {
            collided.add(other_object);
        }
        if (second_group.length === 0) {
            break;
        }
    }
    first_group.difference_update(collided);
    return collided.length;
}


function new_game() {
    //global score, lives, time, pause, my_ship, rock_group, missile_group, level, explosion_group
    rock_group = new Set();
    missile_group = new Set();
    explosion_group = new Set();
    score = 0;
    lives = 3;
    time = 0;
    level = 1;
    score_for_level = ROCK_QUANTITY;
    my_ship = null;
    my_ship = new Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info);
    //my_ship = new Ship([10, 10], [0, 0], 0, ship_image, ship_info);
    //soundtrack.rewind();
    //soundtrack.play();
    pause = false;
}




// Ship class
function Ship(pos, vel, angle, image, info) {
        this.pos = [pos[0], pos[1]];
        this.vel = [vel[0], vel[1]];
        this.thrust = false;
        this.angle = angle;
        this.angle_vel = 0;
        this.image = image;
        //this.image_center = list(info.get_center());
        this.image_center = info.get_center();
        this.save_image_x = info.get_center()[0];
        this.image_size = info.get_size();
        this.radius = info.get_radius();
}
        
Ship.prototype.draw = function(canvas) {
//        if this.thrust:
//            canvas.draw_image(this.image, [this.image_center[0] + this.image_size[0], this.image_center[1]] , this.image_size,
//                              this.pos, this.image_size, this.angle)
//        else:
            //canvas.drawImage(this.image, this.image_center, this.image_size,
              //                this.pos, this.image_size);//, this.angle);
    canvas.save();
    canvas.beginPath();
    canvas.translate(this.pos[0], this.pos[1]);
    canvas.rotate(this.angle);
            canvas.drawImage(this.image, this.image_center[0], this.image_center[1], this.image_size[0], this.image_size[1], 
                //this.pos[0], this.pos[1], 
                -45, -45, 
                this.image_size[0], this.image_size[1]);
        // canvas.draw_circle(this.pos, this.radius, 1, "White", "White")
    canvas.restore();
}

Ship.prototype.update = function() {
        // update angle
        this.angle += this.angle_vel;
        
        // update position
        this.pos[0] = (this.pos[0] + this.vel[0]) % WIDTH;
        if (this.pos[0] < 0) {this.pos[0] = WIDTH;}
        this.pos[1] = (this.pos[1] + this.vel[1]) % HEIGHT;
        if (this.pos[1] < 0) {this.pos[1] = HEIGHT;}

        // update velocity
        if (this.thrust) {
            forward = [Math.cos(this.angle), Math.sin(this.angle)];
            this.vel[0] += SHIP_THRUST_MULTYPLY * forward[0];
            this.vel[1] += SHIP_THRUST_MULTYPLY * forward[1];
        }
        // friction udpate
        this.vel[0] *= (1 - SHIP_FRICTION);
        this.vel[1] *= (1 - SHIP_FRICTION);
}

Ship.prototype.set_thrust = function(on) {
        this.thrust = on;
        if (on) {
            this.image_center[0] = 90;//this.save_image_x * 3;
            //ship_thrust_sound.rewind();
            //ship_thrust_sound.play();
        }
        else {
            this.image_center[0] = this.save_image_x;
            //ship_thrust_sound.pause();
        }
}
       
Ship.prototype.increment_angle_vel = function() {
        this.angle_vel += SHIP_ANGLE_VELOCITY;
}
        
Ship.prototype.decrement_angle_vel = function() {
        this.angle_vel -= SHIP_ANGLE_VELOCITY;
}

Ship.prototype.set_angle_velocity = function(direction) {
        this.angle_vel = SHIP_ANGLE_VELOCITY * direction;
        //console.log(this.angle_vel);
}

Ship.prototype.shoot = function() {
        //global a_missile
        forward = angle_to_vector(this.angle);
        missile_pos = [this.pos[0] + this.radius * forward[0], this.pos[1] + this.radius * forward[1]];
        missile_vel = [this.vel[0] + MISSILE_VELOCITY * forward[0], 
                       this.vel[1] + MISSILE_VELOCITY * forward[1]];
        missile_group.add(new Sprite(missile_pos, missile_vel, this.angle, 0, missile_image, missile_info, missile_sound));
}

Ship.prototype.get_pos = function() {
        return this.pos;
}

Ship.prototype.get_radius = function() {
        return this.radius;
}

Ship.prototype.pause = function() {
//        this.angle_vel = 0
        //ship_thrust_sound.pause();
}

Ship.prototype.unpause = function() {
        if (this.thrust) {
            //ship_thrust_sound.play();
        }
}

Ship.prototype.kill = function() {
        //ship_thrust_sound.pause();
}

Ship.prototype.event_key_down = function(key) {
    //console.log(key);
        for (var i in SHIP_ANGLE_KEY) {
            //console.log(i);
            //console.log(KEY_MAP[i]);
            if (key === KEY_MAP[i]) {
                //console.log(SHIP_ANGLE_KEY[i]);
                this.set_angle_velocity(SHIP_ANGLE_KEY[i]);
                return;
            }
        }
        for (var i in SHIP_THRUST_KEY) {
            if (key === KEY_MAP[i]) {
                this.set_thrust(true);
                return;
            }
        }
        if (key === KEY_MAP[SHIP_SHOOT_KEY]) {
            this.shoot();
        }
}

Ship.prototype.event_key_up = function(key) {
        for (var i in SHIP_ANGLE_KEY) {
            if (key === KEY_MAP[i]) {
                this.set_angle_velocity(0);
                return;
            }
        }
        for (var i in SHIP_THRUST_KEY) {
            if (key === KEY_MAP[i]) {
                this.set_thrust(false);
                return;
            }
        }
}
















function init() {
    canvas = document.querySelector("#vcanvas");

//WIDTH
//HEIGHT
    ctx = canvas.getContext('2d');

    
    // Callback function called by the imageObj.src = .... line
    //located after this function
    explosion_image.onload = onload_do();
    asteroid_image.onload = onload_do();
    missile_image.onload = onload_do();
    ship_image.onload = onload_do();
    splash_image.onload = onload_do();
    nebula_image.onload = onload_do();
    debris_image.onload = onload_do();

    // Calls the imageObj.onload function asynchronously
    debris_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png";
    nebula_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png";
    splash_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png";
    ship_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png";
    missile_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png";
    asteroid_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png";
    explosion_image.src = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png";



    canvas.addEventListener('keydown', handleKeydown, false);
    canvas.addEventListener('keyup', handleKeyup, false);
    
    canvas.addEventListener('mouseenter', setFocus, false);
    canvas.addEventListener('mouseout', unsetFocus, false);

    new_game();

    canvas.focus();

    requestAnimationFrame(animate);
    //setInterval(animate, 1000);
}



function animate() {
        if (loaded) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

    // animiate background
    ctx.save();
    ctx.beginPath();
    ctx.drawImage(nebula_image, nebula_info.get_center()[0], nebula_info.get_center()[1], nebula_info.get_size()[0], nebula_info.get_size()[1], 0, 0, WIDTH, HEIGHT);
    ctx.restore();

    time += 1;
    wtime = (time / 4) % WIDTH;
    center = debris_info.get_center();
    size = debris_info.get_size();
    ctx.save();
    ctx.beginPath();
    ctx.translate(wtime + WIDTH/ 2, 0);
    ctx.drawImage(debris_image, center[0], center[1], size[0], size[1], 0, 0, WIDTH, HEIGHT);
    ctx.restore();
    ctx.save();
    ctx.beginPath();
    ctx.translate(wtime - WIDTH/ 2, 0);
    ctx.drawImage(debris_image, center[0], center[1], size[0], size[1], 0, 0, WIDTH, HEIGHT);
    ctx.restore();

        
        my_ship.draw(ctx);
        my_ship.update();
        }
        requestAnimationFrame(animate);
    }

    function handleKeydown(event) {
        var keyunicode=event.charCode || event.keyCode;
        my_ship.event_key_down(keyunicode);
        return false;
    }

    function handleKeyup(event) {
        var keyunicode=event.charCode || event.keyCode;
        my_ship.event_key_up(keyunicode);
        return false;
    }


 function setFocus(event) {
    canvas.focus();
};

 function unsetFocus(event) {
   canvas.blur();
 };