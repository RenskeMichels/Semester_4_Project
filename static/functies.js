/**
 * Deze functie toont de algoritme parameters wanneer
 * een checkbox is aangevinkt.
 */


let checkbox = document.getElementById("optionparameters");

// Voeg alleen listener toe op de pagina's waar deze wordt gebruikt.
if(checkbox) {
    checkbox.addEventListener("click", function () {

        let content = document.getElementById("optioncontent");

        if (checkbox.checked) {
            content.style.display = "block";
        } else {
            content.style.display = "none";
        }
    });
}


// Globale index voor de images.
let i = 0;

/**
 * Elke keer als deze functie wordt aangeroepen wordt er een
 * nieuwe afbeelding 2 seconden getoond.
 */
function changeImage() {

    let hoofdimg = document.getElementById("hoofdimg");
    let images = ["/static/champignonteeld1.jpg", "/static/champignonteeld2.jpg",
                    "/static/champignonteeld3.jpg"];
    // Verander afbeelding
     hoofdimg.src = images[i];
     // Verander de index
     if(i < images.length - 1) {
            i++;
     }
     else{
         i = 0;
     }
    // Wacht 2 seconden.
     setTimeout(changeImage, 4000);
}

window.onload = changeImage;
