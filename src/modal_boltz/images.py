import modal

boltz_image = modal.Image.debian_slim(python_version="3.12").run_commands(
    "uv pip install --system --compile-bytecode boltz==2.1.1"
)


