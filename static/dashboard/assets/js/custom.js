/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";

function toast(title,message="",type="info",position="topRight"){
    let types=["info","question","success","error","warning"]
    if(types.includes(type)){
        iziToast[type]({
            title: title,
            message: message,
            position: position
        });
    }
}

function setTimeToStart(ts){
    let end=moment(ts);
    if (window.startTimer) {
        clearInterval(window.startTimer);
    }
    let diff = moment.utc(end.diff(moment())).format("HH:mm:ss");
    $('#timeToStart').html("Exam starts in "+diff);
    window.startTimer=setInterval(function(){
        diff = moment.utc(end.diff(moment())).format("HH:mm:ss");
        $('#timeToStart').html("Exam starts in "+diff);
        if (""+diff == "00:00:00") {
            clearInterval(window.startTimer);
            $('#timeToStart').html("Please Wait...");
            setTimeout(function () {
                location.reload()
            }, 1000);
        }
    }, 1000); 
}

function setTimeToEnd(ts) {
    let end = moment(ts);
    if (window.startTimer) {
        clearInterval(window.startTimer);
    }
    let diff = moment.utc(end.diff(moment())).format("HH:mm:ss");
    $('#timeToEnd').html(diff);
    window.startTimer = setInterval(function () {
        diff = moment.utc(end.diff(moment())).format("HH:mm:ss");
        $('#timeToEnd').html(diff);
        if ("" + diff == "00:00:00") {
            clearInterval(window.startTimer);
            $('#finishExam').click();
        }
    }, 1000);
}

function fullscreen() {
    if (
        !document.fullscreenElement && // alternative standard method
        !document.mozFullScreenElement &&
        !document.webkitFullscreenElement &&
        !document.msFullscreenElement
    ) {
        // current working methods
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.msRequestFullscreen) {
            document.documentElement.msRequestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(
                Element.ALLOW_KEYBOARD_INPUT
            );
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        }
    }
}
