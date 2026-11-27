import math

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


def image_to_tensor(image_path, device):
    with Image.open(image_path) as image:
        image = torch.tensor(
            np.array(image.convert("RGB")),
            dtype=torch.float32,
            device=device
        )
    return image

def convert_to_grayscale(image_tensor):
    R = image_tensor[:, :, 0]
    G = image_tensor[:, :, 1]
    B = image_tensor[:, :, 2]

    return (0.299*R + 0.587*G + 0.114*B) / 255


def compute_gaussian_kernel(sigma, device):
    r = math.ceil(3 * sigma) # kernel radius

    coords = torch.arange(-r, r + 1, dtype=torch.float32, device=device)
    y, x = torch.meshgrid(coords, coords, indexing="ij")

    d2 = x**2 + y**2
    kernel = torch.exp(-d2 / (2 * sigma**2))

    return kernel / kernel.sum()
    


def apply_gaussian_blur(image, kernel):
    p = kernel.shape[0] // 2 # padding

    image = image[None, None, :, :]
    kernel = kernel[None, None, :, :]

    image = F.pad(image, (p, p, p, p), mode="reflect")

    return F.conv2d(image, kernel)[0, 0]


def build_gaussian_pyramid(image, num_octaves, num_scales, device, sigma=1.6, sigma_input=0.5):
    pyramid = []

    k = math.pow(2, 1 / num_scales) # scale multipler

    initial_sigma = math.sqrt(sigma**2 - sigma_input**2)
    kernel = compute_gaussian_kernel(initial_sigma, device)
    base = apply_gaussian_blur(image, kernel)

    for _ in range(num_octaves):
        octave = [base]

        for s in range(1, num_scales + 3):
            current_sigma = sigma * k**s
            previous_sigma = sigma * k**(s - 1)

            incremental_sigma = math.sqrt(
                current_sigma**2 - previous_sigma**2
            )

            kernel = compute_gaussian_kernel(incremental_sigma, device)
            blurred = apply_gaussian_blur(octave[-1], kernel)

            octave.append(blurred)

        pyramid.append(octave)
        base = octave[num_scales][::2, ::2]

    return pyramid
    

def build_dog_pyramid(gaussian_pyramid):
    """ Construct Difference of Gaussians Pyramid"""
    pass

    



    
    

