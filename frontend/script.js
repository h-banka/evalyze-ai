document.addEventListener("DOMContentLoaded", () => {
  const preview = document.getElementById("preview");
  const startBtn = document.getElementById("startBtn");
  const stopBtn = document.getElementById("stopBtn");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const loading = document.getElementById("loading");
  const questionText = document.getElementById("question");

  let mediaRecorder;
  let recordedChunks = [];
  let recordedBlob;

  const questions = [
    "Tell us about yourself and your technical skills.",
    "Describe a challenging project you worked on.",
    "Why are you interested in this role?",
    "What are your strengths and areas for improvement?"
  ];

  let currentQuestion = 0;
  questionText.textContent = questions[currentQuestion];

  async function setupCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      preview.srcObject = stream;
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };
      mediaRecorder.onstop = async () => {
        recordedBlob = new Blob(recordedChunks, { type: "video/webm" });
        loading.classList.remove("hidden");

        const formData = new FormData();
        formData.append("file", recordedBlob, "interview.webm");

        try {
          const response = await fetch("http://127.0.0.1:8000/analyze-video", {
            method: "POST",
            body: formData
          });
          const result = await response.json();
          localStorage.setItem("analysisResult", JSON.stringify(result));
          window.location.href = "result.html";
        } catch (error) {
          alert("Error analyzing interview.");
          console.error(error);
        }
      };
    } catch (err) {
      alert("Camera access denied or not available.");
      console.error(err);
    }
  }

  startBtn.addEventListener("click", async () => {
    if (!mediaRecorder) await setupCamera();
    recordedChunks = [];
    mediaRecorder.start();
    startBtn.disabled = true;
    stopBtn.disabled = false;
    analyzeBtn.disabled = false;
  });

  analyzeBtn.addEventListener("click", () => {
    if (currentQuestion < questions.length - 1) {
      currentQuestion++;
      questionText.textContent = questions[currentQuestion];
    } else {
      alert("Last question reached. Click Stop Interview.");
    }
  });

  stopBtn.addEventListener("click", () => {
    mediaRecorder.stop();
    stopBtn.disabled = true;
    analyzeBtn.disabled = true;
  });
});