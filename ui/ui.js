"use strict";

// RPC wrapper
function invoke_rpc(method, args, timeout, on_done){
  $("#crash").hide();
  $("#timeout").hide();
  $("#rpc_spinner").show();
  //send RPC with whatever data is appropriate. Display an error message on crash or timeout
  var xhr = new XMLHttpRequest();
  xhr.open("POST", method, true);
  xhr.setRequestHeader('Content-Type','application/json; charset=UTF-8');
  xhr.timeout = timeout;
  xhr.send(JSON.stringify(args));
  xhr.ontimeout = function () {
    $("#timeout").show();
    $("#rpc_spinner").hide();
    $("#crash").hide();
  };
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      $("#rpc_spinner").hide();
      var result = JSON.parse(xhr.responseText)
      $("#timeout").hide();
      if (typeof(on_done) != "undefined"){
        on_done(result);
      }
    } else {
      $("#crash").show();
    }
  }
}

// Resource load wrapper
function load_resource(name, on_done) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", name, true);
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      on_done(result);
    }
  }
  xhr.send();
}

// Code that runs first
$(document).ready(function(){
    // race condition if init() does RPC on function not yet registered by restart()!
    //restart();
    //init();
    invoke_rpc( "/restart", {}, 0, function() { init(); } )
});

function restart(){
  invoke_rpc( "/restart", {} )
}

//  LAB CODE

// this is inlined into infra/ui/ui.js

var step = 50;
var run = false;
var ghosting = false;
var busy = false;
var emoji;
var pressed_keys = [];
var scale = 4;
var svg_width;
var svg_height;
var last_data;

var tile_size = 64;

// convert game data into svg
function display(data,debug) {
    var w = $('#wrapper');
    svg_width = w.width();
    svg_height = 3*svg_width/4;   // 4:3 aspect ratio

    // build list of svg for emoji
    var blist = [];
    data.forEach(function(blob) {
        // blob attributes: texture, rect
        var svg = emoji[blob.texture];
        if (svg === undefined) {
            console.log('no emoji for '+JSON.stringify(blob));
        } else {
            var x = blob.rect[0].toString();
            var y = (scale*svg_height - blob.rect[3] - blob.rect[1]).toString();
            var g = '<g transform="translate('+x+' '+y+')';
            var scalex = blob.rect[2]/tile_size;
            var scaley = blob.rect[3]/tile_size;
            if (scalex != 1 || scaley != 1) {
                g += 'scale('+scalex.toString()+' '+scaley.toString()+')';
            }
            g += '"';
            if (blob.ghost) {
                g += ' opacity="0.5"';
            }
            g += '>';
            g += svg;
            if (debug) {
                g += '<rect x="0" y="0" width="64" height="64" stroke="red" stroke-width="2" fill="none"/>';
                g += '<text x="-5" y="-5" text-anchor="end" stroke="red" fill="red">'+x.toString()+","+y.toString()+'</text>';
            }
            g += '</g>';
            blist.push(g);
        }
    });

    // update visualization
    var svg = '<svg width="' + 
            svg_width.toString() +
            '" height="' +
            svg_height.toString() +
            '" viewbox="0 0 ' +
            (scale*svg_width).toString() +
            ' ' +
            (scale*svg_height).toString() +
            '">' +
            blist.join('') +
            '</svg>';
    $('#wrapper').html(svg);
}

function init_svg() {
    var w = $('#wrapper');
    svg_width = w.width();
    svg_height = 3*svg_width/4;   // 4:3 aspect ratio
}

function timestep(actions) {
    busy = true;
    var old_run = run;
    run = false;  // no more calls until this one is done!

    init_svg();

    // translate pressed keys into action string
    if (actions === undefined) {
        actions = [];
        pressed_keys.forEach(function(keycode) {
            if (keycode >= 65 && keycode <= 90) actions.push(String.fromCharCode(keycode));
            else if (keycode == 8) actions.push('delete');        // del
            else if (keycode == 9) actions.push('tab');        // tab
            else if (keycode == 13) actions.push('enter');       // enter/return
            else if (keycode == 32) actions.push('space');        // space
            else if (keycode == 37) actions.push('left');   // left arrow
            else if (keycode == 38) actions.push('up');   // up arrow
            else if (keycode == 39) actions.push('right');   // right arrow
            else if (keycode == 40) actions.push('down');   // down arrow
        });
    }

    invoke_rpc('/timestep', [actions, ghosting, scale*svg_width, scale*svg_height], 500, function (data) {
        last_data = data;
        if (emoji) display(data);
        run = old_run;  // okay to enable further timesteps now
        busy = false;
    });
}

