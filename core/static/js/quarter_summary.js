
// Filter expenses by quarter and month
function (expenses, selectedQuarter = null, selectedMonth = null) {
    return expenses.filter(expense => {
        const date = new Date(expense.created_date);
        const month = date.getMonth() + 1; // JS months are 0-indexed
        const quarter = getQuarter(month);

        const matchesQuarter = selectedQuarter ? quarter === selectedQuarter : true;
        const matchesMonth = selectedMonth ? month === selectedMonth : true;

        return matchesQuarter && matchesMonth;
    });
}
    // first subprogram date is q1 q2 etc - python does this already





    function updateProgressBar() {
        let spent = {{ total_spent }};
        let totalBudget = {{ allocated_budget }};
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

    function filterExpenses(quarter, month) {
        const rows = document.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const rowQuarter = row.dataset.quarter;
            const rowMonth = row.dataset.month;

            let show = true;

            if (quarter && rowQuarter !== quarter) show = false;
            if (month && rowMonth !== month) show = false;

            row.style.display = show ? '' : 'none';
        });
    }

    document.getElementById('quarterFilter').addEventListener('change', function () {
        const selectedQuarter = this.value;
        const selectedMonth = document.getElementById('monthFilter').value;
        filterExpenses(selectedQuarter, selectedMonth);
    });

    document.getElementById('monthFilter').addEventListener('change', function () {
        const selectedMonth = this.value;
        const selectedQuarter = document.getElementById('quarterFilter').value;
        filterExpenses(selectedQuarter, selectedMonth);
    });

    function clearFilters() {
        document.getElementById('quarterFilter').value = '';
        document.getElementById('monthFilter').value = '';
        filterExpenses('', '');
    }

    updateProgressBar();
