import psutil
import time
import sys

def monitor_process(pid, interval=1, duration=None):
    process = psutil.Process(pid)
    start_time = time.time()
    
    while True:
        try:
            process_cpu_percent = process.cpu_percent(interval=interval)
            system_cpu_percent = psutil.cpu_percent(interval=interval, percpu=True)
            memory_info = process.memory_info()
            
            print(f"Time: {time.time() - start_time:.2f}s")
            print(f"Overall CPU: {process_cpu_percent}%")
            print(f"Per-core CPU: {system_cpu_percent}")
            print(f"Memory: {memory_info.rss / 1024 / 1024:.2f} MB")
            print("---")
            
            if duration and (time.time() - start_time) > duration:
                break
        except psutil.NoSuchProcess:
            print("Process has terminated.")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <PID>")
        sys.exit(1)
    
    try:
        pid = int(sys.argv[1])
    except ValueError:
        print("Error: PID must be an integer")
        sys.exit(1)
    
    try:
        monitor_process(pid)
    except psutil.NoSuchProcess:
        print(f"Error: No process found with PID {pid}")
        sys.exit(1)