/**
 * Deze functie toont de algoritme parameters wanneer
 * een checkbox is aangevinkt.
 */


let checkbox = document.getElementById("optionparameters")

checkbox.addEventListener("click", function () {

    let content = document.getElementById("optioncontent")

    if (checkbox.checked){
        content.style.display = "block";
    }
    else{
        content.style.display = "none";
    }
})
