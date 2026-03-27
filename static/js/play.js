const buttonHideDeck = document.getElementById("hideDeck");
const buttonShuffleDeck = document.getElementById("shuffleDeck");
const myDeck = document.getElementById("deck");
const playForm = document.getElementById("playForm")

// The main part of the code, once this button is pressed, the game starts
buttonHideDeck.addEventListener("click", event => {
    buttonHideDeck.style.display = "none";
    myDeck.style.display = "none";
    buttonShuffleDeck.style.display = "none";
    playForm.style.visibility = "visible";
    });

    




