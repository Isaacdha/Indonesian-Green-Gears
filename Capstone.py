import streamlit as st
import time
import pandas as pd
import numpy as np
from scipy.stats import spearmanr

#Import Data
data_polusi = pd.read_excel('Data.xlsx', sheet_name='Norway')
data_mobil = pd.read_excel('Data.xlsx', sheet_name='Car')
data_presentase = pd.read_excel('Data.xlsx', sheet_name='Air')

#Page Config
st.set_page_config(
    page_title = "Dashboard Capstone Project IsaacDha",
    page_icon = (":sparkles:"),
    layout = 'wide')

with st.spinner(text = 'Loading Resources...'):
    time.sleep(5)

#Introduction
st.image('Header.png')
st.write("---")
st.write("""Pemerintah RI dikabarkan tengah menyiapkan regulasi berupa instruksi presiden (inpres) terkait penggunaan kendaraan listrik di lingkungan pemerintahan. 
            Selain itu, Rencana investasi dan pembangunan pabrik baterai dan mobil listrik baru saja diluncurkan oleh beberapa perusahaan mobil listrik, sebut saja 
            Hyundai (Juni) dan Wuling (Juli). Dibalik rencana dan berita tersebut, tentunya banyak pro dan kontra mengenai mobil listrik yang akan menggantikan mobil
            berbahan bakar minyak. Apa saja perbedaan dari kedua jenis mobil tersebut? Berikut pembahasannya.
""")

#BAGIAN 1 : POLUSI MOBIL LISTRIK VS BENSIN
st.subheader("BAGIAN 1 : Polusi Mobil Listrik VS Bensin")
col11, col12 = st.columns([6,3], gap = "large")
with col11:
    st.write("""Perbedaan mendasar dari mobil listrik dan mobil bbm tentu saja dari polusinya. Mobil listrik bergerak menggunakan energi listrik yang tersimpan pada baterai, 
                sehingga dalam pengoperasiannya minim polusi. Disisi lain, Mobil bbm masih bergantung pada pembakaran minyak yang tentunya melepaskan banyak gas rumah kaca 
                yang merupakan penyebab polusi udara.""")
    st.write("""
                Dikutip dari Kompas.com, 75% dari polusi udara di Indonesia disebabkan oleh transportasi, diikuti oleh pembangkit listrik dan pemanas pada 9%, Industri 8%, 
                dan Domestik 8%. Data-data tersebut tersaji pada diagram garis di samping ini. Fakta ini tentunya merupakan salah satu motivasi pemerintah dalam mendukung 
                peralihan jenis mobil baik dari regulasi maupun investasi.""")
    st.write("""
                Dari argumen diatas pastinya terdapat pertanyaan. Apakah terdapat hubungan dari peralihan tenaga mobil dari BBM ke listrik pada polusi udara?. Untuk menjawab hal
                tersebut, kita meminjam data dari Norwegia, yang merupakan salah satu negara yang berhasil melakukan peralihan energi mobil 10 tahun terakhir ini. Data dan
                pemeriksaan hubungan dari polusi dan mobil listrik dapat kita lihat dibawah ini. """)

with col12:
    st.markdown("***Proporsi Penyebab Pencemaran Udara (sumber: kompas)***")
    data_barchart = data_presentase.copy()
    data_barchart.drop('Penyebab', axis = 1, inplace=True)
    data_barchart.set_index('Alias', inplace=True)
    st.bar_chart(data_barchart)

with st.expander("Data Polusi (pm10) dan Presentase kendaraan listrik"):
    st.write('Berikut adalah data Polusi (pm10) dan Presentase kendaraan listrik (dilihat dari market share %) di Norwegia tahun 2010-2020 (sumber: statista.com & aqicn.org)')
    st.table(data_polusi)

data_r = data_polusi.copy()
data_r['Year'] = data_r['Year'].astype(str)
data_r.set_index('Year', inplace=True)

col5, col6 = st.columns([8,4], gap = "large")

with col5:
    st.markdown('***Line Chart Polusi Udara di Norwegia 2009-2020 (Trend Turun)***')
    st.line_chart(data_r['Norways pm10 Pollution Index (pm10)'], height = 200)
    st.markdown('***Line Chart Market Share Kendaraan Listrik di Norwegia 2009-2020 (Trend Naik)***')
    st.line_chart(data_r['Norways EV Vehicle Market Share (%)'], height = 200)

with col6:
    corr,pvalue = spearmanr(data_r['Norways pm10 Pollution Index (pm10)'], data_r['Norways EV Vehicle Market Share (%)'])
    st.metric("Korelasi Spearmann", round(corr,3),)
    st.write("""Polusi dan Proporsi Kendaraan Listrik di Norwegia Memiliki Hubungan Negatif Yang Kuat,
                Hubungan negatif tersebut menandakan semakin tinggi proporsi kendaraan listrik, maka populasi akan cenderung semakin rendah.""")
    st.write("""Dari pemeriksaan hubungan tersebut, tentunya sudah terjawab bahwa peralihan pemakaian mobil bbm ke mobil listrik akan menyebabkan 
                pengaruh yang baik pada berkurangnya polusi di negara kita. Polusi yang berkurang akan bermanfaat juga bagi kesehatan, kinerja, dan kemajuan 
                Bangsa Indonesia.""")

