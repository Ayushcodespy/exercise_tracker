document.addEventListener("DOMContentLoaded", () => {
    const exerciseList = document.getElementById("exercise-data");
    const resetButton = document.getElementById("reset-button");

    // Fetch real-time exercise data
    function fetchExerciseData() {
        fetch("/data")
            .then(response => response.json())
            .then(data => {
                exerciseList.innerHTML = Object.entries(data).map(([exercise, count]) => `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center">
                            ${exercise.charAt(0).toUpperCase() + exercise.slice(1)}
                        </div>
                        <span class="badge bg-primary rounded-pill">${count}</span>
                    </li>
                `).join('');
            });
    }

    // Reset exercise data
    resetButton.addEventListener("click", () => {
        fetch("/reset", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                fetchExerciseData(); // Refresh the exercise data
                alert("Exercise counts have been reset!");
            }
        })
        .catch(error => {
            console.error("Error resetting data:", error);
        });
    });

    // Refresh exercise data every second
    setInterval(fetchExerciseData, 1000);
});




document.addEventListener("DOMContentLoaded", () => {
    // GSAP Animations for Exercise Cards
    const exerciseCards = document.querySelectorAll(".exercise-card");

    exerciseCards.forEach((card) => {
        const smallDescription = card.querySelector(".small-description");
        const fullDescription = card.querySelector(".full-description");

        card.addEventListener("click", () => {
            if (fullDescription.style.display === "none") {
                // Expand the card
                gsap.to(fullDescription, {
                    height: "auto",
                    opacity: 1,
                    duration: 0.3,
                    ease: "power1.out",
                    onStart: () => {
                        fullDescription.style.display = "block";
                    },
                });
            } else {
                // Collapse the card
                gsap.to(fullDescription, {
                    height: 0,
                    opacity: 0,
                    duration: 0.3,
                    ease: "power1.in",
                    onComplete: () => {
                        fullDescription.style.display = "none";
                    },
                });
            }
        });
    });
});