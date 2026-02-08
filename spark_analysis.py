import pandas as pd

file_path = "data/raw/petani_perempuan_jabar.csv"
df = pd.read_csv(file_path)

print(df.head())
print(df.info())

selected_columns = [
    "nama_provinsi",
    "bps_nama_kabupaten_kota",
    "bps_nama_kecamatan",
    "bps_nama_desa_kelurahan",
    "jumlah_petani",
    "tahun"
]

df_selected = df[selected_columns]

print(df_selected.isnull().sum())

df_selected["jumlah_petani"] = pd.to_numeric(
    df_selected["jumlah_petani"],
    errors="coerce"
)

df_cleaned = df_selected.dropna()

df_cleaned.to_csv(
    "data/processed/cleaned_data.csv",
    index=False
)

print("Data preprocessing selesai")

df_grouped = df_cleaned.groupby(
    "bps_nama_kabupaten_kota"
).agg(
    total_petani_perempuan=("jumlah_petani", "sum"),
    jumlah_desa=("bps_nama_desa_kelurahan", "count"),
    rata_rata_petani=("jumlah_petani", "mean")
).reset_index()

print("\n=== HASIL AGREGASI PER KABUPATEN ===")
print(df_grouped.head())

output_agg_path = "data/processed/aggregated_per_kabupaten.csv"
df_grouped.to_csv(output_agg_path, index=False)

print("\n=== DATA AGREGASI DISIMPAN ===")
print(f"Lokasi file: {output_agg_path}")

print("\n=== ANALISIS DESKRIPTIF ===")

total_petani_jabar = df_grouped["total_petani_perempuan"].sum()
print(f"Total petani perempuan di Jawa Barat: {total_petani_jabar}")

kabupaten_tertinggi = df_grouped.loc[
    df_grouped["total_petani_perempuan"].idxmax()
]
print("\nKabupaten dengan petani perempuan terbanyak:")
print(kabupaten_tertinggi)

kabupaten_terendah = df_grouped.loc[
    df_grouped["total_petani_perempuan"].idxmin()
]
print("\nKabupaten dengan petani perempuan paling sedikit:")
print(kabupaten_terendah)

print("\nStatistik ringkas total petani perempuan per kabupaten:")
print(df_grouped["total_petani_perempuan"].describe())