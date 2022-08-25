import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import spearmanr

#Import Data
data_polusi = pd.read_excel('resource/Data.xlsx', sheet_name='Norway')
data_mobil = pd.read_excel('resource/Data.xlsx', sheet_name='Car')
data_presentase = pd.read_excel('resource/Data.xlsx', sheet_name='Air')

#Page Config
st.set_page_config(
    page_title = "Dashboard Capstone Project IsaacDha",
    page_icon = (":sparkles:"),
    layout = 'wide')

with st.spinner(text = 'Loading Resources...'):
    time.sleep(5)

# Inject CSS to Hide Index Table
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
            
#Introduction
st.image('resource/Header.png')
st.write("---")
st.markdown('''<div style="text-align: justify;">
              Pemerintah RI dikabarkan tengah menyiapkan regulasi berupa instruksi presiden (inpres) terkait penggunaan kendaraan listrik di lingkungan pemerintahan. 
            Selain itu, Rencana investasi dan pembangunan pabrik baterai dan mobil listrik baru saja diluncurkan oleh beberapa perusahaan mobil listrik, sebut saja 
            Hyundai (Juni) dan Wuling (Juli). Dibalik rencana dan berita tersebut, tentunya banyak pro dan kontra mengenai mobil listrik yang akan menggantikan mobil
            berbahan bakar minyak. Apa saja perbedaan dari kedua jenis mobil tersebut? Berikut pembahasannya.</div>''', unsafe_allow_html=True)
st.write(' ')

#BAGIAN 1 : POLUSI MOBIL LISTRIK VS BENSIN
st.subheader("BAGIAN 1 : Polusi")
col11, col12 = st.columns([4,4], gap = "medium")
with col11:
    st.markdown('''<div style="text-align: justify;">
                  Perbedaan mendasar dari mobil listrik dan mobil bbm tentu saja dari polusinya. Mobil listrik bergerak menggunakan energi listrik yang tersimpan pada baterai, 
                sehingga dalam pengoperasiannya minim polusi. Disisi lain, Mobil bbm masih bergantung pada pembakaran minyak yang tentunya melepaskan banyak gas rumah kaca 
                yang merupakan penyebab polusi udara.</div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: justify;">
                  Dikutip dari Kompas.com, 75% dari polusi udara di Indonesia disebabkan oleh transportasi, diikuti oleh pembangkit listrik dan pemanas pada 9%, Industri 8%, 
                dan Domestik 8%. Data-data tersebut tersaji pada diagram lingkaran di samping ini. Fakta ini tentunya merupakan salah satu motivasi pemerintah dalam mendukung 
                peralihan jenis mobil baik dari regulasi maupun investasi.</div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: justify;">
                  Dari argumen diatas pastinya terdapat pertanyaan. Apakah terdapat hubungan dari peralihan tenaga mobil dari BBM ke listrik pada polusi udara?. Untuk menjawab hal
                tersebut, kita meminjam data dari Norwegia, yang merupakan salah satu negara yang berhasil melakukan peralihan energi mobil 10 tahun terakhir ini. Data dan
                pemeriksaan hubungan dari polusi dan mobil listrik dapat kita lihat dibawah ini.</div>''', unsafe_allow_html=True)

with col12:
    st.markdown('''<div style="text-align: center;">
                    Proporsi Penyebab Pencemaran Udara (sumberdata: kompas)
                    </div>''', unsafe_allow_html=True)
    data_barchart = data_presentase.copy()
    data_barchart.drop('Penyebab', axis = 1, inplace=True)
    #data_barchart.set_index('Alias', inplace=True)
    fig = px.pie(data_barchart, values='Presentase', names='Alias')
    #fig.layout.update(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Data Polusi & Kendaraan"):
    st.write('Berikut adalah data Polusi (pm10) dan Presentase kendaraan listrik (dilihat dari market share %) di Norwegia tahun 2010-2020 (sumber: statista.com & aqicn.org)')
    st.table(data_polusi)

data_r = data_polusi.copy()
data_r['Year'] = data_r['Year'].astype(str)
data_r.set_index('Year', inplace=True)

col5, col6 = st.columns([8,4], gap = "large")

with col5:
    st.markdown('***Trend Polusi Udara di Norwegia 2009-2020***')
    st.line_chart(data_r['Norways pm10 Pollution Index (pm10)'], height = 200)
    st.markdown('***Trend Market Share Kendaraan Listrik di Norwegia 2009-2020***')
    st.line_chart(data_r['Norways EV Vehicle Market Share (%)'], height = 200)

