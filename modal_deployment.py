import asyncio
import os
import modal

app = modal.App("example-app")

current_dir = os.path.dirname(__file__)
print(f"current dir is {current_dir}")

dockerfile_image = modal.Image.from_registry(
    "nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu20.04",
    add_python="3.10"
).workdir(
    "/app"
).apt_install(
    [
        "wget",
        "ffmpeg",
        "portaudio19-dev",
        "python3-pyaudio",
        "gcc",
        "clang",
        "python3-dev",
        "build-essential"
    ],
).pip_install(["psutil", "gputil"])


async def monitor_resources(interval=5):
    import psutil
    import GPUtil
    while True:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage in MB
        memory_info = psutil.virtual_memory()
        memory_total = memory_info.total / (1024 * 1024)  # Total memory in MB
        memory_used = memory_info.used / (1024 * 1024)    # Used memory in MB

        # GPU usage (if available)
        gpus = GPUtil.getGPUs()
        if gpus:
            print("GPU Memory Usage:")
            for gpu in gpus:
                gpu_memory_used = gpu.memoryUsed
                gpu_memory_total = gpu.memoryTotal
                gpu_memory_percent = gpu.memoryUtil * 100
                print(f"GPU {gpu.id}: {gpu_memory_used}/{gpu_memory_total} MB ({gpu_memory_percent:.2f}% used)")
        
        # Top 5 processes by CPU and Memory usage
        processes = [(p.info['pid'], p.info['name'], p.info['memory_info'].rss, p.info['cpu_percent'])
                     for p in psutil.process_iter(['pid','name', 'memory_info', 'cpu_percent'])]
        
        # Sort by memory usage
        top_memory_processes = sorted(processes, key=lambda p: p[2], reverse=True)[:5]
        # Sort by CPU usage
        top_cpu_processes = sorted(processes, key=lambda p: p[3], reverse=True)[:5]

        # Display system CPU and memory
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory_used:.2f} MB / {memory_total:.2f} MB")
        
        print("\nTop 5 Processes by Memory Usage:")
        for pid, name, memory, cpu in top_memory_processes:
            print(f"{name} (PID: {pid}) - Memory: {memory / (1024 * 1024):.2f} MB, CPU: {cpu}%")
        
        print("\nTop 5 Processes by CPU Usage:")
        for pid, name, memory, cpu in top_cpu_processes:
            print(f"{name} (PID: {pid}) - Memory: {memory / (1024 * 1024):.2f} MB, CPU: {cpu}%")
        
        print("-" * 50)
        await asyncio.sleep(interval)



@app.function(
    image=dockerfile_image,
    enable_memory_snapshot=True,
    gpu="a100:1",
    timeout=180,
    cpu=3.1,
    container_idle_timeout=10,
)
def example_function():
    print("Entered example function")

    print(f"Function is running in region: {os.environ.get('MODAL_REGION')} and cloud provider: {os.environ.get('MODAL_CLOUD_PROVIDER')}")
    try:
        print("Started monitoring resources")
        async def monitor():
            await asyncio.wait_for(monitor_resources(), timeout=120)

        asyncio.run(monitor())
    except asyncio.TimeoutError:
        print("finished monitoring resources")


@app.local_entrypoint()
def main():
    print("Output of example function is: ", example_function.remote())
