var current_frame, total_frames, path, length, handle, myobj;

myobj = document.getElementById('myobj').cloneNode(true);

var init = function() {
    current_frame = 0;
    total_frames = 60;
    path = new Array();
    length = new Array();
    for(var i=0; i<7;i++){
        path[i] = document.getElementById('i'+i);
        l = path[i].getTotalLength();
        length[i] = l;
        path[i].style.strokeDasharray = l + ' ' + l;
        path[i].style.strokeDashoffset = l;
    }
    handle = 0;
}


var draw = function() {
    var progress = current_frame/total_frames;
    if (progress > 1) {
        window.cancelAnimationFrame(handle);
    } else {
        current_frame++;
        for(var j=0; j<path.length;j++){
            path[j].style.strokeDashoffset = Math.floor(length[j] * (1 - progress));
        }
        handle = window.requestAnimationFrame(draw);
    }
};

init();
draw();

var rerun = function() {
    var old = document.getElementsByTagName('div')[0];
    old.parentNode.removeChild(old);
    document.getElementsByTagName('body')[0].appendChild(myobj);
    init();
    draw();
};

// chart-bar
setTimeout(function start (){

    $('.server').each(function(j){
        // console.log(j)
        var $server = $(this);
        $(this).append('<span class="server-count"></span>')
        setTimeout(function(){

            // console.log($server.attr('data-percent'))
            // $server.css('width', $server.attr('data-percent'));

            $server.css('width', '100%');
        }, j*100);

    });

    $('.server-count').each(function () {

        // console.log($(this).parent('.server').attr('data-percent'))
        // var percent_user = $(this).parent('.server').attr('data-percent')
        // console.log(parseInt(percent_user))

        $(this).prop('Counter',0).animate({
            Counter: $(this).parent('.server').attr('data-percent')
        }, {
            duration: 2000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now) +' ');
            }
        });
    });

    $('.bar').each(function(i){
        var $bar = $(this);
        $(this).append('<span class="count"></span>')

        var user_count = $("#user-count").attr('data-percent')
        var active_user = $("#active-user").attr('data-percent')

        var calculated_percentage = (parseInt(active_user) / parseInt(user_count)) * 100
        // console.log(calculated_percentage)

        var string_percentage = calculated_percentage.toString() + '%'
        // console.log(string_percentage)

        $('.bar').attr('data-percent',string_percentage)
        // console.log($bar.attr('data-percent'))

        setTimeout(function(){
            $bar.css('width', $bar.attr('data-percent'));
        }, i*100);
    });

    $('.count').each(function () {
        $(this).prop('Counter',0).animate({
            Counter: $(this).parent('.bar').attr('data-percent')
        }, {
            duration: 2000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now) +'%');
            }
        });
    });

}, 500);
//server - counter

