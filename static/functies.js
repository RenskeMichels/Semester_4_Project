/**
 * Deze functie toont de algoritme parameters wanneer
 * een checkbox is aangevinkt.
 */

alert("Hello??");

let checkbox = document.getElementById("optionparameters");

checkbox.addEventListener("click", function () {

    let content = document.getElementById("optioncontent");

    if (checkbox.checked){
        content.style.display = "block";
    }
    else{
        content.style.display = "none";
    }
})

/**
 * Deze functie zorgt voor een image slider en roept zichzelf steeds aan
 * */

let hoofdimg = document.getElementById("hoofdimg");

hoofdimg.addEventListener("click", function () {

})