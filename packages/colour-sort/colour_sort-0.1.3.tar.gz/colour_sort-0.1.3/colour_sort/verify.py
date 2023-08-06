import sys

import numpy as np
from PIL import Image

def verify_image(img: Image.Image) -> bool:
    check = np.zeros(256*256*256, dtype=np.bool)
    img_a = np.array(img).astype(np.uint32) # Oh god they all have to be uint32 because 255 << 16 = 16711680
    if np.product(img_a.shape[:2]) != 256*256*256:
        raise Exception('Image is not the correct shape')

    flattened = np.reshape(img_a, (256*256*256, 3))

    np.left_shift(flattened[:,0], 16, out=flattened[:,0])
    np.left_shift(flattened[:,1], 8, out=flattened[:,1])

    indexed = flattened[:,0] | flattened[:,1] | flattened[:,2]
    check[indexed] = True

    return np.all(check)

if __name__ == '__main__':
    img = Image.open(sys.argv[1])
    print(verify_image(img))
