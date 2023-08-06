# -*- coding=utf-8 -*-
"""Preprocessing functions for ssd-mobilenet."""
from typing import Tuple
import numpy as np
import cv2
from PIL import Image


def image_to_tensor(image: Image) -> np.ndarray:
    """
    Realise preprocess for an input pillow image and convert it to numpy array.

    Parameters
    ----------
    image
        An input image to be processed.

    Returns
    -------
    tensor
        Preprocessed numpy array.
    """
    image = image.convert('RGB')
    tensor = np.asarray(image, dtype=np.float32)
    tensor = cv2.resize(tensor, (300, 300))
    assert tensor.shape == (300, 300, 3)
    return tensor


def preprocess_tensor(preprocess_runner, image: Image) -> Tuple[np.ndarray, np.ndarray]:
    """Preprocess image for the network."""
    image = image.convert('RGB')
    tensor = np.asarray(image)

    tensor = np.expand_dims(tensor, axis=0)
    prepr_tensor = preprocess_runner(tensor)
    return prepr_tensor, tensor
