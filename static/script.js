const api_url = 
      "http://localhost:8000/video/";
  
// Defining async function
async function getapi(url) {
    
    // Storing response
    const response = await fetch(url);
    
    // Storing data in form of JSON
    var data = await response.json();
    console.log(data);
    if (response) {
        hideloader();
    }
    show(data);
}

// Function to hide the loader
function hideloader() {
    document.getElementById('loading').style.display = 'none';
}
// Function to define innerHTML for HTML table
function show(data) {
    container = document.getElementById("container")
    for (let each of data) {
        player = document.createElement('video')
        player.setAttribute('id', each.oid.substring(0,8))
        player.setAttribute('class', 'video-js vjs-default-skin')
        player.setAttribute('controls', 'controls')
        player.setAttribute("height", "300")
        player.setAttribute("poster", `http://localhost:8000/storage/${each.oid}/thumbnail.png`)
        source = document.createElement('source')
        source.setAttribute("src", `http://localhost:8000/storage/${each.oid}/og.mpd`)
        source.setAttribute("type", "application/dash+xml")
        player.appendChild(source)

        container.appendChild(player)
        videojs(player)
    }
}

// Calling that async function
getapi(api_url);
  