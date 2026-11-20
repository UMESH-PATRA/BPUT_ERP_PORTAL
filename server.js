const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 6000;
const BASE_DIR = __dirname;
const NODE_ENV = process.env.NODE_ENV || 'production';
const DEBUG = process.env.DEBUG === 'true';

const ALLOWED_ORIGINS = new Set([
  'http://localhost:5000',
  'http://127.0.0.1:5000',
  'http://localhost:6000',
  'http://127.0.0.1:6000',
  'https://campus.bput.ac.in'
]);

const BLOCKED_PATTERNS = [
  '.env',
  '.git',
  '.agent',
  '.gitignore',
  'server.py',
  'server.js',
  'package.json',
  'tsconfig.json',
  'playwright.config.ts',
  'vercel.json',
  '.py',
  '.ts',
  '.log',
  '.sh',
  '.bat',
  '/scratch/',
  '/tests/',
  '/audits/'
];

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8'
};

const requestHistory = new Map();
const RATE_LIMIT_WINDOW = 60 * 1000; // 60s
const RATE_LIMIT_MAX = 120;

function isRateLimited(ip) {
  const now = Date.now();
  let timestamps = requestHistory.get(ip) || [];
  timestamps = timestamps.filter(t => now - t < RATE_LIMIT_WINDOW);
  if (timestamps.length >= RATE_LIMIT_MAX) {
    return true;
  }
  timestamps.push(now);
  requestHistory.set(ip, timestamps);
  return false;
}

const server = http.createServer((req, res) => {
  const clientIp = req.socket.remoteAddress || '127.0.0.1';

  // 1. Rate Limiting
  if (isRateLimited(clientIp)) {
    res.writeHead(429, {
      'Content-Type': 'application/json; charset=utf-8',
      'Retry-After': '60'
    });
    res.end(JSON.stringify({ error: 'Too Many Requests', retryAfterSeconds: 60 }));
    return;
  }

  // 2. Handle CORS & Security Headers
  const origin = req.headers['origin'] || '';
  const corsOrigin = ALLOWED_ORIGINS.has(origin) ? origin : 'http://localhost:5000';

  const securityHeaders = {
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net https://challenges.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.tailwindcss.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https: blob:; connect-src 'self' https://*.supabase.co wss://*.supabase.co https://*.clerk.accounts.dev https://*.sentry.io; frame-ancestors 'self'; object-src 'none';",
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    'Cross-Origin-Opener-Policy': 'same-origin',
    'X-XSS-Protection': '1; mode=block',
    'Access-Control-Allow-Origin': corsOrigin,
    'Cache-Control': 'no-cache, no-store, must-revalidate'
  };

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      ...securityHeaders,
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
      'Access-Control-Max-Age': '86400'
    });
    res.end();
    return;
  }

  // Normalize URL
  let reqPath = decodeURI(req.url.split('?')[0]);
  if (reqPath === '/' || reqPath === '') {
    reqPath = '/index.html';
  }

  // 3. API Endpoints
  if (reqPath === '/api/health') {
    res.writeHead(200, { ...securityHeaders, 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ status: 'healthy', version: '2.1.0', environment: NODE_ENV }));
    return;
  }

  if (reqPath === '/api/config') {
    res.writeHead(200, { ...securityHeaders, 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ app: 'BPUT Digital Campus', environment: NODE_ENV }));
    return;
  }

  // 4. Block Sensitive & Exposed Files
  const lowerPath = reqPath.toLowerCase();
  for (const pattern of BLOCKED_PATTERNS) {
    if (lowerPath.includes(pattern)) {
      res.writeHead(403, { ...securityHeaders, 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1>403 Forbidden</h1><p>Access to sensitive system assets is restricted.</p>');
      return;
    }
  }

  const filePath = path.join(BASE_DIR, reqPath);

  // Security check: ensure path is strictly within BASE_DIR
  if (!filePath.startsWith(BASE_DIR)) {
    res.writeHead(403, { ...securityHeaders, 'Content-Type': 'text/plain' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      const notFoundPath = path.join(BASE_DIR, '404.html');
      fs.readFile(notFoundPath, (err404, data404) => {
        if (!err404) {
          res.writeHead(404, { ...securityHeaders, 'Content-Type': 'text/html; charset=utf-8' });
          res.end(data404);
        } else {
          res.writeHead(404, { ...securityHeaders, 'Content-Type': 'text/plain' });
          res.end(`404 Not Found: ${reqPath}`);
        }
      });
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, {
      ...securityHeaders,
      'Content-Type': contentType
    });

    const stream = fs.createReadStream(filePath);
    stream.pipe(res);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`\n======================================================`);
  console.log(`🚀 BPUT DIGITAL CAMPUS PLATFORM SERVER (Hardened Node.js)`);
  console.log(`Port: ${PORT} | Environment: ${NODE_ENV}`);
  console.log(`======================================================\n`);
});
