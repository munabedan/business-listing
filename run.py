import subprocess

# Run cdn.py
cdn_process = subprocess.Popen(['python3', 'cdn.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("cdn.py process started.")

# Run main.py
server_process = subprocess.Popen(['python3', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("server.py process started.")

# Run uvicorn main:app on port 8000
uvicorn_process = subprocess.Popen(['uvicorn', 'main:app', '--port', '8000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("uvicorn process started on port 8000.")

# Print the output of uvicorn if needed
uvicorn_output, uvicorn_error = uvicorn_process.communicate()
print(uvicorn_output.decode("utf-8"))

# Check for errors in cdn.py
cdn_output, cdn_error = cdn_process.communicate()
if cdn_process.returncode != 0:
    print(f'Error running cdn.py: {cdn_error.decode("utf-8")}')
    exit(1)

# Check for errors in main.py
server_output, server_error = server_process.communicate()
if server_process.returncode != 0:
    print(f'Error running main.py: {server_error.decode("utf-8")}')
    exit(1)
