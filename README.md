# Mass Tagger App

This is a Gradio-based web application for mass tagging images using the WD14 tagger model. It allows you to tag images in a single folder or recursively through multiple subfolders, making it efficient for tagging large datasets of images.

The app serves as a user-friendly wrapper around the [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts) repository, specifically utilizing its WD14 tagger functionality for automated image tagging.

## Features

- **Batch Tagging**: Tag all images in a selected folder and its subfolders.
- **Recursive Processing**: Automatically processes subfolders within the chosen directory.
- **Gradio Interface**: Easy-to-use web interface for selecting folders and initiating tagging.
- **WD14 Tagger Integration**: Leverages the powerful WD14 model for accurate tag generation.

## Setup

1. Ensure you have Python installed (version 3.8 or higher recommended).
2. Clone or download this repository.
3. Run the setup script to install dependencies and set up the environment:

   ```bash
   ./setup.sh
   ```

   This script will create a virtual environment, install the required packages from `requirements.txt`, and prepare the necessary models.

## Launching the App

After setup, activate the virtual environment and run the Gradio app:

```bash
source venv/bin/activate  # On Windows, use venv\Scripts\activate
python gradio_mass_tagger.py
```

The app will start a local web server. Open the provided URL in your browser to access the interface.

## Usage

1. In the Gradio interface, select the folder containing your images.
2. Choose whether to process subfolders recursively.
3. Click "Start Tagging" to begin the process.
4. The app will generate tags for each image and save them alongside the images or in a specified output format.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
- WD14 tagger model (downloaded during setup)

## Contributing

This app is built on top of kohya-ss/sd-scripts. For issues related to the underlying tagging functionality, please refer to the [original repository](https://github.com/kohya-ss/sd-scripts).