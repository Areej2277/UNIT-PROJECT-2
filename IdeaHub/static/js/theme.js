document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const body = document.body;

    // التحقق من الوضع المخزن في LocalStorage
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        body.classList.remove("light-mode");
        themeIcon.textContent = "light_mode"; // أيقونة الشمس
    } else {
        body.classList.add("light-mode");
        body.classList.remove("dark-mode");
        themeIcon.textContent = "dark_mode"; // أيقونة القمر
    }

    themeToggle.addEventListener("click", function () {
        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            themeIcon.textContent = "dark_mode"; // تحويل للأيقونة القمر
            localStorage.setItem("theme", "light");
        } else {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            themeIcon.textContent = "light_mode"; // تحويل للأيقونة الشمس
            localStorage.setItem("theme", "dark");
        }
    });
});