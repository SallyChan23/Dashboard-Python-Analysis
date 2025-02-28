import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

sns.set(style='dark')

st.title('Dashboard Penyewaan Sepeda')

all_df = pd.read_csv("https://raw.githubusercontent.com/SallyChan23/Dashboard-Python-Analysis/main/dashboard/all_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

st.sidebar.header('Filter Tanggal')

start_date = pd.to_datetime(st.sidebar.date_input('Start Date', all_df['dteday'].min()))
end_date = pd.to_datetime(st.sidebar.date_input('End Date', all_df['dteday'].max()))

filtered_df = all_df[(all_df['dteday'] >= start_date) & (all_df['dteday'] <= end_date)]

filtered_df_daily = filtered_df[['dteday', 'total_count_day', 'year_day', 'month_day', 'temp_day']].drop_duplicates(subset=['dteday']).reset_index(drop=True)

filtered_df_daily['year_day'] = filtered_df_daily['year_day'].astype(int)
filtered_df_daily['month_day'] = filtered_df_daily['month_day'].astype(int)

filtered_df_daily.rename(columns={'year_hour': 'year_day', 'month_hour': 'month_day'}, inplace=True)

monthly_df = filtered_df_daily.groupby(['year_day', 'month_day'])['total_count_day'].sum().reset_index()
monthly_df['year_day'] = monthly_df['year_day'].map({0: 2011, 1: 2012})


def calculate_metrics(df):
    total_rentals = df['total_count_day'].sum()  # Pastikan ini pakai filtered_df_daily
    average_rentals = df['total_count_day'].mean()  # Rata-rata dari dataset harian
    average_temperature = df['temp_day'].mean()  # Pastikan ambil suhu dari data yang benar
    return total_rentals, average_rentals, average_temperature

total_rentals, average_rentals, average_temperature = calculate_metrics(filtered_df_daily)  # Gunakan data yang sudah dibersihkan

st.subheader('📊 Ringkasan Data')
col1, col2, col3 = st.columns(3)
col1.metric('Total Penyewaan', f"{int(total_rentals):,}")
col2.metric('Rata-rata Penyewaan', f"{average_rentals:.2f}")
col3.metric('Rata-rata Suhu', f"{average_temperature:.2f}°C")

st.subheader('Tren Penyewaan Sepeda')

# Pertanyaan 1
fig, ax = plt.subplots(figsize=(10, 6))

# 2011
ax.plot(
    monthly_df[monthly_df['year_day'] == 2011]['month_day'],
    monthly_df[monthly_df['year_day'] == 2011]['total_count_day'],
    marker='o', color='orange', linewidth=2
)

# 2012
ax.plot(
    monthly_df[monthly_df['year_day'] == 2012]['month_day'],
    monthly_df[monthly_df['year_day'] == 2012]['total_count_day'],
    marker='o', color='blue', linewidth=2
)

ax.set_title('Tren Bulanan Penyewaan Sepeda per Tahun')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticks(range(1, 13))
ax.legend(title='Tahun', labels=['2011', '2012'])

st.pyplot(fig)

# Pertanyaan 2
st.subheader('Hubungan Suhu dan Cuaca dengan Jumlah Penyewaan Sepeda')

fig, ax = plt.subplots(figsize=(10, 6))

scatter = ax.scatter(
    filtered_df['temp_day'],
    filtered_df['total_count_day'],
    c=filtered_df['weathersit_day'],  
    cmap='coolwarm',  
    alpha=0.6,
    edgecolors='black'
)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan)", fontsize=12)

ax.set_title('Hubungan Suhu dan Cuaca dengan Jumlah Penyewaan Sepeda', fontsize=15)
ax.set_xlabel('Suhu', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=12)

st.pyplot(fig)

