window.resizeTo(900, 600)
var mediaElementCreated = false;

eel.expose(show_popup)
function show_popup(title, description) {
    document.getElementById("popup-title").innerHTML = title;
    document.getElementById("popup-description").innerHTML = description;
    document.getElementsByClassName("popup")[0].style = "display: block";
};

function update_video_resolution_option() {
    if (document.getElementById("file-type").value == "Audio") {document.getElementById("vid-res").disabled = true;}
    else {document.getElementById("vid-res").disabled = false;};
    /*
    if (document.getElementById("file-type").value == "Audio") {
        document.getElementById("prev-toggle").disabled = true;
        document.getElementById("prev-toggle").checked = false;
    }
    else {document.getElementById("prev-toggle").disabled = false;};
    */
};

function start_processing() {
    document.getElementsByClassName("load-anim")[0].style = "display: block";
    link = document.getElementById("yt-link").value;
    eel.create_yt_obj(link)(function(args) {
        if (!args) {
            document.getElementsByClassName("load-anim")[0].style.display = "none";
            return;
        }
        title = args[0]
        author = args[1]
        resolutions = args[2]
        document.getElementById("vid-title").innerHTML = title;
        document.getElementById("auth-title").innerHTML = author;
        document.getElementById("vid-res").innerHTML = null;
        for (i in resolutions) {document.getElementById("vid-res").innerHTML += `<option>${resolutions[i]}</option>`}
        document.getElementsByClassName("config-menu")[0].style.display = "block";
        document.getElementsByClassName("load-anim")[0].style.display = "none";
        document.getElementsByClassName("config-menu")[0].style.animation = "fade_in 1s ease forwards";
        setTimeout(function() {
            document.getElementById("home-page").style = "display: none";
        }, 1000)
    });
}

function back_to_home() {
    document.getElementById("home-page").style = "display: block";
    document.getElementsByClassName("config-menu")[0].style.animation = "fade_out 1s ease forwards";
    setTimeout(function() {
        document.getElementsByClassName("config-menu")[0].style = "display: none";
    }, 1000)
}

function start_download() {
    file_type = document.getElementById("file-type").value;
    show_preview = document.getElementById("prev-toggle").checked; // ! Remove this line if you want to pack this file as an executable with the '--onefile' arg or as a single file.
    document.getElementsByClassName("download-popup")[0].style = "display: block";

    if (file_type == "Video") {
        video_res = document.getElementById("vid-res").value;
        document.getElementsByClassName("vid-dl")[0].style.display = "block";
        eel.start_download(file_type, video_res, show_preview) // ! Replace this line with the next line if you want to pack this file as an executable with the '--onefile' arg or as a single file.
        // // eel.start_download(file_type, video_res) // ? Replace the code above with this one when packing the code in an executable with '--onefile' arg.
    }
    else {
        eel.start_download(file_type, null, show_preview)
    }
}

eel.expose(update_dl_desc)
function update_dl_desc(title, res, type) {
    document.getElementById("vid-title-lab").innerHTML = title;
    document.getElementById("vid-res-lab").innerHTML = res;
    document.getElementById("vid-type-lab").innerHTML = type;
};

eel.expose(update_progress)
function update_progress(percentage_completed, file_type) {
    if (file_type == "audio") {
        document.getElementById("aud-pro").style.width = percentage_completed + "%";
        document.getElementById("aud-perc").innerHTML = percentage_completed + "%";
    }
    else {
        document.getElementById("vid-pro").style.width = percentage_completed + "%";
        document.getElementById("vid-perc").innerHTML = percentage_completed + "%";
    }
}

eel.expose(reset_dl_popup)
function reset_dl_popup(result) {
    if (result === undefined) {result = true;};
    if (result) {
        document.getElementById("load-desc").style.display = "block";
        document.getElementsByClassName("load-anim")[0].style = "display: block";
    };
    document.getElementsByClassName("download-popup")[0].style = "display: none";
    document.getElementsByClassName("vid-dl")[0].style.display = "none";
    document.getElementById("aud-pro").style.width = 0;
    document.getElementById("aud-perc").innerHTML = "0%";
    document.getElementById("vid-pro").style.width = 0;
    document.getElementById("vid-perc").innerHTML = "0%";
}

