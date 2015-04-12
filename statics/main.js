function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}


function getNewVideo() {
    var r = new XMLHttpRequest();
    r.open("GET", "/get_gif/", true);
    console.log("getting new video");
    r.onreadystatechange = function () {
      if (r.readyState != 4 || r.status != 200) return;
      onNewVid(r);
    };
    r.send();
}

function onNewVid(r) {
    data = JSON.parse(r.responseText);
    var mainVideo = document.createElement("video");
    var source = document.createElement("source");
    var source_link = document.createElement("h3");
    mainVideo.autoplay = true;
    if (!document.getElementById("autoplay").checked) {
        mainVideo.loop = true;
    }
    source.src = data.link;
    source.type = "video/mp4";
    source_link.innerHTML = data.source;
    mainVideo.appendChild(source);
    mainVideo.onended = function(e) {
        if (document.getElementById("autoplay").checked) {
            window.location = location.origin + "?autoplay=true";
        }
    };

    document.getElementById("main-player").innerHTML = "";
    document.getElementById("main-player").appendChild(mainVideo);
    document.getElementById("main-player").appendChild(source_link);
}

if (getParameterByName("autoplay") == "true") {
    document.getElementById("autoplay").checked = true;
}

getNewVideo();
