import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# The exact payload from your original Worker
PAYLOAD = {
    "wssUrl": "wss://code-relay-2-main-k2-17f8e1c8a668.herokuapp.com/ws",
    "wssUrls": ["wss://code-relay-2-main-k2-17f8e1c8a668.com/ws"],
    "authUrls": ["https://code-auth-1-d4-k2-be7a0248470d.herokuapp.com/check"],
    "authUrl": "https://code-auth-1-d4-k2-be7a0248470d.herokuapp.com/check",
    "regionalUrl": "wss://wss.rebatecodeclaimer.com/ws",
    "healthUrl": "wss://health-dashh-z2-k2-8ab8f55fc397.herokuapp.com/ws",
    "healthBase": "https://health-dashh-z2-k2-8ab8f55fc397.herokuapp.com/",
    "dashboardUrl": "https://code-dahsboard-0w-k2-f0484eadf33c.herokuapp.com/api/claim-report",
    "dashboardBase": "https://code-dahsboard-0w-k2-f0484eadf33c.herokuapp.com/",
    "meta": {
        "region": "AWS - EU-east",
        "country": "Global",
        "selected_node_stats": "Internal"
    }
}

class LoadBalancerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        """Serve the JSON payload"""
        # Note: We cannot easily get 'Country' like CF does without a GeoIP database.
        # This keeps the response structure identical to your Worker.
        
        response_data = json.dumps(PAYLOAD, indent=2).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "public, max-age=300")
        self.send_header("Content-Length", str(len(response_data)))
        self.end_headers()
        self.wfile.write(response_data)

    # Silence logs to save CPU on Render
    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    # Render provides the PORT via environment variable
    import os
    port = int(os.environ.get("PORT", 8080))
    server = ThreadingHTTPServer(("0.0.0.0", port), LoadBalancerHandler)
    print(f"Server started on port {port}")
    server.serve_forever()
