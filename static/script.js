document.addEventListener("DOMContentLoaded", () => {
    const exerciseList = document.getElementById("exercise-data");
    const body = document.getElementById("body");
    const themeToggler = document.getElementById("theme-toggler");

    // Fetch real-time exercise data
    function fetchExerciseData() {
        fetch("/data")
            .then(response => response.json())
            .then(data => {
                exerciseList.innerHTML = ""; // Clear existing data
                for (const [exercise, count] of Object.entries(data)) {
                    const listItem = document.createElement("li");
                    listItem.className = "list-group-item";
                    listItem.textContent = `${exercise.charAt(0).toUpperCase() + exercise.slice(1)}: ${count}`;
                    exerciseList.appendChild(listItem);
                }
            });
    }

    // Refresh exercise data every second
    setInterval(fetchExerciseData, 1000);

    // Theme toggler functionality
    themeToggler.addEventListener("click", () => {
        if (body.classList.contains("light-theme")) {
            body.classList.replace("light-theme", "dark-theme");
            themeToggler.textContent = "Switch to Light Theme";
        } else {
            body.classList.replace("dark-theme", "light-theme");
            themeToggler.textContent = "Switch to Dark Theme";
        }
    });
});
