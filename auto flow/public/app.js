let selectedArticle = null;
let pollTimer = null;

// Dynamic API Base URL detection for Web & Android APK
const API_BASE = (window.location.protocol === 'file:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? (window.location.origin.includes('http') ? window.location.origin : 'http://localhost:3000')
  : window.location.origin;

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('scrapeBtn').addEventListener('click', fetchNews);
  document.getElementById('generateBtn').addEventListener('click', runPipeline);
  
  // Initial status check
  checkStatus();
});

function setTopic(topic) {
  document.getElementById('topicInput').value = topic;
  fetchNews();
}

async function fetchNews() {
  const topic = document.getElementById('topicInput').value.trim();
  const newsList = document.getElementById('newsList');
  newsList.innerHTML = '<div class="placeholder-text">Fetching news articles...</div>';

  try {
    const resp = await fetch(`${API_BASE}/api/news?topic=${encodeURIComponent(topic)}`);
    const data = await resp.json();

    if (data.success && data.articles.length > 0) {
      newsList.innerHTML = '';
      data.articles.forEach((art, idx) => {
        const card = document.createElement('div');
        card.className = `news-card ${idx === 0 ? 'selected' : ''}`;
        card.innerHTML = `
          <h4>${art.title}</h4>
          <p><strong>Source:</strong> ${art.source} | ${art.published}</p>
        `;
        card.addEventListener('click', () => {
          document.querySelectorAll('.news-card').forEach(c => c.classList.remove('selected'));
          card.classList.add('selected');
          selectedArticle = art;
        });
        newsList.appendChild(card);
      });
      selectedArticle = data.articles[0];
    } else {
      newsList.innerHTML = '<div class="placeholder-text">No articles found. Enter a custom topic above.</div>';
    }
  } catch (err) {
    console.error(err);
    newsList.innerHTML = '<div class="placeholder-text">Failed to connect to news API.</div>';
  }
}

async function runPipeline() {
  const topic = document.getElementById('topicInput').value.trim();
  const generateBtn = document.getElementById('generateBtn');

  generateBtn.disabled = true;
  generateBtn.innerText = '⏳ Pipeline Running (11 Stages)...';

  try {
    const resp = await fetch(`${API_BASE}/api/generate-video`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic })
    });
    const data = await resp.json();

    if (data.success) {
      startPolling();
    } else {
      alert(data.message || 'Pipeline failed to start.');
      generateBtn.disabled = false;
      generateBtn.innerText = '🚀 Run Full 11-Stage Video Pipeline';
    }
  } catch (err) {
    console.error(err);
    alert('Error connecting to backend server.');
    generateBtn.disabled = false;
    generateBtn.innerText = '🚀 Run Full 11-Stage Video Pipeline';
  }
}

function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTimer = setInterval(checkStatus, 2000);
}

async function checkStatus() {
  try {
    const resp = await fetch(`${API_BASE}/api/status`);
    const data = await resp.json();

    updateStepper(data.stage, data.stageName, data.status);
    updateTerminalLogs(data.logs || []);

    if (data.status === 'COMPLETED' && data.manifest) {
      clearInterval(pollTimer);
      document.getElementById('generateBtn').disabled = false;
      document.getElementById('generateBtn').innerText = '🚀 Run Full 11-Stage Video Pipeline';
      renderFinalResults(data.manifest);
    } else if (data.status === 'FAILED') {
      clearInterval(pollTimer);
      document.getElementById('generateBtn').disabled = false;
      document.getElementById('generateBtn').innerText = '🚀 Run Full 11-Stage Video Pipeline';
    } else if (data.status === 'RUNNING') {
      if (!pollTimer) startPolling();
    }
  } catch (err) {
    console.error('Status check error:', err);
  }
}

function updateStepper(currentStage, stageName, globalStatus) {
  for (let i = 1; i <= 11; i++) {
    const stepEl = document.getElementById(`step-${i}`);
    if (!stepEl) continue;

    const statusSpan = stepEl.querySelector('.step-status');

    if (i < currentStage || globalStatus === 'COMPLETED') {
      stepEl.className = 'step-item completed';
      statusSpan.innerText = 'Done';
    } else if (i === currentStage && globalStatus === 'RUNNING') {
      stepEl.className = 'step-item active';
      statusSpan.innerText = 'Processing...';
    } else {
      stepEl.className = 'step-item';
      statusSpan.innerText = 'Idle';
    }
  }

  const sysStatus = document.getElementById('systemStatus');
  if (globalStatus === 'RUNNING') {
    sysStatus.innerHTML = `<span class="pulse-dot" style="background:#f59e0b"></span> Stage ${currentStage}/11: ${stageName}`;
  } else if (globalStatus === 'COMPLETED') {
    sysStatus.innerHTML = `<span class="pulse-dot"></span> Ready 1-Min Video Completed!`;
  }
}

function updateTerminalLogs(logs) {
  const consoleLogs = document.getElementById('consoleLogs');
  consoleLogs.innerText = logs.join('\n');
  consoleLogs.scrollTop = consoleLogs.scrollHeight;
}

function renderFinalResults(manifest) {
  // Show Video
  const placeholder = document.getElementById('videoPlaceholder');
  const player = document.getElementById('finalVideoPlayer');
  placeholder.classList.add('hidden');
  player.classList.remove('hidden');
  player.src = '/output/final_1min_video.mp4?t=' + Date.now();

  // Downloads
  const downloadBar = document.getElementById('downloadBar');
  const downloadVideoBtn = document.getElementById('downloadVideoBtn');
  const downloadThumbBtn = document.getElementById('downloadThumbBtn');
  downloadBar.classList.remove('hidden');
  downloadVideoBtn.href = '/output/final_1min_video.mp4';
  downloadThumbBtn.href = '/output/thumbnail.jpg';

  // Thumbnail
  const thumbPreview = document.getElementById('thumbPreview');
  const thumbImg = document.getElementById('thumbImg');
  thumbPreview.classList.remove('hidden');
  thumbImg.src = '/output/thumbnail.jpg?t=' + Date.now();

  // Script
  if (manifest.script) {
    document.getElementById('scriptTitle').innerText = manifest.script.title || '60s Short Script';
    document.getElementById('scriptHook').innerHTML = `<strong>Hook:</strong> ${manifest.script.hook || ''}`;
    document.getElementById('scriptFull').innerText = manifest.script.full_script || '';
  }

  // Scenes
  if (manifest.scenes) {
    const grid = document.getElementById('scenesGrid');
    grid.innerHTML = '';
    manifest.scenes.forEach(s => {
      const card = document.createElement('div');
      card.className = 'scene-card-item';
      card.innerHTML = `
        <h5>Scene 0${s.scene_number} (${s.duration}s)</h5>
        <p><strong>Narration:</strong> ${s.narration}</p>
        <p><strong>Visual Prompt:</strong> <em>${s.video_prompt || s.shot_description}</em></p>
      `;
      grid.appendChild(card);
    });
  }
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

  event.target.classList.add('active');
  document.getElementById(tabId).classList.add('active');
}
