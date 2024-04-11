import argparse
import numpy as np
import pydicom
from tkinter import Tk, Label, Scale, HORIZONTAL
from PIL import Image, ImageTk

parser = argparse.ArgumentParser(description="DICOM Window Level Adjustment Tool")
parser.add_argument("-f", "--file", type=str, help="Path to the DICOM file.")
args = parser.parse_args()

dicom_data = pydicom.dcmread(args.file)
pixel_array: np.ndarray = dicom_data.pixel_array


def apply_window_level(
    pixel_array: np.ndarray, window_center: int, window_width: int
) -> np.ndarray:
    """
    Apply window leveling to the input image.

    Parameters:
    - pixel_array: numpy.ndarray
        The original image array.
    - window_center: int
        The center of the window for the level adjustment.
    - window_width: int
        The width of the window for the level adjustment.

    Returns:
    - The window-leveled image array.
    """
    img_min: int = window_center - window_width // 2
    img_max: int = window_center + window_width // 2
    windowed_img: np.ndarray = (
        ((pixel_array - img_min) / (img_max - img_min) * 255)
        .clip(0, 255)
        .astype(np.uint8)
    )
    return windowed_img


root: Tk = Tk()
root.title("DICOM Window Level Adjustment")

init_window_center: int = (
    int(dicom_data.WindowCenter[0])
    if isinstance(dicom_data.WindowCenter, pydicom.multival.MultiValue)
    else int(dicom_data.WindowCenter)
)
init_window_width: int = (
    int(dicom_data.WindowWidth[0])
    if isinstance(dicom_data.WindowWidth, pydicom.multival.MultiValue)
    else int(dicom_data.WindowWidth)
)


def update_image(window_center: int, window_width: int) -> None:
    """
    Update the displayed image based on the given window center and width.
    """
    adjusted_image: np.ndarray = apply_window_level(
        pixel_array, window_center, window_width
    )
    img = Image.fromarray(adjusted_image)
    imgtk = ImageTk.PhotoImage(image=img)
    lbl_img.configure(image=imgtk)
    lbl_img.image = imgtk


def on_slide(_: str) -> None:
    """
    Handle the event when the slider is moved. Fetches the current values from the sliders and updates the image.
    """
    window_center: int = int(slider_center.get())
    window_width: int = int(slider_width.get())
    update_image(window_center, window_width)


slider_center: Scale = Scale(
    root,
    from_=np.min(pixel_array),
    to=np.max(pixel_array),
    orient=HORIZONTAL,
    label="Window Center",
    length=400,
    command=on_slide,
)
slider_center.set(init_window_center)
slider_center.pack()

slider_width: Scale = Scale(
    root,
    from_=1,
    to=np.max(pixel_array) - np.min(pixel_array),
    orient=HORIZONTAL,
    label="Window Width",
    length=400,
    command=on_slide,
)
slider_width.set(init_window_width)
slider_width.pack()

lbl_img = Label(root)
lbl_img.pack()

update_image(init_window_center, init_window_width)
root.mainloop()
