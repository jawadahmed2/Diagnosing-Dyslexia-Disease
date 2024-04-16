document.addEventListener("DOMContentLoaded", function () {
    const alphabet = "CHIKLMNORTUVWXY"; // Removed letters not trained A, B, D, E, F, G, P , Q, S, Z
    let currentQuestionIndex = 0;

    // Randomly select 10 alphabets for questions
    const questions = getRandomQuestions(alphabet, 10);
    const questionContainer = document.getElementById("question");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    function getRandomQuestions(alphabet, count) {
        const shuffledAlphabet = alphabet.split("").sort(() => Math.random() - 0.5);
        return shuffledAlphabet.slice(0, count);
    }

    function displayQuestion(index) {
        const questionTextElement = document.getElementById("questionText");
        questionTextElement.textContent = `Write an alphabet :  ${questions[index]}`;
        questionTextElement.classList.add("question-text");
    }


    function clearCanvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function displayAnswerCanvas() {
        canvas.addEventListener("mousedown", startPosition);
        canvas.addEventListener("mouseup", finishedPosition);
        canvas.addEventListener("mousemove", draw);

        canvas.width = 500;
        canvas.height = 300;
        canvas.style.border = "1px solid #000";
    }

    function startPosition(e) {
        drawing = true;
        draw(e);
    }

    function finishedPosition() {
        drawing = false;
        context.beginPath();
    }

    function draw(e) {
        if (!drawing) return;

        const rect = canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        context.lineWidth = 10;
        context.lineCap = "round";
        context.strokeStyle = "#000";

        context.lineTo(mouseX, mouseY);
        context.stroke();
        context.beginPath();
        context.moveTo(mouseX, mouseY);
    }


    displayQuestion(currentQuestionIndex);
    displayAnswerCanvas();
    updateCounter();

    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitBtn");

    prevBtn.addEventListener("click", function () {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
            clearCanvas();
            clearResult(); // Clear the result elements
            updateCounter();
        }
    });

    nextBtn.addEventListener("click", function () {
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
            clearCanvas();
            clearResult(); // Clear the result elements
            updateCounter();
        }
    });

    // Function to clear the result elements
    function clearResult() {
        document.getElementById("resultLabel").textContent = "";
        document.getElementById("resultScore").textContent = "";
    }

    submitBtn.addEventListener("click", function () {
        const dataUrl = canvas.toDataURL();
        console.log(dataUrl);

        fetch("/upload-alphabets", {
            method: "POST",
            body: new URLSearchParams({
                img_data: dataUrl,
                letter_number: currentQuestionIndex
            }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
            .then(response => {
                if (response.ok) {
                    console.log("Image saved successfully");
                    // Fetch result after image is saved
                    return fetch("/alphabet-result");
                } else {
                    console.error("Failed to save image");
                    // Optionally, handle error cases
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update UI with received result
                const { label, score } = data;
                document.getElementById("resultLabel").textContent = `Label: ${label}`;
                document.getElementById("resultScore").textContent = `Score: ${score} / 10`;

                // Check if this is the 10th question
                if (currentQuestionIndex === 9) {
                    // Fetch and display overall result
                    fetchOverallResult();
                    // Fetch and render pie chart
                    fetchPieChartData();
                }
            })
            .catch(error => {
                console.error("Error occurred:", error);
                // Optionally, handle error cases
            });
    });
    function fetchPieChartData() {
        fetch("/alphabet-piechart-data")
            .then(response => response.json())
            .then(data => {
                // Extract labels and counts from the data
                const labels = data.map(item => item.label);
                const counts = data.map(item => item.count);

                // Render the pie chart
                renderPieChart(labels, counts);
            })
            .catch(error => {
                console.error("Error fetching pie chart data:", error);
                // Handle error
            });
    }

    function renderPieChart(labels, counts) {
        const ctx = document.getElementById("pieChart").getContext("2d");
        const pieChart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        // Add more colors if needed
                    ]
                }]
            },
            options: {
                // Set width and height of the pie chart
                responsive: true, // Disable responsiveness
                maintainAspectRatio: false, // Allow chart to be resized
                width: 600, // Set width to 200 pixels
                height: 600, // Set height to 200 pixels
                // Add other options as needed
            }
        });
    }

    function fetchOverallResult() {
        fetch("/overall-alphabet-result")
            .then(response => response.json())
            .then(data => {
                // Update UI with overall result
                const { Prediction, overall_score } = data;
                const predictedResultElement = document.getElementById("predicted_result");
                const predictedScoreElement = document.getElementById("predicted_score");

                // Set text content
                predictedResultElement.innerHTML = `Predicted Result: <span class="${Prediction === "Hurrah! There is no Dyslexia Found" ? 'green-text' : 'red-text'}">${Prediction}</span>`;
                predictedScoreElement.innerHTML = `Predicted Score: <span class="${Prediction === "Hurrah! There is no Dyslexia Found" ? 'green-text' : 'red-text'}">${overall_score} / 100</span>`;
            })
            .catch(error => {
                console.error("Error occurred:", error);
                // Optionally, handle error cases
            });
    }




    function updateCounter() {
        const counterElement = document.getElementById("counter");
        counterElement.textContent = `${currentQuestionIndex + 1}/${questions.length}`;
    }

    clearBtn.addEventListener("click", function () {
        clearCanvas();
    });

});






