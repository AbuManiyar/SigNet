from google.colab import drive
drive.mount('/content/drive')

import kagglehub
path = kagglehub.dataset_download("akashgundu/signature-verification-dataset")

# Copy to drive
!cp -r {path} /content/drive/MyDrive/signature_dataset