// like timestep, but don't advance game state
function render() {
    busy = true;
    var old_run = run;
    run = false;  // no more calls until this one is done!

    init_svg();

    invoke_rpc('/render', [ghosting,scale*svg_width,scale*svg_height], 500, function (data) {
        last_data = data;
        if (emoji) display(data);
        run = old_run;  // okay to enable further timesteps now
        busy = false;
    });
}

function init_gui() {
    // add key listeners to game board
    pressed_keys = [];
    $(document).on('keydown',function(event) {
        var key = event.which;
        if (pressed_keys.indexOf(key) == -1) pressed_keys.push(key);
        event.preventDefault();
    });
    $(document).on('keyup',function(event) {
        var key = event.which;
        var i = pressed_keys.indexOf(key);
        if (i != -1) pressed_keys.splice(i,1);
        event.preventDefault();
    });

    // load SVG for all the emoji
    load_resource('/resources/emoji.json',function (data) {
        emoji = {};
        var re = new RegExp('\<svg.*?\>(.*)\</svg\>');
        $.each(data,function(codepoint,svg) {
            svg = svg.replace(re,'$1');
            emoji[codepoint] = svg;
        });
        if (last_data) display(last_data);
    });

    // hide controls until we have a map
    $("#step_simulation").css('visibility','hidden');
    $("#run_simulation").css('visibility','hidden');
    $("#pause_simulation").css('visibility','hidden');

    // set up map selection
    invoke_rpc("/ls", {"path":"resources/maps/"}, 0, function(loaded) {
        loaded.sort();
        for (var i in loaded) {
            $("#map_list").append(
                "<li class=\"mdl-menu__item\" onclick=\"handle_map_select('" +
                    loaded[i] +
                    "')\">" +
                    loaded[i] +
                    "</li>");
        }
        // start by selecting first map
        handle_map_select(loaded[0]);
    });
}

function handle_map_select(value){
    run = false;
    ghosting = false;

    $("#step_simulation").css('visibility','hidden');
    $("#run_simulation").css('visibility','hidden');
    $("#pause_simulation").css('visibility','hidden');

    invoke_rpc('/init_game',value,500,function () {
        $('#current_map').text(value);
        $("#step_simulation").css('visibility','visible');
        $("#run_simulation").css('visibility','visible');
        render();
    });
}

function handle_reset_button() {
    handle_map_select($('#current_map').text());
}

function handle_simulate_button(){
  // start simulation
  if(!run){
    // show / hide GUI elements
    $("#pause_simulation").css('visibility','visible');
    $("#run_simulation").css('visibility','hidden');
    $("#step_simulation").css('visibility','hidden');

    // flag update sequence to run
    run = true;
  }
}

function handle_step_button(){
  timestep();
}

function handle_ghost_button(){
    ghosting = true;
    render();
}

function handle_pause_button(){
  if(run){
    // show / hide GUI elements
    $("#pause_simulation").css('visibility','hidden');
    $("#run_simulation").css('visibility','visible');
    $("#step_simulation").css('visibility','visible');

    // flag update sequence to stop
    run = false;
  }
}

function handle_bigger_button() {
    if (scale > 1) scale -= 1;
    if (!busy) render();
}

function handle_smaller_button() {
    if (scale < 8) scale += 1;
    if (!busy) render();
}

function handle_debug_button() {
    if (last_data) display(last_data,true);
}

function init(){
    var step_function = function(){
        if(run){
            timestep();
        }
        // Repeat
        setTimeout(step_function, step);
    };

    init_gui();
    step_function();
}


