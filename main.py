import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# The exact payload from your original Worker
PAYLOAD = {
    "wssUrl": "wss://code-ldr-d1f9b35cf1b6.herokuapp.com/ws",
    "wssUrls": ["wss://code-ldr-d1f9b35cf1b6.herokuapp.com/ws"],
    "authUrls": ["https://code-auth-843da34b0699.herokuapp.com/check"],
    "authUrl": "https://code-auth-843da34b0699.herokuapp.com/check",
    "regionalUrl": "https://code.hh123.site",
    "healthUrl": "wss://health-api-605a7dae1f99.herokuapp.com/ws",
    "healthBase": "https://health-api-605a7dae1f99.herokuapp.com.com/",
    "dashboardUrl": "https://code-dash1-a6f0feeb4e8b.herokuapp.com/api/claim-report",
    "dashboardBase": "https://code-dash1-a6f0feeb4e8b.herokuapp.com/",
    "meta": {
        "region": "AWS - EU-east",
        "country": "UNKNOWN",
        "selected_node_stats": "Internal Load Balancing Active"
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
