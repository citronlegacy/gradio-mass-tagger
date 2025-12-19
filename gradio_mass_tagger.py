import os
import gradio as gr
import subprocess
import re

# === CONFIG ===
SCRIPT_PATH = f"sd-scripts/finetune/tag_images_by_wd14_tagger.py"
VENV_PYTHON = f"sd-scripts/venv/bin/accelerate"
MODEL_REPO = "SmilingWolf/wd-v1-4-convnextv2-tagger-v2"

def load_last_directory():
    try:
        with open("last_directory.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_last_directory(path):
    with open("last_directory.txt", "w") as f:
        f.write(path)

def run_tagger_on_folder(folder_path, batch_size, threshold):
    command = [
        VENV_PYTHON, "launch",
        "--num_processes", "1",
        "--num_machines", "1",
        "--mixed_precision", "no",
        "--dynamo_backend", "no",
        SCRIPT_PATH,
        "--append_tags",
        "--batch_size", str(batch_size),
        "--caption_extension", ".txt",
        "--caption_separator", ",",
        "--debug",
        "--frequency_tags",
        "--general_threshold", str(threshold),
        "--max_data_loader_n_workers", "2",
        "--onnx",
        "--recursive",
        "--remove_underscore",
        "--repo_id", MODEL_REPO,
        "--thresh", str(threshold),
        folder_path
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    output_lines = []
    progress_pattern = re.compile(r'(\d+)%')
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.strip())  # Output to terminal
        output_lines.append(line.strip())
        match = progress_pattern.search(line)
        if match:
            perc = int(match.group(1)) / 100
            yield "\n".join(output_lines), gr.update(value=perc, visible=True)
    process.wait()
    if process.returncode == 0:
        yield "\n".join(output_lines) + "\nTagging completed successfully.", gr.update(value=1, visible=True)
    else:
        yield "\n".join(output_lines) + f"\nTagging failed. Error: {''.join(output_lines)}", gr.update(visible=False)

def tag_images(directory, batch_size, threshold):
    if not os.path.isdir(directory):
        yield "Invalid directory path.", gr.update(visible=False)
        return
    save_last_directory(directory)
    yield "Starting tagging process...", gr.update(value=0, visible=True)
    yield from run_tagger_on_folder(directory, batch_size, threshold)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Mass Image Tagger")
    gr.Markdown("Provide a directory containing images to tag them automatically.")
    
    with gr.Row():
        directory_input = gr.Textbox(label="Directory Path", placeholder="Enter the path to the folder with images", value=load_last_directory())
        batch_size_input = gr.Number(label="Batch Size", value=2, minimum=1)
        threshold_input = gr.Number(label="Threshold", value=0.3, minimum=0.0, maximum=1.0)
    
    tag_button = gr.Button("Tag Images")
    progress_bar = gr.Slider(label="Progress", minimum=0, maximum=1, value=0, interactive=False, visible=False)
    output = gr.Textbox(label="Output", interactive=False, lines=10)
    
    tag_button.click(fn=tag_images, inputs=[directory_input, batch_size_input, threshold_input], outputs=[output, progress_bar])

if __name__ == "__main__":
    demo.launch()