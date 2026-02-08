import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "data/processed/aggregated_per_kabupaten.csv"
df = pd.read_csv(file_path)

sns.set(style="whitegrid")

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df,
    x="bps_nama_kabupaten_kota",
    y="total_petani_perempuan"
)
plt.xticks(rotation=90)
plt.title("Total Petani Perempuan per Kabupaten di Jawa Barat")
plt.xlabel("Kabupaten/Kota")
plt.ylabel("Total Petani Perempuan")
plt.tight_layout()
plt.show()

top10 = df.sort_values(
    by="total_petani_perempuan",
    ascending=False
).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top10,
    x="total_petani_perempuan",
    y="bps_nama_kabupaten_kota"
)
plt.title("Top 10 Kabupaten dengan Petani Perempuan Terbanyak")
plt.xlabel("Total Petani Perempuan")
plt.ylabel("Kabupaten/Kota")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["total_petani_perempuan"], bins=10, kde=True)
plt.title("Distribusi Total Petani Perempuan per Kabupaten")
plt.xlabel("Total Petani Perempuan")
plt.ylabel("Jumlah Kabupaten")
plt.tight_layout()
plt.show()