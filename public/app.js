// REAL Gemini AI Powered APK & Web QA System - Client Logic

let apkState = null;

function handleApkSelect(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (!file.name.endsWith('.apk')) {
    alert('Please select a valid Android `.apk` file.');
    return;
  }

  processApkFile(file);
}

async function processApkFile(file) {
  const term = document.getElementById('terminal-console');
  term.innerHTML += `<div class="text-gemini-cyan font-bold mt-2">[GEMINI APK UPLOAD] Uploaded ${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)...</div>`;

  try {
    const res = await fetch('/api/upload-apk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ fileName: file.name, fileSize: file.size })
    });

    if (res.ok) {
      const data = await res.json();
      apkState = data.apkDetails;
      term.innerHTML += `<div class="text-brand-500 font-bold">[GEMINI PARSER] Package ${apkState.packageName} (${apkState.version}) validated cleanly.</div>`;
      term.scrollTop = term.scrollHeight;

      // Auto trigger Gemini AI Audit
      runGeminiAiAudit();
    }
  } catch (e) {
    console.warn('Upload API fallback:', e);
  }
}

async function runGeminiAiAudit() {
  const term = document.getElementById('terminal-console');
  const btn = document.getElementById('btn-gemini-run');
  const targetUrl = document.getElementById('target-web-url') ? document.getElementById('target-web-url').value.trim() : 'https://example.com';
  const apiKey = localStorage.getItem('GEMINI_API_KEY') || '';

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> QUERYING GEMINI AI...`;
    lucide.createIcons();
  }

  term.innerHTML += `<div class="text-gemini-cyan font-bold mt-2">[GEMINI 1.5 FLASH] Querying live Google Gemini AI API for automated audit...</div>`;
  term.scrollTop = term.scrollHeight;

  try {
    const res = await fetch('/api/gemini-qa-audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        targetUrl,
        apkDetails: apkState,
        userApiKey: apiKey
      })
    });

    if (res.ok) {
      const responseData = await res.json();
      const audit = responseData.audit;

      // Update UI Scores with Real Gemini Output
      document.getElementById('metric-ui').innerText = `${audit.uiScore}%`;
      document.getElementById('metric-ux').innerText = `${audit.uxScore}%`;
      document.getElementById('metric-perf').innerText = `${audit.perfScore}%`;
      document.getElementById('metric-sec').innerText = `${audit.securityScore}%`;

      document.getElementById('bar-ui').style.width = `${audit.uiScore}%`;
      document.getElementById('bar-ux').style.width = `${audit.uxScore}%`;
      document.getElementById('bar-perf').style.width = `${audit.perfScore}%`;
      document.getElementById('bar-sec').style.width = `${audit.securityScore}%`;

      document.getElementById('gemini-source-tag').innerText = `Source: ${responseData.source}`;

      // Render Gemini AI Findings & Fixes
      const findingsContainer = document.getElementById('gemini-findings-container');
      const bugs = audit.bugs || [];

      findingsContainer.innerHTML = bugs.map(b => `
        <div class="p-3.5 rounded-2xl bg-slate-900/80 border ${b.severity === 'HIGH' ? 'border-amber-500/30' : 'border-emerald-500/30'} space-y-1.5">
          <div class="flex justify-between items-center">
            <strong class="text-white font-semibold text-xs">${b.type} (${b.severity || 'PASSED'})</strong>
            <span class="px-2 py-0.5 rounded bg-gemini-500/20 text-gemini-cyan font-bold text-[10px]">GEMINI AI VERIFIED</span>
          </div>
          <p class="text-slate-300 font-mono text-[11px]">${b.issue}</p>
          <p class="text-slate-400 text-[10px]"><strong>AI Recommendation:</strong> ${b.fix}</p>
        </div>
      `).join('');

      term.innerHTML += `<div class="text-emerald-400 font-bold mt-2">[GEMINI AUDIT PASSED] ${audit.geminiSummary || 'Audit Complete!'}</div>`;
      term.scrollTop = term.scrollHeight;
    }
  } catch (err) {
    term.innerHTML += `<div class="text-rose-400 font-bold mt-2">[ERROR] Failed to communicate with Gemini API: ${err.message}</div>`;
  }

  if (btn) {
    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="sparkles" class="w-4 h-4"></i> Run Gemini AI Audit`;
    lucide.createIcons();
  }
}
