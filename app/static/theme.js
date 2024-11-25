document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');

    // Try to load the saved theme from localStorage or default to 'light'
    let savedTheme = 'light';
    try {
        savedTheme = localStorage.getItem('theme') || 'light';
    } catch (e) {
        console.error('LocalStorage access denied:', e);
    }
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Update button text based on the current theme
    themeToggle.textContent = savedTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';

    // Add click event listener to toggle theme
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';

        document.documentElement.setAttribute('data-theme', newTheme);
        try {
            localStorage.setItem('theme', newTheme);
        } catch (e) {
            console.error('Failed to save theme in localStorage:', e);
        }

        themeToggle.textContent = newTheme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    });
});
