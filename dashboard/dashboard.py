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

def calculate_metrics(df):
    total_rentals = df['total_count_day'].sum()
    average_rentals = df['total_count_day'].mean()
    average_temperature = df['temp_day'].mean()
    return total_rentals, average_rentals, average_temperature

total_rentals, average_rentals, average_temperature = calculate_metrics(filtered_df)

st.title('🚲 Statistik Penyewaan Sepeda')
st.subheader('📊 Ringkasan Data')
col1, col2, col3 = st.columns(3)
col1.metric('Total Penyewaan', f"{int(total_rentals):,}")
col2.metric('Rata-rata Penyewaan', f"{average_rentals:.2f}")
col3.metric('Rata-rata Suhu', f"{average_temperature:.2f}°C")

col1, col2 = st.columns(2)
col1.metric('Jumlah baris di Dashboard:', filtered_df.groupby(['year_day', 'month_day']).size().shape[0])
col2.metric('Total Penyewaan di Dashboard:', filtered_df['total_count_day'].sum())

st.subheader('Tren Penyewaan Sepeda')

# filtered_df.set_index('dteday', inplace=True)
# monthly_df = filtered_df.resample('M')['total_count_day'].sum().reset_index()
# monthly_df['year'] = monthly_df['dteday'].dt.year
# monthly_df['month'] = monthly_df['dteday'].dt.month

monthly_df = filtered_df.groupby(['year_day', 'month_day'])['total_count_day'].mean().reset_index()
monthly_df['year_day'] = monthly_df['year_day'].map({0: 2011, 1: 2012}) 

fig, ax = plt.subplots(figsize=(10, 6))

# Plot tahun 2011
ax.plot(
    monthly_df[monthly_df['year_day'] == 2011]['month_day'],
    monthly_df[monthly_df['year_day'] == 2011]['total_count_day'],
    marker='o'
)

# Plot tahun 2012
ax.plot(
    monthly_df[monthly_df['year_day'] == 2012]['month_day'],
    monthly_df[monthly_df['year_day'] == 2012]['total_count_day'],
    marker='o'
)

ax.set_title('Tren Bulanan Penyewaan Sepeda per Tahun')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Penyewaan')

# Paksa format angka di sumbu Y biar sama seperti notebook
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

ax.set_xticks(range(1, 13))
ax.legend(title='Tahun')

st.pyplot(fig)


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

