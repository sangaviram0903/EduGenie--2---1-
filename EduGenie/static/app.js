const state = { task: "qa" };

const taskConfig = {
  qa: {
    button: "Get Answer",
    endpoint: "/qa",
    buildBody: () => ({ text: value("qa-input") }),
  },
  explain: {
    button: "Explain",
    endpoint: "/explain",
    buildBody: () => ({ topic: value("explain-input") }),
  },
  quiz: {
    button: "Generate Quiz",
    endpoint: "/quiz",
    buildBody: () => ({ text: value("quiz-input") }),
  },
  summarize: {
    button: "Summarize",
    endpoint: "/summarize",
    buildBody: () => ({ text: value("summary-input") }),
  },
  learn: {
    button: "Get Learning Recommendations",
    endpoint: "/learn/recommendations",
    buildBody: () => ({
      topic: value("learn-input"),
      level: value("level-input"),
    }),
  },
};

function value(id) {
  return document.getElementById(id).value.trim();
}

function setTask(task) {
  state.task = task;

  document.querySelectorAll(".task-tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.task === task);
  });

  document.querySelectorAll(".task-fields").forEach((section) => {
    section.classList.add("hidden");
  });

  document.getElementById(`${task}-fields`).classList.remove("hidden");
  document.getElementById("submit-button").textContent = taskConfig[task].button;
  clearResult();
}

function clearResult() {
  const result = document.getElementById("result");
  result.classList.add("hidden");
  result.innerHTML = "";
  setStatus("");
}

function setStatus(message) {
  const status = document.getElementById("status");
  if (!message) {
    status.classList.add("hidden");
    status.textContent = "";
    return;
  }
  status.classList.remove("hidden");
  status.textContent = message;
}

function renderText(title, text) {
  const result = document.getElementById("result");
  result.classList.remove("hidden");
  result.innerHTML = `<h3>${escapeHtml(title)}</h3><p>${escapeHtml(text)}</p>`;
}

function renderQuiz(questions) {
  const result = document.getElementById("result");
  result.classList.remove("hidden");

  result.innerHTML = `
    <h3>Quiz</h3>
    <p>Choose an answer for each question, then click <b>Check Answer</b>.</p>
    ${questions.map((q, index) => `
      <article class="quiz-question" data-question="${index}">
        <strong>${index + 1}. ${escapeHtml(q.question)}</strong>
        <div>
          ${q.options.map((option) => `
            <label class="option">
              <input type="radio" name="q-${index}" value="${escapeAttr(option)}" />
              ${escapeHtml(option)}
            </label>
          `).join("")}
        </div>
        <button class="small-button check-answer" type="button"
          data-index="${index}">Check Answer</button>
        <div class="quiz-feedback" id="feedback-${index}"></div>
      </article>
    `).join("")}
  `;

  result.querySelectorAll(".check-answer").forEach((button) => {
    button.addEventListener("click", () => {
      const index = Number(button.dataset.index);
      const question = questions[index];
      const selected = result.querySelector(`input[name="q-${index}"]:checked`);
      const feedback = document.getElementById(`feedback-${index}`);

      if (!selected) {
        feedback.textContent = "Please select an option.";
        return;
      }

      if (selected.value === question.answer) {
        feedback.textContent = `Correct! ${question.explanation || ""}`;
      } else {
        feedback.textContent = `Not quite. Correct answer: ${question.answer}. ${question.explanation || ""}`;
      }
    });
  });
}

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(text) {
  return escapeHtml(text);
}

async function submitTask(event) {
  event.preventDefault();

  const config = taskConfig[state.task];
  const body = config.buildBody();

  if (Object.values(body).some((item) => !item)) {
    setStatus("Please enter the required information.");
    return;
  }

  const button = document.getElementById("submit-button");
  button.disabled = true;
  setStatus("EduGenie is thinking...");
  clearResult();

  try {
    const response = await fetch(config.endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "The server returned an error.");
    }

    setStatus("Completed.");

    if (state.task === "qa") {
      renderText("Answer", data.answer);
    } else if (state.task === "explain") {
      renderText("Explanation", data.explanation);
    } else if (state.task === "summarize") {
      renderText("Summary", data.summary);
    } else if (state.task === "learn") {
      renderText(`Learning Path — ${data.topic} (${data.level})`, data.recommendations);
    } else if (state.task === "quiz") {
      renderQuiz(data.questions);
    }
  } catch (error) {
    setStatus(error.message || "Something went wrong.");
  } finally {
    button.disabled = false;
  }
}

document.querySelectorAll(".task-tab").forEach((button) => {
  button.addEventListener("click", () => setTask(button.dataset.task));
});

document.getElementById("task-form").addEventListener("submit", submitTask);
