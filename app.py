from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code')  # Get code from frontend
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    # Save the code to a temporary file
    with open('temp.py', 'w') as f:
        f.write(code)

    try:
        # Run the code inside a Docker container (Python 3.9 image)
        result = subprocess.run(
            ['docker', 'run', '--rm', '-v', os.getcwd() + ':/mnt', 'python:3.9', 'python', '/mnt/temp.py'],
            capture_output=True, text=True, timeout=10
        )
        
        # Return both stdout and stderr from the Docker container
        return jsonify({'output': result.stdout + result.stderr})
    
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Code execution timed out'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
