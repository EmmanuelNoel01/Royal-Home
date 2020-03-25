var tabButtons = document.querySelectorAll(".review-wrapper .dots .dot");
var tabPanels = document.querySelectorAll(".review-wrapper  .review-card-wrapper");
function showPanel(panelIndex) {
    tabPanels.forEach(function (node) {
        node.style.display = "none";
    });
    tabPanels[panelIndex].style.display = "flex";
};
showPanel(0);