with col6:
    corr,pvalue = spearmanr(data_r['Norways pm10 Pollution Index (pm10)'], data_r['Norways EV Vehicle Market Share (%)'])
    st.metric("Korelasi Spearmann", round(corr,3))
    st.markdown('''<div style="text-align: justify;">
                  Polusi udara dan Proporsi Kendaraan Listrik di Norwegia Memiliki Hubungan Negatif Yang Kuat,
                Hubungan negatif tersebut menandakan semakin tinggi proporsi kendaraan listrik, maka polusi udara akan cenderung semakin rendah.
                </div>''', unsafe_allow_html=True)
    st.markdown('''<div style="text-align: justify;">
                  Dari pemeriksaan hubungan tersebut, tentunya sudah terjawab bahwa peralihan pemakaian mobil bbm ke mobil listrik akan menyebabkan 
                pengaruh yang baik pada berkurangnya polusi udara di negara kita. Polusi udara yang berkurang akan bermanfaat juga bagi kesehatan, kinerja, dan kemajuan 
                Bangsa Indonesia.
                </div>''', unsafe_allow_html=True)

st.write("---")
    

#Bagian 2 : COST MOBIL LISTRIK VS BENSIN
st.subheader("BAGIAN 2 : Cost / Biaya")
st.markdown('''<div style="text-align: justify;">
              Perbedaan selanjutnya sekaligus tantangan bagi peralihan energi adalah biaya (cost) dari mobil listrik itu sendiri. Biaya adalah uang yang 
            dikeluarkan untuk mengadakan/melakukan sesuatu (KBBI), sehingga harga dan biaya jalan masuk dalam komponen biaya itu sendiri. perbedaan biaya 
            kedua tipe model ini akan kita kulik satu-persatu.
            </div>''', unsafe_allow_html=True)
st.markdown(' ')
    
#Harga
st.subheader("Harga")
st.markdown('''<div style="text-align: justify;">
              Harga dari suatu produk sangat dipengaruhi oleh ketersediaan pabrik dan sumber daya suatu negara. 
            Mayoritas dari mobil listrik di Indonesia yang merupakan barang import pabrik luar negeri tentunya menyebabkan harganya melambung naik.
            Sebagai contoh, berikut adalah data harga dari 5 mobil bbm dan 4 mobil listrik terlaris di Indonesia selama 2022.
            </div>''', unsafe_allow_html=True)
st.markdown(' ')
with st.expander('Sumber'):
    st.markdown('***Sumber Data : Data Bulanan Penjualan Kendaraan Januari 2022 - Juni 2022 Gabungan Industri Kendaraan Bermotor Indonesia (GAIKINDO)***')
    st.markdown('***Website : gaikindo.or.id***')
st.write('')

col1, col2 = st.columns([4,6], gap = 'large')
data_mobil_harga = data_mobil.copy()
data_mobil_harga.drop([9,10], inplace=True)
data_mobil_harga['Kode'] = ['Rush MT', 'T Avanza', 'Xpander', 'Rush AT', 'Veloz', 'Ioniq5Ex', 'Leaf', 'Ioniq', 'Kona']
data_mobil_show = data_mobil_harga.copy()
data_mobil_show['Harga'] = data_mobil_show['Harga'].apply(lambda x: str(round(x/1000000)) + 'jt')

with col1:
    st.markdown('***Tabel Harga Mobil BBM dan Listrik Terlaris di Indonesia***')
    st.table(data_mobil_show[['Alias', 'Jenis', 'Harga', 'Kode']])

with col2:
    agregat = st.checkbox('Agregat')
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
            
    if agregat = False:
        st.markdown('''<div style="text-align: center;">
                        Harga Mobil BBM dan Listrik Terlaris di Indonesia
                    </div>''', unsafe_allow_html=True)
        st.bar_chart(data_bar, width=500, height=375)
    else:
        st.table(data_bar)

st.markdown('''<div style="text-align: justify;">
              Dari data dan grafik diatas, tentunya terlihat bahwa mobil listrik sangat mahal dibandingkan dengan mobil bbm yang tentunya merupakan halangan bagi
            masyarakat untuk beralih ke mobil listrik. perbedaan harga yang signifikan tersebut membuat masyarakat juga masih setia dalam menggunakan mobil bbm.
            </div>''', unsafe_allow_html=True) 
st.markdown(' ')

##Grafik Simulasi
st.subheader('Simulasi Cost')
st.markdown('''<div style="text-align: justify;">
              Klaim dari beberapa media mengatakan bahwa memilih untuk menggunakan mobil listrik lebih hemat biaya dibandingkan memilih untuk menggunakan mobil bbm karena harga listrik yang 
            lebih murah dibandingkan bbm. Apakah klaim tersebut benar?. Untuk menjawab klaim tersebut, kita dapat melakukan simulasi sederhana menggunakan komponen dari biaya
            itu sendiri, yaitu harga dan biaya per KM dengan acuan harga bensin Rp.7650/liter (Pertalite) dan harga listrik Rp.2466/kwh (SPKLU) yang dapat dilihat pada grafik dibawah.
            </div>''', unsafe_allow_html=True)