eel.expose(after_download)
function after_download(file_type, file_path, show_preview) {
    // ---------------------------------------------------------------------------------
    if (show_preview) {
        if (file_type == "Video") {
            document.getElementById("video-preview").innerHTML = `<source src='${file_path}'>`;
            document.getElementById("video-preview").pause();
            document.getElementById("video-preview").volume = 0.6;
            document.getElementById("video-preview").play();
            document.getElementById("vid-preview-popup").style.display = "block"
        }
        else {
            document.getElementById("audio-preview").src = file_path;
            document.getElementById("audio-preview").pause();
            document.getElementById("audio-preview").volume = 0.6;
            document.getElementById("audio-preview").play();
            document.getElementById("aud-preview-popup").style.display = "block";
              
            if (!mediaElementCreated) {
                audio = document.getElementById("audio-preview");
                context = new AudioContext();
                src = context.createMediaElementSource(audio);
                mediaElementCreated = true;
            }

            var analyser = context.createAnalyser();

            var canvas = document.getElementById("canvas");
            var ctx = canvas.getContext("2d");

            canvas.height = (document.getElementById("aud-prev-cont").clientHeight * (60/100));
            canvas.width = (document.getElementById("aud-prev-cont").clientWidth * (96/100));

            src.connect(analyser);
            analyser.connect(context.destination);

            analyser.fftSize = 64;

            var bufferLength = analyser.frequencyBinCount;
            console.log(bufferLength);

            var dataArray = new Uint8Array(bufferLength);

            var WIDTH = canvas.width;
            var HEIGHT = canvas.height;

            var barWidth = ((WIDTH - 2) / bufferLength);
            var barHeight;
            var x = 0;

            function renderFrame() {
                requestAnimationFrame(renderFrame);

                x = 1;

                analyser.getByteFrequencyData(dataArray);

                ctx.fillStyle = "#eeeeee";
                ctx.fillRect(0, 0, WIDTH, HEIGHT);

                for (var i = 0; i < bufferLength; i++) {
                    barHeight = (dataArray[i])*(window.outerHeight/600);
                    
                    var r = (barHeight/HEIGHT) * (255) //(col1[0] + (col2[0] - col1[0])*i/bufferLength) 
                    var g = ((HEIGHT - barHeight)/HEIGHT) * (255) //(col1[1] + (col2[1] - col1[1])*i/bufferLength) ;
                    var b = 216 //(col1[2] + (col2[2] - col1[2])*i/bufferLength);

                    ctx.fillStyle = "rgb(" + r + "," + g + "," + b + ")";
                    // ctx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
                    roundRect(ctx, x, HEIGHT - barHeight, barWidth, barHeight, {tl: 6, tr: 6, br: 6, bl: 6}, true, false)

                    x += barWidth + 2;
                }
            }

            window.onresize = function(event) {
                canvas.height = (document.getElementById("aud-prev-cont").clientHeight * (60/100));
                canvas.width = (document.getElementById("aud-prev-cont").clientWidth * (96/100));
                
                WIDTH = canvas.width;
                HEIGHT = canvas.height;

                barWidth = ((WIDTH - 2) / bufferLength);
            }

            audio.play();
            renderFrame();
        }
    }
    // -----------------------------------------------------------------------------------------
    document.getElementsByClassName("load-anim")[0].style = "display: none";
    document.getElementById("load-desc").style.display = "none";
    show_popup("Downloaded Successfully", "Your Audio/Video has been succesfully downloaded in the Downloads Folder. <br>You may close this popup. <br><br>Hope you liked this software.")
}

// ----------------------------------------------------------------------
function roundRect(ctx, x, y, width, height, radius, fill, stroke) {
    if (typeof stroke === 'undefined') {
        stroke = true;
    }
    if (typeof radius === 'undefined') {
        radius = 5;
    }
    if (typeof radius === 'number') {
        radius = {tl: radius, tr: radius, br: radius, bl: radius};
    } else {
        var defaultRadius = {tl: 0, tr: 0, br: 0, bl: 0};
        for (var side in defaultRadius) {
            radius[side] = radius[side] || defaultRadius[side];
        }
    }
    ctx.beginPath();
    if (height != 0) {
        ctx.moveTo(x + radius.tl, y);
        ctx.lineTo(x + width - radius.tr, y);
        ctx.quadraticCurveTo(x + width, y, x + width, y + radius.tr);
        ctx.lineTo(x + width, y + height - radius.br);
        ctx.quadraticCurveTo(x + width, y + height, x + width - radius.br, y + height);
        ctx.lineTo(x + radius.bl, y + height);
        ctx.quadraticCurveTo(x, y + height, x, y + height - radius.bl);
        ctx.lineTo(x, y + radius.tl);
        ctx.quadraticCurveTo(x, y, x + radius.tl, y);
    }
    ctx.closePath();
    if (fill) {
        ctx.fill();
    }
    if (stroke) {
        ctx.stroke();
    }
}
// ----------------------------------------------------------------------------------------------

function close_preview() {
    document.getElementById("video-preview").pause();
    document.getElementById("vid-preview-popup").style.display = 'none';
    document.getElementById("audio-preview").pause();
    document.getElementById("aud-preview-popup").style.display = 'none';
}