
 function toggleDarkMode() {
        const html = document.documentElement;
        const isDarkMode = html.classList.toggle('dark');

        // Save the preference in localStorage
        if (isDarkMode) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    }

    // Apply the saved theme when the page loads
    window.onload = function() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark');
        }
    };


