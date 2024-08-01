import os
import subprocess
import sys
import modal

app = modal.App("example-app")

current_dir = os.path.dirname(__file__)
print(f"current dir is {current_dir}")

dockerfile_image = modal.Image.from_dockerfile(
    path="Dockerfile",
    context_mount=modal.Mount.from_local_dir(
        local_path=current_dir,
        remote_path=".",
    ),
).run_commands([
    [f"cd /app && conda run -n example python data_preprocessing.py --destination_tensor_file_path /app/torso_imgs_tensor.pt"]
])

# .run_commands([
#     f"cd /app && conda run -n example python -c \"import torch; torch.save(torch.randn(10**9 // 4), './torch_tensor.pt')\""
# ])


@app.function(
    image=dockerfile_image,
    gpu="a100:1",
    timeout=30,
    cpu=4.0,
)
def example_function():
    print("Entered example function")

    process = subprocess.Popen(
        ["conda", "run", "-n", "example", "--no-capture-output", "python", "-u", "test_script.py"],
        cwd="/app",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    for line in iter(process.stdout.readline, ''):
        print(line, end='')  # Print to console
        sys.stdout.flush()   # Ensure it's displayed immediately

    process.stdout.close()
    return_code = process.wait()

    if return_code:
        raise subprocess.CalledProcessError(
            return_code,
            ["conda", "run", "-n", "example", "--no-capture-output", "python", "-u", "test_script.py"]
        )

@app.local_entrypoint()
def main():
    print("Output of example function is: ", example_function.remote())
