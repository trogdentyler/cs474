import torch
from PIL import Image
import numpy as np
from RealESRGAN import RealESRGAN

# this ensures that the current MacOS version is at least 12.3+
# print(torch.backends.mps.is_available())# this ensures that the current current PyTorch installation was built with MPS activated.
# print(torch.backends.mps.is_built())

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')

model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4.pth', download=True)

path_to_image = 'imgs/link.png'
image = Image.open(path_to_image).convert('RGB')

sr_image = model.predict(image)

sr_image.save('imgs/link_sr.png')