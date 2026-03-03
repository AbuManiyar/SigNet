# ---------- creating all pairs possible ----------------
import os
import random
import pandas as pd
from itertools import combinations

data_dir = "/content/drive/My Drive/signature_dataset/extract"
output_csv = "/content/drive/My Drive/signature_dataset/pairs.csv"

pairs = []

# Get all genuine folders (exclude _forg)
ids = sorted([f for f in os.listdir(data_dir) if "_forg" not in f])

for id_name in ids:
    genuine_dir = os.path.join(data_dir, id_name)
    forged_dir = os.path.join(data_dir, id_name + "_forg")
    
    if not os.path.exists(forged_dir):
        continue

    # Filter strictly for jpg files
    genuine_images = sorted([
        f for f in os.listdir(genuine_dir)
        if f.lower().endswith(".jpg")
    ])

    forged_images = sorted([
        f for f in os.listdir(forged_dir)
        if f.lower().endswith(".jpg")
    ])

    # Genuine-Genuine pairs (label 0)
    for img1, img2 in combinations(genuine_images, 2):
        pairs.append([
            f"{id_name}/{img1}",
            f"{id_name}/{img2}",
            0
        ])

    # Genuine-Forged pairs (label 1)
    for g_img in genuine_images:
        for f_img in forged_images:
            pairs.append([
                f"{id_name}/{g_img}",
                f"{id_name}_forg/{f_img}",
                1
            ])

# Shuffle once at the end
random.shuffle(pairs)

# Save CSV
df = pd.DataFrame(pairs, columns=["image1", "image2", "label"])
df.to_csv(output_csv, index=False)

print("pairs.csv created successfully!")
print("Total pairs:", len(df))
print()
print()




# -------- creating test, train and validation ------------
from sklearn.model_selection import train_test_split

# 70% train, 30% temp
train_df, temp_df = train_test_split(
    df, test_size=0.3, random_state=42, stratify=df["label"]
)

# Split temp into val (15%) and test (15%)
val_df, test_df = train_test_split(
    temp_df, test_size=0.5, random_state=42, stratify=temp_df["label"]
)

train_df.to_csv("/content/drive/My Drive/signature_dataset/train.csv", index=False)
val_df.to_csv("/content/drive/My Drive/signature_dataset/val.csv", index=False)
test_df.to_csv("/content/drive/My Drive/signature_dataset/test.csv", index=False)

print("Train:", len(train_df))
print("Val:", len(val_df))
print("Test:", len(test_df))
