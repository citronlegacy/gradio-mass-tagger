# Additional Setup Notes

This document outlines the system dependencies that need to be installed on Ubuntu Linux for the sd-scripts project to work properly, particularly when building packages like ONNX that require C++ compilation and Python extensions.

## System Dependencies

### cmake
- **Description**: CMake is a cross-platform build system generator. It is used to control the software compilation process using simple platform and compiler independent configuration files.
- **Why needed**: Required for building ONNX, which includes C++ components. Without cmake, the build process for ONNX fails with "Could not find cmake in PATH" errors.
- **Installation**: `sudo apt install cmake`

### libprotobuf-dev
- **Description**: Protocol Buffers (protobuf) is Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data. The dev package includes headers and libraries needed for development.
- **Why needed**: ONNX uses protobuf for its model serialization format. The development headers are required when building ONNX from source to link against the protobuf libraries.
- **Installation**: `sudo apt install libprotobuf-dev`

### protobuf-compiler
- **Description**: The protobuf compiler (protoc) is used to compile .proto files into language-specific code.
- **Why needed**: ONNX's build process requires compiling protobuf definition files. Without the compiler, the build fails during the protobuf compilation step.
- **Installation**: `sudo apt install protobuf-compiler`

### python3-dev
- **Description**: Python development headers and libraries. This package contains the header files and static libraries necessary for building Python extensions using C or C++.
- **Why needed**: When building Python packages with C extensions (like ONNX's Python bindings), the compiler needs access to Python's internal headers (e.g., Python.h). Without this, builds fail with "Python.h: No such file or directory" errors.
- **Installation**: `sudo apt install python3-dev`

## Installation Command
To install all dependencies at once:
```bash
sudo apt install cmake libprotobuf-dev protobuf-compiler python3-dev
```

## Runtime Fixes

### NumPy Version Compatibility
- **Issue**: NumPy 2.x is incompatible with OpenCV and other compiled extensions, causing import errors like "ImportError: numpy.core.multiarray failed to import".
- **Solution**: Downgrade NumPy to version 1.x.
- **Command**: `pip install "numpy<2"`

### SyntaxWarnings in Python Scripts
- **Issue**: Python files contain invalid escape sequences in strings (e.g., `\(` in docstrings or help text), triggering SyntaxWarnings.
- **Solutions**:
  - For help strings in argument parsers: Escape backslashes by doubling them (e.g., change `\(` to `\\(`).
  - For docstrings: Use raw strings by prefixing with `r` (e.g., `r"""docstring"""`).
- **Files Fixed**:
  - `finetune/tag_images_by_wd14_tagger.py`: Escaped backslashes in help text for tag replacement arguments.
  - `library/custom_train_functions.py`: Made docstring a raw string to handle escape sequences properly.

## Notes
- These dependencies are typically needed when pip has to build packages from source, which happens when pre-built wheels are not available for your Python version/platform combination.
- For Python 3.12 on Ubuntu, some packages like ONNX may not have pre-built wheels, requiring source compilation.
- After installing these, you can proceed with `pip install -r requirements.txt` in your virtual environment.

## Requirements.txt Modifications

You might also need to modify `sd-scripts/requirements.txt` with the following changes:

- `onnx>=1.15.0` (to allow newer versions and avoid build issues)
- `onnxruntime==1.17.1` (specific version for compatibility)
- Ensure `torchvision` is included if not present
