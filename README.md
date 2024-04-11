# DICOM Window Level Adjustment Tool (DWLAT)

This tool provides a graphical user interface (GUI) for adjusting the window level of DICOM images. With a simple slider control, users can fine-tune the visualization of medical images to enhance the clarity and contrast.

## Prerequisites

Before you begin, ensure that you have met the following requirements:

- Python 3.11 installed on your system.
- Poetry dependency management tool installed.

## Installation

To set up the project environment and install all the required dependencies, follow these steps:

1. Clone the repository or download the source code onto your local machine.

```bash
git clone https://github.com/futabato/DWLAT.git
cd DWLAT
```

2. Use poetry to install the project dependencies.

```bash
poetry install
```

## Usage

Once you have installed the dependencies, you can run the tool with the command:

```bash
python main.py -f path_to_your_dicom_file.dcm
```

Replace `path_to_your_dicom_file.dcm` with the actual path to the DICOM file you want to adjust.

The GUI will open with two sliders allowing you to change the Window Center and Window Width dynamically. Adjusting these sliders updates the displayed image in real-time.
