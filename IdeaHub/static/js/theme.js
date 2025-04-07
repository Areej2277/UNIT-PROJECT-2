document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;

    // Check the status stored in LocalStorage
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        body.classList.remove("light-mode");
        themeIcon.textContent = "light_mode"; // Sun icon
    } else {
        body.classList.add("light-mode");
        body.classList.remove("dark-mode");
        themeIcon.textContent = "dark_mode"; // Moon icon
    }

    themeToggle.addEventListener("click", function () {
        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            themeIcon.textContent = "dark_mode"; // Convert to moon icon
            localStorage.setItem("theme", "light");
        } else {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            themeIcon.textContent = "light_mode";// Convert to sun icon
            localStorage.setItem("theme", "dark");
        }
    });
});