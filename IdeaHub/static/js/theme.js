document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    // تحقق إذا كان المستخدم قد اختار الوضع الداكن مسبقًا
    if (localStorage.getItem("theme") === "dark") {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        themeToggle.textContent = "dark_mode";
    }

    themeToggle.addEventListener("click", function () {
        if (body.classList.contains("light-mode")) {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            themeToggle.textContent = "dark_mode";
            localStorage.setItem("theme", "dark");
        } else {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            themeToggle.textContent = "light_mode";
            localStorage.setItem("theme", "light");
        }
    });
});