import subprocess

def run_server():
    command = ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8081", "--reload"]
    subprocess.run(command)

if __name__ == "__main__":
    run_server()
