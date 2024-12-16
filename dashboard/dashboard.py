import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Mengimpor dataset (contoh, sesuaikan dengan data Anda)
day_df = pd.read_csv('day_data.csv')
hour_df = pd.read_csv('hour_data.csv')


day_df = pd.DataFrame(day_df)
hour_df = pd.DataFrame(hour_df)

# Streamlit Sidebar
st.sidebar.header("Nisrina Alifa Adzahra")
st.sidebar.subheader("nisrinalifa@gmail.com")
st.sidebar.text("Dataset = Bike Sharing Dataset")

st.header('Analisis Dataset Bike Sharing Dataset')

# Visualisasi Penyewaan sepeda berdasarkan Musim dan Cuaca
st.text('Pertanyaan 1 :')
st.subheader("Penyewaan Sepeda Berdasarkan Musim dan Cuaca")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='cnt', data=day_df, hue='weathersit', ax=ax)
ax.set_title('Penyewaan Sepeda Berdasarkan Musim dan Cuaca', fontsize=15)
ax.set_xlabel('Musim', fontsize=15)
ax.set_ylabel('Jumlah Penyewaan', fontsize=15)
ax.grid(True, axis='y', linestyle='--', alpha=0.5)

st.pyplot(fig)

# Visualisasi Tren Penyewaan Sepeda dalam satu Minggu (berdasarkan hari)
st.text('Pertanyaan 2 :')
st.subheader("Tren Penyewaan Sepeda dalam Satu Minggu")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=day_df.weekday, y=day_df.cnt, marker='o', ax=ax)
ax.set_title('Tren Penyewaan Sepeda dalam Satu Minggu', fontsize=15)
ax.set_xlabel('Hari', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
st.pyplot(fig)

# Visualisasi Tren Penyewaan Sepeda per Jam
st.text('Pertanyaan 3 :')
st.subheader("Tren Penyewaan Sepeda per Jam")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=hour_df['hr'], y=hour_df['cnt'], marker='o', ax=ax)
ax.set_title('Tren Penyewaan Sepeda per Jam', fontsize=15)
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

st.pyplot(fig)
