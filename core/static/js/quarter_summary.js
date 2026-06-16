// budget-chart.js

function updateProgressBar() {
    // Get data from the global variable set in HTML
    const chartData = window.BUDGET_DATA?.datapoints || [];
    const totalBudget = parseFloat(window.BUDGET_DATA?.allocated_budget || 0);

    // Extract values safely
    const spentObj = chartData.find(item => item.label === "Spent");
    const remainingObj = chartData.find(item => item.label === "Remaining");

    const spent = spentObj ? spentObj.y : 0;
    const remaining = remainingObj ? remainingObj.y : 0;

    if (totalBudget === 0) return;

    const percentage = (remaining / totalBudget) * 100;

    // Update the Progress Bar
    const progressBar = document.getElementById("budgetProgressBar");
    if (progressBar) {
        progressBar.style.width = Math.max(0, Math.min(100, percentage)) + "%";

        progressBar.classList.remove("bg-green-500", "bg-yellow-500", "bg-red-500");

        if (percentage <= 20) {
            progressBar.classList.add("bg-red-500");
        } else if (percentage <= 50) {
            progressBar.classList.add("bg-yellow-500");
        } else {
            progressBar.classList.add("bg-green-500");
        }
    }
}

// Run when page loads
document.addEventListener('DOMContentLoaded', updateProgressBar);