import http.server
import socketserver
import os
import sys
import time
import json
from collections import defaultdict

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------
# 1. ENVIRONMENT CONFIGURATION & PARSING
# ------------------------------------------------------------------------------
def load_env_file():
    env_path = os.path.join(BASE_DIR, '.env')
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

load_env_file()

PORT = int(os.environ.get('PORT', 5000))
NODE_ENV = os.environ.get('NODE_ENV', 'production')
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'

# Whitelisted CORS origins (no wildcard * allowed)
CORS_ORIGINS_RAW = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:5000,http://127.0.0.1:5000,https://campus.bput.ac.in'
)
ALLOWED_ORIGINS = set(o.strip() for o in CORS_ORIGINS_RAW.split(',') if o.strip())

# Rate limiting settings (in-memory sliding window)
RATE_LIMIT_WINDOW = int(os.environ.get('RATE_LIMIT_WINDOW_SECONDS', 60))
RATE_LIMIT_MAX = int(os.environ.get('RATE_LIMIT_MAX_REQUESTS', 1000))
request_history = defaultdict(list)
START_TIME = time.time()

# Sensitive files / patterns that must never be served over HTTP
BLOCKED_PATTERNS = [
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
]

# ------------------------------------------------------------------------------
# 2. HARDENED HTTP REQUEST HANDLER
# ------------------------------------------------------------------------------
class HardenedCampusRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        # In production with debug off, suppress noisy request logging
        if DEBUG:
            super().log_message(format, *args)

    def is_rate_limited(self, client_ip):
        now = time.time()
        timestamps = request_history[client_ip]
        # Purge timestamps outside sliding window
        request_history[client_ip] = [t for t in timestamps if now - t < RATE_LIMIT_WINDOW]
        if len(request_history[client_ip]) >= RATE_LIMIT_MAX:
            return True
        request_history[client_ip].append(now)
        return False

    def is_sensitive_path(self, clean_path):
        normalized = clean_path.lower().replace('\\', '/')
        for pattern in BLOCKED_PATTERNS:
            if pattern in normalized:
                return True
        # Block hidden files or directories starting with .
        parts = normalized.split('/')
        for part in parts:
            if part.startswith('.') and part != '.' and part != '..':
                return True
        return False

    def send_security_headers(self):
        # Content Security Policy (allows CDNs used, blocks untrusted objects and frame ancestors)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net https://challenges.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.tailwindcss.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https: blob:; "
            "connect-src 'self' https://*.supabase.co wss://*.supabase.co https://*.clerk.accounts.dev https://*.sentry.io; "
            "frame-src 'self' https://www.google.com https://maps.google.com; "
            "frame-ancestors 'self'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        self.send_header('Content-Security-Policy', csp)
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')

        # Precise CORS origin validation (no wildcard '*')
        origin = self.headers.get('Origin', '')
        if origin in ALLOWED_ORIGINS:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Vary', 'Origin')
        elif not origin:
            # Same-origin request
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5000')

    def end_headers(self):
        self.send_security_headers()
        super().end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight requests securely
        origin = self.headers.get('Origin', '')
        if origin in ALLOWED_ORIGINS:
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            self.send_header('Access-Control-Max-Age', '86400')
            self.end_headers()
        else:
            self.send_response(403)
            self.end_headers()

    def do_GET(self):
        client_ip = self.client_address[0]

        # 1. Apply Sliding-Window Rate Limiting
        if self.is_rate_limited(client_ip):
            self.send_response(429)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Retry-After', str(RATE_LIMIT_WINDOW))
            self.end_headers()
            err_payload = json.dumps({
                "error": "Too Many Requests",
                "message": "Rate limit threshold reached. Please wait before making further requests.",
                "retryAfterSeconds": RATE_LIMIT_WINDOW
            }).encode('utf-8')
            self.wfile.write(err_payload)
            return

        clean_path = self.path.split('?')[0]

        # 2. Secure REST API Endpoints
        if clean_path == '/api/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            payload = json.dumps({
                "status": "healthy",
                "system": "BPUT Digital Campus Platform",
                "version": "2.1.0",
                "environment": NODE_ENV,
                "debug": DEBUG,
                "uptimeSeconds": round(time.time() - START_TIME, 1)
            }, indent=2).encode('utf-8')
            self.wfile.write(payload)
            return

        if clean_path == '/api/config':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Safe public configuration (secrets and private keys stripped)
            public_cfg = json.dumps({
                "appName": "BPUT Digital Campus Platform",
                "university": "Biju Patnaik University of Technology (BPUT), Odisha",
                "environment": NODE_ENV,
                "authModes": ["institutional", "credentials"],
                "rateLimit": {
                    "window": RATE_LIMIT_WINDOW,
                    "maxRequests": RATE_LIMIT_MAX
                }
            }, indent=2).encode('utf-8')
            self.wfile.write(public_cfg)
            return

        # 3. Block Sensitive / Exposed Files (Prevent Source Code / Env Leakage)
        if self.is_sensitive_path(clean_path):
            self.send_response(403)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            msg = (
                "<!DOCTYPE html><html><head><title>403 Forbidden</title></head>"
                "<body style='font-family:sans-serif;text-align:center;padding:50px;background:#0f172a;color:#f8fafc;'>"
                "<h1>403 Forbidden</h1>"
                "<p>Direct access to institutional source code and protected system assets is restricted.</p>"
                "</body></html>"
            ).encode('utf-8')
            self.wfile.write(msg)
            return

        # 4. Default root path to /index.html
        if clean_path == '/' or clean_path == '':
            self.path = '/index.html'
            clean_path = '/index.html'

        # 5. Path Traversal & Existence Check (serve custom 404.html if not found)
        req_rel = clean_path.lstrip('/')
        full_path = os.path.abspath(os.path.join(BASE_DIR, req_rel))

        # Enforce directory confinement
        if not full_path.startswith(BASE_DIR):
            self.send_response(403)
            self.end_headers()
            return

        if not os.path.exists(full_path) or os.path.isdir(full_path):
            four_oh_four = os.path.join(BASE_DIR, '404.html')
            if os.path.exists(four_oh_four):
                self.send_response(404)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(four_oh_four, 'rb') as f:
                    self.wfile.write(f.read())
                return

        return super().do_GET()

# ------------------------------------------------------------------------------
# 3. SERVER ENTRYPOINT
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    class ReusableTCPServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    try:
        with ReusableTCPServer(('0.0.0.0', PORT), HardenedCampusRequestHandler) as httpd:
            print("=" * 60)
            print(f">> BPUT DIGITAL CAMPUS PLATFORM — HARDENED SECURE SERVER")
            print("=" * 60)
            print(f"Environment:       {NODE_ENV} (Debug: {DEBUG})")
            print(f"Local Access:      http://localhost:{PORT}")
            print(f"Network Access:    http://127.0.0.1:{PORT}")
            print(f"Rate Limiting:     {RATE_LIMIT_MAX} req / {RATE_LIMIT_WINDOW}s")
            print(f"Security Headers:  CSP, X-Frame-Options, Nosniff, Referrer, COOP")
            print(f"CORS Whitelist:    {len(ALLOWED_ORIGINS)} verified origins")
            print("\nEndpoints:")
            print(f"  * Public Portal:     http://localhost:{PORT}/index.html")
            print(f"  * Student Auth:      http://localhost:{PORT}/student-auth.html")
            print(f"  * Admin Auth:        http://localhost:{PORT}/admin-auth.html")
            print(f"  * API Health:        http://localhost:{PORT}/api/health")
            print(f"  * API Safe Config:   http://localhost:{PORT}/api/config")
            print("=" * 60 + "\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
