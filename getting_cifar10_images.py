# !wget -P dataset/CIFAR10/test https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
# !tar -xvf dataset/CIFAR10/test/cifar-10-python.tar.gz
import numpy as np
import imageio
import os

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

data_dir = "./cifar-10-batches-py"  # Adjust if needed
output_dir = "./bpgmaster/cifar10/original_data/"  # Adjust if needed

os.makedirs(output_dir, exist_ok=True)  # Create output directory 

data_file = os.path.join(data_dir, f"test_batch")
data = unpickle(data_file)  # Load using unpickle function
labels = unpickle(os.path.join(data_dir, "batches.meta"))
for j in range(len(data)):  # Iterate over images
    img = data[b'data'][j]
    label = data[b'filenames'][j]
    img = img.reshape((3, 32, 32)).transpose((1, 2, 0))  # Reshape and transpose
    img = (img * 255).astype(np.uint8)  # Rescale to uint8
    imageio.imsave(os.path.join(output_dir, label.decode("utf-8")), img)
print("Successfully extract the images from the test path!")
