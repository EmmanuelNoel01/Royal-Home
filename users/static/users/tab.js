var tabButtons = document.querySelectorAll(".tabContainer .form-header .buttonContainer a");
var tabPanels = document.querySelectorAll(".tabContainer  .tabPanel");
function showPanel(panelIndex) {
    tabPanels.forEach(function (node) {
        node.style.display = "none";
    });
    tabPanels[panelIndex].style.display = "block";
};
showPanel(0);
