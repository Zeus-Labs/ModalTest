import argparse
import json
import os
import tempfile

import cv2
import numpy as np
import torch
from utils import (copy_file, copy_files, download_file, unzip_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--destination_tensor_file_path', type=str, help="file path, tensor gets saved")

    opt = parser.parse_args()

    destination_tensor_file_path = opt.destination_tensor_file_path
    if destination_tensor_file_path is None or destination_tensor_file_path == "":
        raise Exception("Missing destination tensor file path.")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Download images data from gDrive
        may_url = "https://drive.google.com/uc?export=download&id=18Q2H612CAReFxBd9kxr-i1dD8U1AUfsV"
        data_folder = os.path.join(temp_dir, "data_original")
        data_zip_file_name = "May.zip"
        data_file_name = "May"

        data_unzip_path = download_and_unzip(may_url, data_folder, data_zip_file_name, data_file_name)

        # Copy only test data to separate folder
        source_dir = data_unzip_path
        test_data_dir = os.path.join(temp_dir, "data/May")
        os.makedirs(test_data_dir, exist_ok=True)

        # Copy bs.npy, bc.jpg, transforms_val.json
        copy_files(source_dir, test_data_dir, ["bs.npy", "bc.jpg", "transforms_val.json"])

        # Copy torso images and lms based on transforms_val.json
        test_torso_dir = os.path.join(test_data_dir, "torso_imgs")
        test_lms_dir = os.path.join(test_data_dir, "ori_imgs")
        os.makedirs(test_torso_dir, exist_ok=True)
        os.makedirs(test_lms_dir, exist_ok=True)
        with open(os.path.join(test_data_dir, 'transforms_val.json'), 'r') as f:
            transform = json.load(f)
        frames = transform["frames"]

        torso_imgs = []
        for frame in frames:
            source_torso_path = os.path.join(source_dir, 'torso_imgs', str(frame['img_id']) + '.png')
            source_lms_path = os.path.join(source_dir, 'ori_imgs', str(frame['img_id']) + '.lms')
            copy_file(source_torso_path, test_torso_dir)
            copy_file(source_lms_path, test_lms_dir)

            # save preprocessed torso images as tensors
            torso_img = cv2.imread(source_torso_path, cv2.IMREAD_UNCHANGED)  # [H, W, 4]
            torso_img = cv2.cvtColor(torso_img, cv2.COLOR_BGRA2RGBA)
            torso_img = torso_img.astype(np.float32) / 255
            torso_imgs.append(torso_img)

        torso_imgs_torch = torch.from_numpy(np.stack(torso_imgs, axis=0))
        torso_imgs_torch = torso_imgs_torch.to(torch.half)
        torch.save(torso_imgs_torch, destination_tensor_file_path, _use_new_zipfile_serialization=True)


def download_and_unzip(may_url, data_folder, data_zip_file_name, data_file_name):
    os.makedirs(data_folder, exist_ok=True)
    data_path = download_file(may_url, data_folder, data_zip_file_name)
    data_unzip_path = unzip_file(data_path, data_folder, data_file_name)
    return data_unzip_path


if __name__ == "__main__":
    main()
