const output = document.getElementById("output");
let words = [];

fetch("word_generation/output.txt")
    .then(response => response.text())
    .then(text => {
    words = text.split("\n");

    //get title from url
    let results = new RegExp("[\?&]id=([^&#]*)").exec(window.location.href);
    if (results) {
        displayTitle(num);
    } else {
        displayTitle(getRandomId());
    }
}).catch(error => {
    console.error(error);
});

function getRandomId() {
    return Math.floor(Math.random() * words.length);
}

function displayTitle(id) {
    output.innerText = getTitleById(id);
    updateUrl(id);
}

function getTitleById(id) {
    return words[id];
}

function updateUrl(id) {
    const url = window.location.href.split("?")[0] + "?id=" + id.toString();
    history.replaceState("", url, url);
}