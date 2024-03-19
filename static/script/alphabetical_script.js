document.addEventListener("DOMContentLoaded", function () {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
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
        context.lineWidth = 10;
        context.lineCap = "round";
        context.strokeStyle = "#000";

        context.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        context.stroke();
        context.beginPath();
        context.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
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
            updateCounter();
        }
    });

    nextBtn.addEventListener("click", function () {
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
            clearCanvas();
            updateCounter();
        }
    });

    submitBtn.addEventListener("click", function () {
        const dataUrl = canvas.toDataURL();
        console.log(dataUrl);

        fetch("/upload-alphabets", {
            method: "POST",
            body: new URLSearchParams({
                img_data: dataUrl
            }),
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
            .then(response => {
                if (response.ok) {
                    console.log("Image saved successfully");
                    // Optionally, you can perform additional actions after image is saved
                } else {
                    console.error("Failed to save image");
                    // Optionally, handle error cases
                }
            })
            .catch(error => {
                console.error("Error occurred:", error);
                // Optionally, handle error cases
            });
    });

    function updateCounter() {
        const counterElement = document.getElementById("counter");
        counterElement.textContent = `${currentQuestionIndex + 1}/${questions.length}`;
    }

    clearBtn.addEventListener("click", function () {
        clearCanvas();
    });

});






