import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Mengimpor dataset (contoh, sesuaikan dengan data Anda)
all_df = pd.read_csv('dashboard/all_data.csv')

# Membuat helper function
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule ='D', on = 'dteday_y').agg({
        'dteday_x' : 'nunique',
        'cnt_y' : 'sum'
    })

    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns= {
        'dteday_x' : 'order_count',
        'cnt_y' : 'qty'
    }, inplace = True)

    return daily_orders_df

def create_avg_season_weather_df(df):
    # Mengelompokkan berdasarkan 'season_x' dan 'weathersit_x' dan menghitung rata-rata dari 'cnt_x'
    avg_season_weather_df = df.groupby(['season_x', 'weathersit_x'])['cnt_x'].mean().reset_index()
    
    # Mengurutkan hasil berdasarkan 'cnt_x' secara menurun
    avg_season_weather_df = avg_season_weather_df.sort_values(by='cnt_x', ascending=False)
    
    return avg_season_weather_df


def create_avg_day_df(df):
    avg_day_df = df.groupby('weekday_x')['cnt_x'].mean().sort_values(ascending = False).reset_index()
    return avg_day_df

def create_avg_hour_df(df):
    avg_hour_df = df.groupby('hr')['cnt_y'].mean().sort_values(ascending = False).reset_index()
    return avg_hour_df


datetime_columns = ['dteday_x', 'dteday_y']
all_df.sort_values(by = 'dteday_x', inplace = True)
all_df.reset_index(inplace = True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# ================ Filter ==================
min_date = all_df['dteday_x'].min()
max_date = all_df['dteday_x'].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label = "Rentang Waktu",
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

main_df = all_df[(all_df['dteday_x'] >= str(start_date)) &
                (all_df['dteday_x'] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
avg_season_weather_df = create_avg_season_weather_df(main_df)
avg_day_df = create_avg_day_df(main_df)
avg_hour_df = create_avg_hour_df(main_df)

# ================ Streamlit Sidebar =================
st.sidebar.header("Nisrina Alifa Adzahra")
st.sidebar.subheader("nisrinalifa@gmail.com")
st.sidebar.text("Dataset = Bike Sharing Dataset")

st.header('Analisis Dataset Bike Sharing Dataset')

st.divider()

col1, col2 = st.columns(2)

with col1:
    total_order_id = daily_orders_df.order_count.sum()
    st.metric('Total Day', value = total_order_id)

with col2:
    total_qty = daily_orders_df.qty.sum()
    st.metric('Total Order', value = total_qty)

st.divider()

#=================================================================================================
# Visualisasi Penyewaan sepeda berdasarkan Musim dan Cuaca
st.text('Pertanyaan 1 :')
st.subheader("Penyewaan Sepeda Terbanyak Berdasarkan Musim dan Cuaca")

col1, col2, col3 = st.columns(3)

with col1:
    max_season = int(avg_season_weather_df.loc[avg_season_weather_df['cnt_x'].idxmax(), 'season_x'])
    st.metric('Musim', value=max_season)

with col2:
    max_weather = int(avg_season_weather_df.loc[avg_season_weather_df['cnt_x'].idxmax(), 'weathersit_x'])
    st.metric('Cuaca', value=max_weather)

with col3:
    max_count = int(avg_season_weather_df.loc[avg_season_weather_df['cnt_x'].idxmax(), 'cnt_x'])
    st.metric('Jumlah Rata-Rata', value=f'{max_count:.2f}')

fig, ax = plt.subplots(figsize = (16, 8))
ax.plot(
    avg_season_weather_df['season_x'],
    avg_season_weather_df['weathersit_x'],
    marker = 'o',
    linewidth = 2,
    color = '#90CAF9'
)

ax.tick_params(axis = 'y', labelsize = 20)
ax.tick_params(axis = 'x', labelsize = 15)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season_x', y='cnt_x', data=avg_season_weather_df, hue='weathersit_x', ax=ax)
ax.set_title('Penyewaan Sepeda Berdasarkan Musim dan Cuaca', fontsize=15)
ax.legend(title='Kondisi Cuaca')
ax.set_xlabel('Musim', fontsize=15)
ax.set_ylabel('Jumlah Penyewaan', fontsize=15)
ax.grid(True, axis='y', linestyle='--', alpha=0.3, color = '#000000')

st.pyplot(fig)

col4, col5 = st.columns(2)

with col4:
    with st.expander('Keterangan Musim'):
        st.text(
            '''
            1 = Musim Semi
            2 = Musim Panas
            3 = Musim Gugur
            4 = Musim Dingin
            '''
        )

with col5:
    with st.expander('Keterangan Cuaca'):
        st.text(
            '''
            1 = Clear, Few clouds, Partly cloudy
            2 = Mist + Cloudy, Mist + Broken clouds
            3 = Light Snow, Light Rain + Thunderstorm
            4 = Heavy Rain + Ice Pallets + Snow + Mist, Fog
            '''
        )

st.divider()

#=======================================================================================
# Visualisasi Tren Penyewaan Sepeda dalam satu Minggu (berdasarkan hari)
st.text('Pertanyaan 2 :')
st.subheader("Tren Penyewaan Sepeda dalam Satu Minggu")

col1, col2, col3 = st.columns(3)

with col1:
    max_day = int(avg_day_df.loc[avg_day_df['cnt_x'].idxmax(), 'weekday_x'])
    st.metric('Hari', value=max_day)

with col2:
    max_count = int(avg_day_df.loc[avg_day_df['cnt_x'].idxmax(), 'cnt_x'])
    st.metric('Jumlah Rata-Rata', value=f'{max_count:.2f}')

with col3:
    with st.expander('Keterangan Hari'):
        st.text(
        '''
        0 = Senin, 
        1 = Selasa, 
        2 = Rabu, 
        3 = Kamis, 
        4 = Jumat, 
        5 = Sabtu, 
        6 = Minggu
        '''
        )

fig, ax = plt.subplots(figsize = (16, 8))
ax.plot(
    avg_season_weather_df['season_x'],
    avg_season_weather_df['weathersit_x'],
    marker = 'o',
    linewidth = 2,
    color = '#90CAF9'
)

ax.tick_params(axis = 'y', labelsize = 20)
ax.tick_params(axis = 'x', labelsize = 15)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=avg_day_df['weekday_x'], y=avg_day_df['cnt_x'], marker='o', ax=ax)
ax.set_title('Tren Penyewaan Sepeda dalam satu Minggu', fontsize=15)
ax.set_xlabel('Hari', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
st.pyplot(fig)

st.divider()

#===============================================================================
# Visualisasi Tren Penyewaan Sepeda per Jam
st.text('Pertanyaan 3 :')
st.subheader("Tren Jam Penyewaan Sepeda")

col1, col2 = st.columns(2)

with col1:
    max_hour = int(avg_hour_df.loc[avg_hour_df['cnt_y'].idxmax(), 'hr'])
    st.metric('Jam', value=max_hour)

with col2:
    max_count = int(avg_hour_df.loc[avg_hour_df['cnt_y'].idxmax(), 'cnt_y'])
    st.metric('Jumlah Rata-Rata', value=f'{max_count:.2f}')


fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=all_df['hr'], y=all_df['cnt_y'], marker='o', ax=ax)
ax.set_title('Tren Jam Penyewaan Sepeda', fontsize=15)
ax.set_xlabel('Jam', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax.set_xticks(range(0, 24))
ax.grid(True, axis='x', linestyle='--', alpha=0.3, color = '#000000')
ax.grid(True, axis='y', linestyle='--', alpha=0.3, color = '#000000')

st.pyplot(fig)
