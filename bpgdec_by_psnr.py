import os
import numpy as np
import cv2


def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 10 * np.log10(max_pixel**2 / mse)
    return psnr

root_dir = './bpgmaster/cifar10/original_data/'
total_psnr = 0  # Variable used to accumulate PSNR
image_count = 0  # Variable to record the number of images

for item in os.listdir(root_dir):   # Traverse root_dir
    image_count += 1
    name = root_dir + item
    save_dir = './bpgmaster/cifar10/encode/'   # Store encoding results
    save_dir1 = './bpgmaster/cifar10/ldpc_decode/'   # Store decoding results

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if not os.path.exists(save_dir1):
        os.makedirs(save_dir1)

    os.system('./bpgdec -o ' + save_dir1 + item.split('.')[0] + '.png' + ' ' + save_dir + item.split('.')[0] + '.bin')
    compressed_img  = cv2.imread(save_dir1 + item.split('.')[0] + '.png' , cv2.IMREAD_GRAYSCALE)
    original_img= cv2.imread(root_dir + item.split('.')[0] + '.png', cv2.IMREAD_GRAYSCALE)

    # Calculate PSNR
    psnr = calculate_psnr(original_img, compressed_img)
    total_psnr += psnr
    print(f"PSNR: {psnr}")

# Calculate avg PSNR
average_psnr = total_psnr / image_count
print(f"平均 PSNR: {average_psnr}")