st.write("---")
    

#Bagian 2 : COST MOBIL LISTRIK VS BENSIN
st.subheader("BAGIAN 2 : Cost Mobil Listrik VS Bensin")
st.write("""Perbedaan selanjutnya sekaligus tantangan bagi peralihan energi adalah biaya (cost) dari mobil listrik itu sendiri. Biaya adalah uang yang 
            dikeluarkan untuk mengadakan/melakukan sesuatu (KBBI), sehingga harga dan biaya jalan masuk dalam komponen biaya itu sendiri. perbedaan biaya 
            kedua tipe model ini akan kita kulik satu-persatu.""")

#Harga
st.subheader("Harga")
st.write("""Harga dari suatu produk sangat dipengaruhi oleh ketersediaan pabrik dan sumber daya suatu negara. 
            Mayoritas dari mobil listrik di Indonesia yang merupakan barang import pabrik luar negeri tentunya menyebabkan harganya melambung naik.
            Sebagai contoh, berikut adalah data harga dari 5 mobil bbm dan 4 mobil listrik terlaris di Indonesia selama 2022.""")
with st.expander('Sumber'):
    st.markdown('***Sumber Data : Data Bulanan Penjualan Kendaraan Januari 2022 - Juni 2022 Gabungan Industri Kendaraan Bermotor Indonesia (GAIKINDO)***')
    st.markdown('***Website : gaikindo.or.id***')
st.write('')

col1, col2 = st.columns([4,6], gap = 'large')
data_mobil_harga = data_mobil.copy()
data_mobil_harga.drop([9,10], inplace=True)
data_mobil_harga['Kode'] = ['Rush MT', 'T Avanza', 'Xpander', 'Rush AT', 'Veloz', 'Ioniq5Ex', 'Leaf', 'Ioniq', 'Kona']

with col1:
    st.markdown('***Tabel Harga Mobil BBM dan Listrik Terlaris di Indonesia***')
    st.dataframe(data_mobil_harga[['Alias', 'Jenis', 'Harga', 'Kode']])

with col2:
    st.markdown('***Grafik Batang Harga Mobil BBM dan Listrik Terlaris di Indonesia***')
    data_bar = pd.DataFrame(np.random.randn(9, 2), columns=['BBM', 'Elektrik'])
    for i in range(0,len(data_mobil_harga)):
        if data_mobil_harga['Jenis'][i] == 'Bensin':
            data_bar['BBM'][i] = data_mobil_harga['Harga'][i]
            data_bar['Elektrik'][i] = 0
        else:
            data_bar['Elektrik'][i] = data_mobil_harga['Harga'][i]
            data_bar['BBM'][i] = 0
    data_bar['Index'] = data_mobil_harga['Kode']
    data_bar.set_index('Index', inplace=True)
    st.bar_chart(data_bar, width=500, height=375)

st.write("""Dari data dan grafik diatas, tentunya terlihat bahwa mobil listrik sangat mahal dibandingkan dengan mobil bbm yang tentunya merupakan halangan bagi
            masyarakat untuk beralih ke mobil listrik. perbedaan harga yang signifikan tersebut membuat masyarakat juga masih setia dalam menggunakan mobil bbm.""")  

##Grafik Simulasi
st.subheader('Simulasi Cost')
st.write("""Klaim dari beberapa media mengatakan bahwa memilih untuk menggunakan mobil listrik lebih hemat biaya dibandingkan memilih untuk menggunakan mobil bbm karena harga listrik yang 
            lebih murah dibandingkan bbm. Apakah klaim tersebut benar?. Untuk menjawab klaim tersebut, kita dapat melakukan simulasi sederhana menggunakan komponen dari biaya
            itu sendiri, yaitu harga dan biaya per KM dengan acuan harga bensin Rp.7650/liter (Pertalite) dan harga listrik Rp.2466/kwh (SPKLU) yang dapat dilihat pada grafik dibawah.
        """)
st.markdown("***Simulasi Perbandingan Total Cost***")
car_choice = st.multiselect('Pilih Mobil Untuk Dibandingkan', data_mobil['Alias'], ['EV-Based Vehicle', 'Gas-Based Vehicle'])

col3, col4 = st.columns([3, 1], gap="large")
with col3:
    number_of_sim = st.slider('Jarak Perjalanan (KM)', min_value=500000, max_value=10000000, step=500000)
    n = range(0, int(number_of_sim), int((number_of_sim/30)))
    sim_dataframe = pd.DataFrame()
    sim_dataframe['Index'] = list(n)
    sim_dataframe.set_index('Index', inplace=True)
    
    for i in car_choice:
        car_price = data_mobil[data_mobil['Alias'] == i]['Harga']
        car_consumption = data_mobil[data_mobil['Alias'] == i]['Biaya per KM']
        list = []
        for j in n:
            worth = car_price + j*1*car_consumption
            list.append(int(worth))
        sim_dataframe[i] = list
    
    st.line_chart(sim_dataframe, width = 800)

