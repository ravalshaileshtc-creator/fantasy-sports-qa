const express = require('express');
const path = require('path');
const https = require('https');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(__dirname));

// REAL Website Audit Endpoint
app.post('/api/audit-url', async (req, res) => {
  const { url } = req.body;
  if (!url) {
    return res.status(400).json({ error: 'URL parameter is required.' });
  }

  const startTime = Date.now();

  try {
    const parsedUrl = new URL(url);
    const client = parsedUrl.protocol === 'https:' ? https : http;

    const requestOptions = {
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Antigravity-AI-QA-Engine/2.0'
      },
      timeout: 10000
    };

    const reqStream = client.request(url, requestOptions, (response) => {
      let body = '';
      const responseTime = Date.now() - startTime;
      const headers = response.headers;

      response.on('data', (chunk) => {
        body += chunk;
      });

      response.on('end', () => {
        // --- 1. REAL SECURITY AUDIT ---
        const isHttps = parsedUrl.protocol === 'https:';
        const hasHsts = !!headers['strict-transport-security'];
        const hasXFrame = !!headers['x-frame-options'];
        const hasCsp = !!headers['content-security-policy'];
        const hasXss = !!headers['x-xss-protection'];

        let securityScore = 60;
        if (isHttps) securityScore += 15;
        if (hasHsts) securityScore += 10;
        if (hasXFrame) securityScore += 5;
        if (hasCsp) securityScore += 5;
        if (hasXss) securityScore += 5;
        securityScore = Math.min(100, securityScore);

        // --- 2. REAL PERFORMANCE AUDIT ---
        const payloadSizeKB = (Buffer.byteLength(body, 'utf8') / 1024).toFixed(1);
        let perfScore = 100;

        if (responseTime > 3000) perfScore -= 40;
        else if (responseTime > 1500) perfScore -= 20;
        else if (responseTime > 800) perfScore -= 10;

        if (payloadSizeKB > 5000) perfScore -= 20;
        else if (payloadSizeKB > 2000) perfScore -= 10;

        perfScore = Math.max(40, Math.min(100, perfScore));

        // --- 3. REAL DOM & UI AUDIT ---
        const hasTitle = /<title[^>]*>([^<]+)<\/title>/i.test(body);
        const hasViewport = /<meta[^>]*name=["']viewport["']/i.test(body);
        const hasH1 = /<h1[^>]*>/i.test(body);
        const imgTags = (body.match(/<img[^>]+>/gi) || []).length;
        const imgWithAlt = (body.match(/<img[^>]+alt=["'][^"']+["']/gi) || []).length;

        let uiScore = 70;
        if (hasTitle) uiScore += 10;
        if (hasViewport) uiScore += 10;
        if (hasH1) uiScore += 10;
        uiScore = Math.min(100, uiScore);

        let uxScore = hasViewport ? 95 : 65;

        // REAL Detected Issues
        const bugs = [];
        if (!isHttps) {
          bugs.push({ type: 'Security Warning', issue: 'Insecure Connection (HTTP instead of HTTPS)', fix: 'Enforce SSL certificate and redirect HTTP to HTTPS.' });
        }
        if (!hasHsts) {
          bugs.push({ type: 'Security Risk', issue: 'Missing Strict-Transport-Security (HSTS) Header', fix: 'Add Strict-Transport-Security header in web server config.' });
        }
        if (!hasViewport) {
          bugs.push({ type: 'Mobile UX Bug', issue: 'Missing meta viewport tag for mobile scaling', fix: 'Add <meta name="viewport" content="width=device-width, initial-scale=1.0"> in head.' });
        }
        if (imgTags > 0 && imgWithAlt < imgTags) {
          bugs.push({ type: 'Accessibility Issue', issue: `${imgTags - imgWithAlt} image(s) missing alt attributes`, fix: 'Add alt description to all <img> tags.' });
        }
        if (responseTime > 2000) {
          bugs.push({ type: 'Performance Bottleneck', issue: `Slow Server Response Time (${responseTime}ms)`, fix: 'Optimize server logic, enable compression & CDN caching.' });
        }

        res.json({
          url,
          statusCode: response.statusCode,
          responseTimeMs: responseTime,
          payloadSizeKB,
          isHttps,
          uiScore,
          uxScore,
          perfScore,
          secScore: securityScore,
          bugs
        });
      });
    });

    reqStream.on('error', (err) => {
      res.status(500).json({ error: `Failed to connect to target URL: ${err.message}` });
    });

    reqStream.end();
  } catch (err) {
    res.status(400).json({ error: `Invalid URL format: ${err.message}` });
  }
});

// SPA Fallback to index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Universal AI QA Server running on port ${PORT}`);
});
