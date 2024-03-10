import os
import pyldpc
import numpy as np

import time
root_dir = './bpgmaster/cifar10/original_data/'
for item in os.listdir(root_dir):   # 遍历root_dir
        name = root_dir + item
        # Store the encoding results and replace it with your own directory. It is recommended to use the complete route.
        save_dir = './bpgmaster/cifar10/encode/'   
        #save_dir1 = './bpgmaster/cifar10/decode/'   # Store decoding results

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        #if not os.path.exists(save_dir1):
        #    os.makedirs(save_dir1)

        os.system('./bpgenc -m 1 -b 8 -q 35 ' + name + ' -o ' + save_dir + item.split('.')[0] + '.bin')
        print(name)
        with open(save_dir+item.split('.')[0]+'.bin', 'rb') as f:
            data = np.unpackbits(np.fromfile(f, dtype=np.uint8))
        print(data.shape)
        n = 50
        d_v = 3
        d_c = 5
        snr = 10
        encode_start_time = time.time()
        seed = np.random.RandomState(42)
        H, G = pyldpc.make_ldpc(n, d_v, d_c, seed=seed, systematic=True, sparse=True)
        print(H)
        print(G)
        # Divide data into chunks and divide by size k

        # n,k = G.shape
        # n_blocks = len(data) // k
        # data_blocks = np.reshape(data[:n_blocks * k], (-1, k))
        # print(data_blocks.shape)

        n, k = G.shape
        n_blocks = len(data) // k
        remainder = len(data) % k

        # If there is remaining data, fill it into a new data block of length k
        if remainder > 0:
            padding_len = k - remainder
            last_block = np.pad(data[n_blocks * k:], (0, padding_len), mode='constant')
            data_blocks = np.vstack((data[:n_blocks * k].reshape(-1, k), last_block))
        else:
            data_blocks = data[:n_blocks * k].reshape(-1, k)
            padding_len = 0

        print(data_blocks.shape)

        # LDPC encoding for each block
        # encoded_data_blocks = np.empty((n_blocks, n), dtype=np.uint8)
        # decoded_data_blocks = np.empty((n_blocks, k), dtype=np.uint8)
        # print(data_blocks[1])
        encoded_data_blocks = pyldpc.encode(G, data_blocks.T, snr, seed=seed)
        # Record encoding end time
        encode_end_time = time.time()

        # Calculate encoding time
        encoding_time = encode_end_time - encode_start_time
        print(f"Encoding time: {encoding_time} secs")

        decode_start_time = time.time()
        # print(encoded_data_blocks)
        y = pyldpc.decode(H, encoded_data_blocks, snr, maxiter=1000)

        # for i in range (data_blocks.shape[0]):
        #    decoded_data_blocks = pyldpc.get_message(G, y.T[i])
        #    print(decoded_data_blocks)
        # Save encoded data as binary file
        decoded_data_blocks_all = np.concatenate([pyldpc.get_message(G, y.T[i]) for i in range(data_blocks.shape[0])])

        # Record decoding end time
        decode_end_time = time.time()

        # Calculate decoding time
        decoding_time = decode_end_time - decode_start_time
        print(f"Deconding time: {decoding_time} secs")
        # Pack the 01 bitstream into uint8 type
        print(decoded_data_blocks_all)

        if padding_len > 0:
            decoded_data_blocks_all = decoded_data_blocks_all[:-padding_len]

        decoded_data_blocks_all = np.packbits(decoded_data_blocks_all)

        # Write decoded data to binary file

        with open(save_dir+item.split('.')[0]+'decoded_data.bin', 'wb') as f:
            decoded_data_blocks_all.tofile(f)
