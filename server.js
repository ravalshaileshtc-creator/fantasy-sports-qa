const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.static(__dirname));

// API Endpoint for Fantasy Sports Status & Config
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    app: 'FantasyXI Pro',
    ai_qa_system: 'active',
    version: '1.0.0'
  });
});

// SPA Fallback to index.html
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`FantasyXI Pro server running on port ${PORT}`);
});
