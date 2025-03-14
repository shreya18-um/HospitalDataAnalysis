import pandas as pd

# Load the dataset
dataset_path = "C:/Users/MacBook Pro/Desktop/HospitalDataAnalysis/dataset/HospInfo.csv"
df = pd.read_csv(dataset_path)

# Keep only necessary columns
columns_to_keep = ["Hospital Name", "City", "State", "Hospital overall rating", "Emergency Services"]
df = df[columns_to_keep]

# Save the reduced dataset
reduced_path = "C:/Users/MacBook Pro/Desktop/HospitalDataAnalysis/dataset/HospInfo_reduced.csv"
df.to_csv(reduced_path, index=False)

print("✅ Reduced dataset saved as HospInfo_reduced.csv")
