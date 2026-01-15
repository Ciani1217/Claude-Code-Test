#!/usr/bin/env python3
"""Simple HTTP server for testing the landing page locally with webhook proxy."""

import http.server
import socketserver
import json
import urllib.request
import urllib.parse
import os

PORT = 8000

# Get n8n webhook URL from environment variable
# Create a .env file with: N8N_WEBHOOK_URL=https://your-webhook-url
N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL')

if not N8N_WEBHOOK_URL:
    print("❌ ERROR: N8N_WEBHOOK_URL environment variable not set!")
    print("   Create a .env file with: N8N_WEBHOOK_URL=https://your-webhook-url")
    print("   Or set it: export N8N_WEBHOOK_URL=https://your-webhook-url")
    exit(1)


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        """Override to add custom logging"""
        print(f"[{self.log_date_time_string()}] {format % args}")
    
    def do_POST(self):
        print(f"[DEBUG] POST request received: {self.path}")
        if self.path == '/webhook' or self.path == '/webhook/':
            print("[DEBUG] Processing webhook request...")
            try:
                # Read the request body to get the message
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                # Parse the JSON to get the message
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    message = data.get('message', '')
                except:
                    message = ''
                
                print(f"[DEBUG] Received message: {message[:50] if message else '(empty)'}")
                
                # n8n webhook expects GET with query parameter
                # Build URL with message as query parameter
                if message:
                    encoded_message = urllib.parse.quote(message)
                    webhook_url_with_params = f"{N8N_WEBHOOK_URL}?message={encoded_message}"
                else:
                    # If no message, try without query params (for testing)
                    webhook_url_with_params = N8N_WEBHOOK_URL
                
                print(f"[DEBUG] Forwarding to n8n (GET): {webhook_url_with_params}")
                
                # Send GET request to n8n webhook
                req = urllib.request.Request(webhook_url_with_params)
                
                try:
                    with urllib.request.urlopen(req) as response:
                        response_data = response.read()
                        response_code = response.getcode()
                        print(f"[DEBUG] n8n responded with status {response_code}")
                        
                        # Send response back to client
                        self.send_response(response_code)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(response_data)
                except urllib.error.HTTPError as e:
                    print(f"[ERROR] n8n returned HTTP {e.code}: {e.reason}")
                    error_body = e.read().decode('utf-8', errors='ignore')
                    print(f"[ERROR] n8n error body: {error_body[:200]}")
                    # Re-raise to be caught by outer exception handler
                    raise
                    
            except Exception as e:
                print(f"[ERROR] Exception occurred: {e}")
                import traceback
                traceback.print_exc()
                # Send error response
                error_response = json.dumps({'error': str(e)}).encode()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(error_response)
        else:
            print(f"[DEBUG] POST to unknown path: {self.path}, returning 404")
            # Return 404 for other POST requests
            self.send_error(404, "Not found")
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"\n  NEURAL INTERFACE SERVER ONLINE")
    print(f"  ================================")
    print(f"  Serving at: http://localhost:{PORT}")
    print(f"  Webhook proxy: /webhook")
    print(f"  Press Ctrl+C to terminate\n")
    httpd.serve_forever()
