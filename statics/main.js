function getNewVideo() {
    var r = new XMLHttpRequest();
    r.open("GET", "/get_gif", true);
    console.log("getting new video");
    r.onreadystatechange = function () {
      if (r.readyState != 4 || r.status != 200) return;
      document.getElementById("main_vid").src = r.responseText;
    };
    r.send();
}

getNewVideo()
