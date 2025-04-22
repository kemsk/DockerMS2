import os
import subprocess
import threading
import time
from flask import Flask, request, jsonify, Response, redirect
import requests

app = Flask(__name__)

DJANGO_PORT = 8000
django_process = None

def start_django_server():
    """Start the Django development server in a separate thread"""
    global django_process
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
    
    # Kill any existing Django processes
    try:
        subprocess.run(["pkill", "-f", "manage.py"], capture_output=True)
    except Exception:
        pass
    
    # Start Django server
    django_process = subprocess.Popen([
        "python", "manage.py", "runserver", f"127.0.0.1:{DJANGO_PORT}"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for Django to start
    time.sleep(2)
    print(f"Django server started on port {DJANGO_PORT}")

# Start Django when the Flask app starts
with app.app_context():
    # Start Django in a separate thread
    thread = threading.Thread(target=start_django_server)
    thread.daemon = True
    thread.start()

@app.route('/')
def index():
    return redirect('/api/')

@app.route('/health')
def health():
    try:
        # Check if Django API is available
        response = requests.get(f"http://127.0.0.1:{DJANGO_PORT}/api/", timeout=2)
        if response.status_code < 500:
            return {"status": "ok", "django_api": "running"}
        else:
            return {"status": "degraded", "django_api": "error", "status_code": response.status_code}
    except Exception as e:
        return {"status": "error", "django_api": "not running", "error": str(e)}

# Proxy all API requests to the Django server
@app.route('/api/', defaults={'path': ''})
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_to_django(path):
    try:
        url = f"http://127.0.0.1:{DJANGO_PORT}/api/{path}"
        
        # Forward the request to Django
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
        
        # Create the response
        response = Response(resp.content, resp.status_code)
        
        # Add headers from Django response
        for key, value in resp.headers.items():
            if key.lower() != 'content-length':  # Skip content-length as it's added automatically
                response.headers[key] = value
                
        return response
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Django API server error: {str(e)}"}), 503

@app.route('/admin/', defaults={'path': ''})
@app.route('/admin/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_admin_to_django(path):
    try:
        url = f"http://127.0.0.1:{DJANGO_PORT}/admin/{path}"
        
        # Forward the request to Django
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
        
        # Create the response
        response = Response(resp.content, resp.status_code)
        
        # Add headers from Django response
        for key, value in resp.headers.items():
            if key.lower() != 'content-length':  # Skip content-length as it's added automatically
                response.headers[key] = value
                
        return response
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Django Admin server error: {str(e)}"}), 503

# For direct Python execution
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)