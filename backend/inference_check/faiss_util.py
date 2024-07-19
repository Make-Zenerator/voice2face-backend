import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import faiss
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import faiss
import tempfile
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from python_speech_features import mfcc

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from skimage.metrics import structural_similarity as ssim
import lpips
import pytorch_fid_wrapper as pfw

def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    image = image.resize((256, 256), Image.ANTIALIAS)
    image = np.array(image).flatten()
    return image

def process_batch(image_paths):
    embeddings = []
    for image_path in tqdm(image_paths):
        try:
            embeddings.append(get_image_embedding(image_path))
        except:
            pass
    return np.array(embeddings)

def save_embeddings(embeddings, filename):
    np.save(filename, embeddings)

def load_embeddings(filename):
    return np.load(filename)

def save_index(csv_path,save_path):
    train_csv = pd.read_csv(csv_path)['mfcc_image_path']

    for image_path in tqdm(train_csv):
        try:
            embeddings.append(get_image_embedding(image_path))
        except:
            pass
    embeddings = np.array(embeddings)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, save_path)

def search_audio_sim(index, audio_path):
    rate, signal = wav.read(audio_path)
    n_mfcc = 13
    mfcc_features = mfcc(signal, rate, numcep=n_mfcc)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        plt.figure(figsize=(10, 4))
        plt.imshow(mfcc_features.T, aspect='auto', cmap='viridis')
        plt.axis('off')
        plt.savefig(temp_file.name, bbox_inches='tight', pad_inches=0)
        plt.close()

        temp_file_path = temp_file.name
        new_embedding = get_image_embedding(temp_file_path)
    distances, indices = index.search(np.array([new_embedding]), 1)
    mfcc_image_path = pd.read_csv('/home/hojun/Documents/code/mz/voice2face-backend/backend/inference_check/sample_OLKAVS.csv')['mfcc_image_path'].iloc[indices[0][0]]
    face_image_path = pd.read_csv('/home/hojun/Documents/code/mz/voice2face-backend/backend/inference_check/sample_OLKAVS.csv')['face_image_path'].iloc[indices[0][0]]
    return  distances, indices, mfcc_image_path,face_image_path


def read_and_process_image(image_path, target_size=(256, 256)):
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, target_size)
    return image

def calculate_psnr(img1, img2):
    img1 = torch.tensor(img1).float() / 255.0  # Normalize to [0, 1]
    img2 = torch.tensor(img2).float() / 255.0  # Normalize to [0, 1]
    loss_l2 = F.mse_loss(img1, img2, reduction="mean")
    PSNR_val = 20 * torch.log10(1.0 / torch.sqrt(loss_l2))
    return PSNR_val.item()

def calculate_ssim(img1, img2):
    ssim_value = ssim(img1, img2, channel_axis=2, full=True)
    return ssim_value[0]

def mssim(img1, img2, scales=5):
    ssim_value = ssim(img1, img2, channel_axis=2, full=True,win_size=11)
    return ssim_value[0]

def calculate_lpips(img1, img2):
    loss_fn = lpips.LPIPS(net='alex')
    img1 = torch.tensor(img1).permute(2, 0, 1).float() / 255.0  # Normalize to [0, 1]
    img2 = torch.tensor(img2).permute(2, 0, 1).float() / 255.0  # Normalize to [0, 1]
    img1 = img1.unsqueeze(0)
    img2 = img2.unsqueeze(0)
    lpips_score = loss_fn(img1, img2)
    return lpips_score.item()

def calculate_fid(img1, img2):
    img1 = torch.tensor(img1).permute(2, 0, 1).float().unsqueeze(0) / 255.0  # Normalize to [0, 1]
    img2 = torch.tensor(img2).permute(2, 0, 1).float().unsqueeze(0) / 255.0  # Normalize to [0, 1]
    fid_val = pfw.fid(img2, img1, batch_size=img2.shape[0])
    return fid_val.item()

def calculate_metric(img1, img2):
    return (
        calculate_psnr(img1, img2),
        calculate_ssim(img1, img2),
        mssim(img1, img2),
        calculate_lpips(img1, img2),
        calculate_fid(img1, img2)
    )
def calcualte_sim_image(index_path,audio_path,inference_image_path):
    index = faiss.read_index(index_path)
    searched_image = search_audio_sim(index=index,audio_path=audio_path)[3]
    metrics = calculate_metric(read_and_process_image(inference_image_path), read_and_process_image(searched_image))
    return metrics