with col4:
    car_min_choice = st.selectbox('Pilih Mobil Sebagai Dasar Perhitungan Total Cost', car_choice)
    base_price = data_mobil[data_mobil['Alias'] == car_min_choice]['Harga'].values[0]
    base_consumption = data_mobil[data_mobil['Alias'] == car_min_choice]['Biaya per KM'].values[0]
    car_comparison = car_choice.copy()
    car_comparison.remove(car_min_choice)

    for i in car_comparison:
        car_price = data_mobil[data_mobil['Alias'] == i]['Harga'].values[0]
        car_consumption = data_mobil[data_mobil['Alias'] == i]['Biaya per KM'].values[0]
        if car_price < base_price and car_consumption < base_consumption:
            st.write('Harga dan konsumsi per KM dari mobil ' + str(i) + ' Lebih rendah dibandingkan dengan mobil ' + str(car_min_choice) + ' Sehingga tidak terdapat penyelesaian')
        elif car_price > base_price and car_consumption > base_consumption:
            st.write('Harga dan konsumsi per KM dari mobil ' + str(i) + ' Lebih tinggi dibandingkan dengan mobil ' + str(car_min_choice) + ' Sehingga tidak terdapat penyelesaian')
        else:
            xsolve = round((base_price-car_price)/(car_consumption-base_consumption))
            st.write('Cost total dari mobil ' + str(i) + ' dan mobil ' + str(car_min_choice) + ' akan sama pada perjalanan kilometer ke-' + str(xsolve))

st.write("""Dari hasil dari simulasi diatas, dapat dilihat bahwa secara garis besar biaya total dari mobil listrik lebih besar dari biaya total dari mobil bbm dikarenakan salah satu 
            komponen biaya, yaitu harga mobil listrik masih sangat mahal untuk saat ini. namun adanya investasi dan rencana pembangunan pabrik mobil listrik di Indonesia tentunya akan 
            menurunkan harga mobil listrik di kemudian hari.""" )
st.write("---")

#Bagian 3 : STASIUN PENGISIAN MOBIL LISTRIK VS BENSIN
st.subheader("BAGIAN 3 : STASIUN PENGISIAN MOBIL LISTRIK VS BENSIN")
st.write("""Perbandingan lainnya yang tidak kalah penting adalah stasiun pengisian mobil listrik, Kesulitan menemukan SPKLU dan ketimpangan antara jumlah SPBU dan 
            jumlah SPKLU merupakan halangan utama masyarakat dari memilih mobil listrik sebagai kendaraan sehari-harinya. Sebagai perbandingan, SPBU di Indonesia 
            tercatat berjumlah sebanyak 5518 buah, jauh mengalahkan jumlah SPKLU dengan jumlah sebanyak 184 yang tersebar di pulau-pulau tertentu. Penyebaran SPKLU 
            di Indonesia dapat dilihat pada grafik dibawah.""")

col9, col10 = st.columns([3, 1], gap="large")
with col9:
    st.markdown("***Persebaran Stasiun Bahan Bakar di Indonesia (sumber: kompasiana)***")
    st.image('SPKLU-Transparent.png')
with col10:
    st.write("""Dari grafik penyebaran SPKLU disamping, dapat dilihat bahwa SPKLU di Indonesia masih berpusat di Pulau Jawa saja, sementara itu daerah Kalimantan dan Papua masih belum
                terdapat stasiun pengisian sama sekali. Hal ini tentunya menjadi tantangan baik bagi pemerintah maupun perusahaan mobil listrik agar mobil listrik dapat dijangkau masyarakat
                di seluruh Indonesia.""")

st.write("---")

#Bagian 4 : Kesimpulan
st.subheader("KESIMPULAN")
st.write("""Dari beberapa perbandingan diatas, kita dapat menyimpulkan bahwa banyak perbedaan antara mobil listrik dengan mobil berbahan bakar minyak. Indonesia sendiri masih belum siap jika terdapat peralihan besar-besaran 
            mobil bbm ke mobil listrik. Tantangan utama dari peralihan tersebut yaitu harga dan fasilitas pengisian masih terus dimimalkan pemerintah dan perusahaan mobil listrik melalui investasi dan pembangunan pabrik lokal serta pihak PLN yang membuka kerjasama dengan swasta 
            untuk perluasan SPKLU. Sangat diharapkan untuk pemerintah untuk mendukung program tersebut baik dari regulasi maupun investasi untuk mempercepat program peralihan mobil listrik tersebut demi Indonesia
            yang lebih baik.
            """)
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
with st.expander("Footnote"):
    st.write('Sumber berita & data : kompas.co.id; gaikindo.or.id; autofun.co.id; oto.com; statista.com; aqicn.org; kompasiana.com')
    st.markdown('***Isaac Dwadattusyah Haikal Azziz @2022 - Capstone Project for TETRIS II By DQLab***')
    st.markdown("Penulis sadar bahwa masih banyak kekurangan dalam pembuatan artikel dashboard ini, untuk saran dan masukan dapat dikirimkan ke email Isaacazziz@gmail.com")