const task = document.getElementById('task');
const input = document.getElementById('input');
const level = document.getElementById('level');
const hours = document.getElementById('hours');
const learningOptions = document.getElementById('learning-options');
const submit = document.getElementById('submit');
const clear = document.getElementById('clear');
const copy = document.getElementById('copy');
const result = document.getElementById('result');
const status = document.getElementById('status');

const placeholders = {
  qa: 'Example: What is the difference between supervised and unsupervised learning?',
  explain: 'Example: Explain the Pythagoras theorem in simple terms.',
  quiz: 'Paste a passage here. EduGenie will create exactly 3 MCQs.',
  summarize: 'Paste a long educational passage here for quick revision.',
  learn: 'Example: Python for machine learning'
};

task.addEventListener('change', () => {
  const isLearn = task.value === 'learn';
  learningOptions.classList.toggle('hidden', !isLearn);
  input.placeholder = placeholders[task.value];
});

clear.addEventListener('click', () => {
  input.value = '';
  result.className = 'result empty';
  result.textContent = 'Your AI-generated result will appear here.';
  copy.classList.add('hidden');
  status.textContent = 'Ready';
});

copy.addEventListener('click', async () => {
  await navigator.clipboard.writeText(result.innerText);
  status.textContent = 'Copied';
  setTimeout(() => status.textContent = 'Ready', 1200);
});

function renderQuiz(quiz) {
  const questions = quiz.questions || [];
  result.className = 'result';
  result.innerHTML = questions.map((q, i) => `
    <div class="quiz-question">
      <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map((option, j) => `<div class="option">${String.fromCharCode(65 + j)}. ${escapeHtml(option)}</div>`).join('')}
      <div class="answer"><strong>Answer:</strong> ${escapeHtml(q.correct_answer)}<br><small>${escapeHtml(q.explanation)}</small></div>
    </div>
  `).join('');
}

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]));
}

submit.addEventListener('click', async () => {
  const value = input.value.trim();
  if (!value) {
    result.className = 'result';
    result.textContent = 'Please enter something first.';
    return;
  }

  const type = task.value;
  let endpoint = '/qa';
  let body = { question: value };
  if (type === 'explain') { endpoint = '/explain'; body = { text: value }; }
  if (type === 'quiz') { endpoint = '/quiz'; body = { text: value }; }
  if (type === 'summarize') { endpoint = '/summarize'; body = { text: value }; }
  if (type === 'learn') {
    endpoint = '/learn/recommendations';
    body = { topic: value, level: level.value, hours_per_week: Number(hours.value) };
  }

  submit.disabled = true;
  status.textContent = 'Generating…';
  result.className = 'result';
  result.textContent = 'Thinking…';
  copy.classList.add('hidden');

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');

    if (type === 'quiz') renderQuiz(data.quiz);
    else {
      result.className = 'result';
      result.textContent = data.answer || data.explanation || data.summary || data.recommendations || '';
    }
    copy.classList.remove('hidden');
    status.textContent = 'Complete';
  } catch (error) {
    result.className = 'result';
    result.textContent = `Error: ${error.message}`;
    status.textContent = 'Error';
  } finally {
    submit.disabled = false;
  }
});
