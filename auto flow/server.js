const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/output', express.static(path.join(__dirname, 'output')));
app.use('/temp', express.static(path.join(__dirname, 'temp')));

let currentJob = {
  status: 'IDLE',
  stage: 0,
  stageName: 'Idle',
  logs: [],
  manifest: null
};

// Endpoint: Fetch trending news
app.get('/api/news', (req, res) => {
  const topic = req.query.topic || 'Artificial Intelligence';
  const py = spawn('python', ['-c', `
import json
from news_scraper import fetch_trending_news
print(json.dumps(fetch_trending_news(${JSON.stringify(topic)})))
  `]);

  let output = '';
  py.stdout.on('data', data => output += data.toString());
  py.on('close', () => {
    try {
      res.json({ success: true, articles: JSON.parse(output.trim()) });
    } catch (e) {
      res.status(500).json({ success: false, error: 'Failed to parse news output' });
    }
  });
});

// Endpoint: Trigger full 11-stage pipeline
app.post('/api/generate-video', (req, res) => {
  const { topic } = req.body;
  
  if (currentJob.status === 'RUNNING') {
    return res.status(400).json({ success: false, message: 'A video generation job is already running.' });
  }

  currentJob = {
    status: 'RUNNING',
    stage: 1,
    stageName: 'Starting Pipeline',
    logs: ['Initializing 11-stage news-to-video pipeline...'],
    manifest: null
  };

  const py = spawn('python', ['-u', 'pipeline.py', '--topic', topic || 'Artificial Intelligence']);

  py.stdout.on('data', data => {
    const text = data.toString().trim();
    console.log(text);
    currentJob.logs.push(text);

    const stageMatch = text.match(/\[Stage (\d+)\/11\] ([^:]+): (.*)/);
    if (stageMatch) {
      currentJob.stage = parseInt(stageMatch[1]);
      currentJob.stageName = stageMatch[2];
    }
  });

  py.stderr.on('data', data => {
    console.error(data.toString());
  });

  py.on('close', code => {
    if (code === 0) {
      currentJob.status = 'COMPLETED';
      currentJob.stage = 11;
      currentJob.stageName = 'Ready 1 Minute Video';
      
      const manifestPath = path.join(__dirname, 'output', 'video_manifest.json');
      if (fs.existsSync(manifestPath)) {
        currentJob.manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
      }
    } else {
      currentJob.status = 'FAILED';
      currentJob.logs.push(`Pipeline exited with error code ${code}`);
    }
  });

  res.json({ success: true, message: 'Pipeline launched', job: currentJob });
});

// Endpoint: Check live job status
app.get('/api/status', (req, res) => {
  const manifestPath = path.join(__dirname, 'output', 'video_manifest.json');
  let manifest = currentJob.manifest;

  if (!manifest && fs.existsSync(manifestPath)) {
    try {
      manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    } catch (e) {}
  }

  res.json({
    ...currentJob,
    manifest
  });
});

app.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(`  11-Stage News-to-Video Generator Server Active`);
  console.log(`  Dashboard URL: http://localhost:${PORT}`);
  console.log(`====================================================`);
});
