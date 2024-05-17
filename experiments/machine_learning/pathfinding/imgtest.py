from PIL import Image
import numpy as np

pixels = [[(255, 0, 0, 255), (255, 0, 0, 255), (255, 0, 0, 255)]]

export_image = Image.fromarray(np.array(pixels).astype(np.uint8))

export_image.save('test.png')
