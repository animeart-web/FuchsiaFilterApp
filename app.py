import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Fuchsia Filter Web App")

# Allow users to upload an image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load the uploaded image using PIL
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image', use_column_width=True)
    st.write("Applying Fuchsia filters...")

    # Convert the image to a format compatible with OpenCV
    image = np.array(image)
    
    # Check if the image has an alpha channel and convert it to BGR
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    ### Version 1: Subject-only Fuchsia Filter ###
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a basic threshold to separate the subject from the background
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Create a Fuchsia overlay
    fuchsia_overlay = np.full_like(image, (255, 0, 255))

    # Apply the Fuchsia overlay only within the thresholded area
    blended_subject_image = np.where(thresholded[..., None] == 255, 
                                     cv2.addWeighted(image, 0.6, fuchsia_overlay, 0.4, 0), 
                                     image)

    # Display the "Subject-only Fuchsia Filter" result
    st.image(blended_subject_image, caption='Subject-only Fuchsia Filter', use_column_width=True)
    st.write("Subject-only Fuchsia filter applied successfully!")

    ### Version 2: Entire Image Fuchsia Filter ###
    # Apply the Fuchsia overlay to the entire image
    blended_entire_image = cv2.addWeighted(image, 0.6, fuchsia_overlay, 0.4, 0)

    # Display the "Entire Image Fuchsia Filter" result
    st.image(blended_entire_image, caption='Entire Image Fuchsia Filter', use_column_width=True)
    st.write("Entire Image Fuchsia filter applied successfully!")