st.markdown(' ')
st.markdown(' ')
st.markdown("***Simulasi Perbandingan Total Cost***")
car_choice = st.multiselect('Pilih Mobil Untuk Dibandingkan', data_mobil['Alias'], ['EV-Based Vehicle', 'Gas-Based Vehicle'])

col3, col4 = st.columns([3, 1], gap="large")
with col3:
    number_of_sim = st.slider('Jarak Perjalanan (KM)', min_value=500000, max_value=10000000, value=2000000, step=500000)
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

st.markdown('''<div style="text-align: justify;">
            Dari hasil dari simulasi diatas, dapat dilihat bahwa secara garis besar biaya total dari mobil listrik lebih besar dari biaya total dari mobil bbm dikarenakan salah satu 
            komponen biaya, yaitu harga mobil listrik masih sangat mahal untuk saat ini. namun adanya investasi dan rencana pembangunan pabrik mobil listrik di Indonesia tentunya akan 
            menurunkan harga mobil listrik di kemudian hari.
            </div>''', unsafe_allow_html=True)
st.write("---")

#Bagian 3 : STASIUN PENGISIAN MOBIL LISTRIK VS BENSIN
st.subheader("BAGIAN 3 : Stasiun Pengisian")
st.markdown('''<div style="text-align: justify;">
              Perbandingan lainnya yang tidak kalah penting adalah stasiun pengisian mobil listrik, Kesulitan menemukan SPKLU dan ketimpangan antara jumlah SPBU dan 
            jumlah SPKLU merupakan halangan utama masyarakat dari memilih mobil listrik sebagai kendaraan sehari-harinya. Sebagai perbandingan, SPBU di Indonesia 
            tercatat berjumlah sebanyak 5518 buah, jauh mengalahkan jumlah SPKLU dengan jumlah sebanyak 184 yang tersebar di pulau-pulau tertentu. Penyebaran SPKLU 
            di Indonesia dapat dilihat pada grafik dibawah.
            </div>''', unsafe_allow_html=True)
st.markdown(' ')
st.markdown(' ')

col9, col10 = st.columns([6.5, 3.5], gap="medium")
with col9:
    st.markdown('''<div style="text-align: center;">
                   Peta Persebaran Stasiun Elektrik di Indonesia (sumberdata: kompasiana)
                   </div>''', unsafe_allow_html=True)
    st.image('resource/SPKLU-Transparent.png')
    
with col10:
    st.markdown('''<div style="text-align: justify;">
                  Dari grafik penyebaran SPKLU disamping, dapat dilihat bahwa SPKLU di Indonesia masih berpusat di Pulau Jawa saja, sementara itu daerah Kalimantan dan Papua masih belum
                terdapat stasiun pengisian sama sekali. Hal ini tentunya menjadi tantangan baik bagi pemerintah maupun perusahaan mobil listrik agar mobil listrik dapat dijangkau masyarakat
                di seluruh Indonesia.
                </div>''', unsafe_allow_html=True)

st.write("---")

#Bagian 4 : Kesimpulan
st.subheader("KESIMPULAN")
st.markdown('''<div style="text-align: justify;">
              Dari beberapa perbandingan diatas, kita dapat menyimpulkan bahwa banyak perbedaan antara mobil listrik dengan mobil berbahan bakar minyak. Indonesia sendiri masih belum siap jika terdapat peralihan besar-besaran 
            mobil bbm ke mobil listrik. Tantangan utama dari peralihan tersebut yaitu harga dan fasilitas pengisian masih terus dimimalkan pemerintah dan perusahaan mobil listrik melalui investasi dan pembangunan pabrik lokal serta pihak PLN yang membuka kerjasama dengan swasta 
            untuk perluasan SPKLU. Sangat diharapkan untuk pemerintah untuk mendukung program tersebut baik dari regulasi maupun investasi untuk mempercepat program peralihan mobil listrik tersebut demi Indonesia
            yang lebih baik.
            </div>''', unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
with st.expander("Footnote"):
    st.write('Sumber berita & data : kompas.co.id; gaikindo.or.id; autofun.co.id; oto.com; statista.com; aqicn.org; kompasiana.com')
    st.markdown('***Isaac Dwadattusyah Haikal Azziz @2022 - Capstone Project for TETRIS II By DQLab***')
    st.markdown("Penulis sadar bahwa masih banyak kekurangan dalam pembuatan artikel dashboard ini, untuk saran dan masukan dapat dikirimkan ke email Isaacazziz@gmail.com atau linkedin.com/in/isaacdha/")
