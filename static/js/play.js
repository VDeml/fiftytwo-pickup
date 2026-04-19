const buttonHideDeck = document.getElementById("hideDeck");
const buttonShuffleDeck = document.getElementById("shuffleDeck");
const buttonPlay = document.getElementById("playButton");
const display = document.getElementById("display");
const myDeck = document.getElementById("deck");
const playForm = document.getElementById("playForm");
const resultForm = document.querySelector('#playForm form');

const isPlay = window.location.pathname === "/play";

// Hide deck
if (buttonHideDeck) {
    buttonHideDeck.addEventListener("click", () => {
        buttonHideDeck.style.display = "none";
        if (myDeck) myDeck.style.display = "none";
        if (buttonShuffleDeck) buttonShuffleDeck.style.display = "none";
        if (playForm) playForm.style.visibility = "visible";
    });
}

// Start timer when PLAY form submits
if (buttonPlay) {
    const playForm = buttonPlay.closest("form");
    if (playForm) {
        playForm.addEventListener("submit", () => {
            localStorage.setItem("startTime", Date.now());
        });
    }
}

// Reset timer and start again when Shuffle deck submits
if (buttonShuffleDeck) {
    const shuffleForm = buttonShuffleDeck.closest("form");
    if (shuffleForm) {
        shuffleForm.addEventListener("submit", () => {
            localStorage.setItem("startTime", Date.now());
        });
    }
}

// Stop timer on submit of the answer form
if (resultForm) {
    resultForm.addEventListener("submit", () => {
        localStorage.removeItem("startTime");
    });
}

// Timer variables
let timer = null;
let startTime = 0;

// Start timer on page load if needed
window.addEventListener("load", () => {
    if (!isPlay) {
        localStorage.removeItem("startTime");
        return;
    }

    const savedStart = localStorage.getItem("startTime");

    if (savedStart && myDeck) {
        startTime = parseInt(savedStart);
        timer = setInterval(update, 10);
    }
});

// Update display
function update() {
    const elapsedTime = Date.now() - startTime;

    let hours = Math.floor(elapsedTime / (1000 * 60 * 60));
    let minutes = Math.floor((elapsedTime / (1000 * 60)) % 60);
    let seconds = Math.floor((elapsedTime / 1000) % 60);
    let milliseconds = Math.floor((elapsedTime % 1000) / 10);

    display.textContent =
        `${String(hours).padStart(2, "0")}:` +
        `${String(minutes).padStart(2, "0")}:` +
        `${String(seconds).padStart(2, "0")}:` +
        `${String(milliseconds).padStart(2, "0")}`;
}

// Implementing accuracy functionality
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#playForm form');
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevents normal form submission. 
        // Not sure why this is needed, but seen multiple times
        const cards = [];
        // Run a loop through all submitted cards, add them all to the array
        for (let i = 0; i < 4; i++) {
            const card = document.querySelector(`input[name="card${i}"]`).value;
            cards.push(card);
        }
        // Sedn cards to app.py using "fetch"
        fetch('/play', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'submit',
                cards: cards
            })
        })
        .then(response => response.json())
        .then(data => {
            alert(`Accuracy is: ${data.accuracy}%`) 
        });  
    });
});