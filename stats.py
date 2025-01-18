import json
import os
import time
import re
import threading
from collections import Counter
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

log_path = os.getenv("LOG_PATH", "access_log_20190520-125058.log") 
log_stats = {
    "unique_ips": 0,
    "ip_requests": Counter(),
    "status_distribution": Counter(),
    "top_referrers": []
}
file_track = 0
last_modified_time = 0
lock = threading.Lock()
cache_expiry = 1 
last_cache_time = 0

# Sanitize IPs in ip_requests
def sanitize_ip_counter(ip_counter):
    sanitized = Counter()
    ip_regex = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')  # Matches valid IPv4 addresses
    for ip, count in ip_counter.items():
        if ip_regex.match(ip) and all(0 <= int(part) <= 255 for part in ip.split('.')):
            sanitized[ip] += count
    return sanitized

# Sanitize status_distribution
def sanitize_status_distribution(status_distribution):
    sanitized = Counter()
    for key, count in status_distribution.items():
        if re.match(r'^\d{3}$', key):  # Matches exactly 3-digit numbers
            sanitized[key] += count
    return sanitized


# Read the log file and process lines
def process_log_lines(new_data):
    global log_stats
    ip_counter = log_stats["ip_requests"]
    status_counter = log_stats["status_distribution"]
    referrer_counter = Counter()

    for line in new_data.splitlines():
        parts = line.split()
        if len(parts) < 9:  
            continue # Skip lines that don't meet the minimum structure

        ip = parts[0]
        status_code = parts[8]
        referrer = parts[10] if len(parts) > 10 else "-"

        ip_counter[ip] += 1
        status_counter[status_code] += 1
        if parts[5] == '"GET':  # Only count referrers for GET requests
            referrer_counter[referrer] += 1

    sanitized_ips = sanitize_ip_counter(ip_counter)
    sanitized_status = sanitize_status_distribution(status_counter)
    
    with lock:
        log_stats["unique_ips"] = len(sanitized_ips)
        log_stats["ip_requests"] = sanitized_ips
        log_stats["status_distribution"] = sanitized_status
        log_stats["top_referrers"] = referrer_counter.most_common(5)



#  Log file parsing thread
def log_file_parser():
    global file_track, last_modified_time, log_stats

    while True:
        try:
            # Check for file modification
            file_stat = os.stat(log_path)
            current_modified_time = file_stat.st_mtime

            if current_modified_time != last_modified_time:
                file_track = 0  # Reset file tracker if the file was rotated
                last_modified_time = current_modified_time

            # Read new data from the log file
            with open(log_path, 'r') as f:
                f.seek(file_track)
                new_data = f.read(10000)  
                if new_data:
                    process_log_lines(new_data)
                    file_track = f.tell()  # Update offset after reading new lines

        except Exception as e:
            print(f"Error reading log file: {e}")

        time.sleep(1)

# Handler for stats API
class StatsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/stats":
            current_time = time.time()

            with lock:
                if current_time - last_cache_time > cache_expiry:
                    stats_data = log_stats
                else:
                    stats_data = log_stats

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(stats_data, indent=4).encode())
        else:
            self.send_response(404)
            self.end_headers()


# Server setup
def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, StatsHandler)
    print(f"Server running on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    # Start the log file parser in a background thread
    parser_thread = threading.Thread(target=log_file_parser, daemon=True)
    parser_thread.start()

    # Start the HTTP server
    run_server()
