document.addEventListener("DOMContentLoaded", () => {
    const exerciseList = document.getElementById("exercise-data");

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
});
