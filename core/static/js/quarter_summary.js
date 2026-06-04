function updateProgressBar() {
    let spent = {{ total_spent_all }};
    let totalBudget = {{ total_budget_all }};
    let remaining = totalBudget - spent;
    let percentage = (remaining / totalBudget) * 100;

    let progressBar = document.getElementById("budgetProgressBar");
    progressBar.style.width = percentage + "%";

    if (percentage <= 20) {
        progressBar.classList.remove("bg-green-500");
        progressBar.classList.add("bg-red-500");
    } else if (percentage <= 50) {
        progressBar.classList.remove("bg-green-500");
        progressBar.classList.add("bg-yellow-500");
    }
}

updateProgressBar();
