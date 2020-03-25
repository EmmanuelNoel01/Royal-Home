var tabButtons = document.querySelectorAll(".dots .dot");
var tabPanels = document.querySelectorAll(".slide");

function showPanel(panelIndex) {
    tabPanels.forEach(function(node) {
        node.style.display = "none";
    });
    tabPanels[panelIndex].style.display = "flex";
    tabPanels[panelIndex].style.transition = "0.6s ease-in-out";

};
showPanel(0);