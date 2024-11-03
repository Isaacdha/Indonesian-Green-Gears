import streamlit as st
import time
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import spearmanr
from streamlit_option_menu import option_menu
from PIL import Image

#Page Config
st.set_page_config(
    page_title = "Green Gears : The Shift to Electric Vehicles in Indonesia",
    page_icon = (":sparkles:"),
    layout = 'wide')

#Import Data
@st.cache_data
def load_data():
    data_polusi = pd.read_excel('resource/Data.xlsx', sheet_name='Norway')
    data_mobil = pd.read_excel('resource/Data.xlsx', sheet_name='Car')
    data_presentase = pd.read_excel('resource/Data.xlsx', sheet_name='Air')
    data_presentase.drop('Penyebab', axis = 1, inplace=True)
    
    data_r = data_polusi.copy()
    data_r['Year'] = data_r['Year'].astype(str)
    data_r.set_index('Year', inplace=True)
    
    data_mobil_harga = data_mobil.copy()
    data_mobil_harga.drop([9,10], inplace=True)
    data_mobil_harga['Kode'] = ['Rush MT', 'T Avanza', 'Xpander', 'Rush AT', 'Veloz', 'Ioniq5Ex', 'Leaf', 'Ioniq', 'Kona']
    data_mobil_show = data_mobil_harga.copy()
    data_mobil_show['Harga'] = data_mobil_show['Harga'].apply(lambda x: str(round(x/1000000)) + 'jt')
    
    return data_polusi, data_mobil, data_presentase, data_r, data_mobil_harga, data_mobil_show

data_polusi, data_mobil, data_presentase, data_r, data_mobil_harga, data_mobil_show = load_data()

@st.cache_resource
def load_image(image_path):
    return Image.open(image_path)


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

# Sidebar Title
st.logo(load_image('resource/logo.png'), icon_image=load_image('resource/Logo_small.png'), size='large')
st.sidebar.image(load_image('resource/dashboard_image.webp'), use_column_width=True)
st.sidebar.title("Green Gears Dashboard")
with st.sidebar:
    page = option_menu(
        "Navigation",
        ["🏠 Overview", 
         "🌍 Pollution", 
         "💰 Cost",
         "🔌 Charging Station",
         "📄 Conclusion"],
        styles = {
            "menu-title" : {"font-size": "20px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#6082B6"},
            "container": {"background-color": "#36454F", "border": "1px solid white"},  # Match the sidebar color and add white border
            "nav-link-selected": {"background-color": "#00203FFF"}  # Change the selected page option color
        }
    )

# Language Selection
language = st.sidebar.selectbox("Choose Language", ('English', 'Indonesian'))

#Introduction
if page == "🏠 Overview":
    st.markdown("""
            <style>
                div[data-testid="column"] {
                    width: fit-content !important;
                    flex: unset;
                }
                div[data-testid="column"] * {
                    width: fit-content !important;
                }
            </style>
            """, unsafe_allow_html=True)
    if language == 'English':
        st.image(load_image('resource/Header_en.png'))
    else:
        st.image(load_image('resource/Header.png'))
    st.write("---")
    if language == 'English':
        st.markdown('''<div style="text-align: justify;">
                    The Indonesian government is reportedly preparing regulations in the form of a presidential instruction (inpres) regarding the use of electric vehicles in the government environment. 
                    In addition, investment plans and the construction of new battery and electric car factories have just been launched by several electric car companies, such as Hyundai (June) and Wuling (July). 
                    Behind these plans and news, there are certainly many pros and cons regarding electric cars that will replace fuel-powered cars. What are the differences between the two types of cars? Here is the discussion.</div>''', unsafe_allow_html=True)
        st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
        st.write("Please choose an option from the navigation bar to begin.")
    else:
        st.markdown('''<div style="text-align: justify;">
                    Pemerintah RI dikabarkan tengah menyiapkan regulasi berupa instruksi presiden (inpres) terkait penggunaan kendaraan listrik di lingkungan pemerintahan. 
                    Selain itu, Rencana investasi dan pembangunan pabrik baterai dan mobil listrik baru saja diluncurkan oleh beberapa perusahaan mobil listrik, sebut saja 
                    Hyundai (Juni) dan Wuling (Juli). Dibalik rencana dan berita tersebut, tentunya banyak pro dan kontra mengenai mobil listrik yang akan menggantikan mobil
                    berbahan bakar minyak. Apa saja perbedaan dari kedua jenis mobil tersebut? Berikut pembahasannya.</div>''', unsafe_allow_html=True)
        st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
        st.write("Silahkan pilih opsi dari menu navigasi untuk memulai.")
    st.write(' ')

    with st.popover('Disclaimer'):
        if language == 'English':
            st.markdown('***Capstone Project for TETRIS II 2022 By DQLab***')
            st.markdown("The author realizes that there are still many shortcomings in the creation of this dashboard article. Suggestions and input can be sent to the author's email/LinkedIn")
        else:
            st.markdown('***Proyek Akhir untuk TETRIS II 2022 Oleh DQLab***')
            st.markdown("Penulis sadar bahwa masih banyak kekurangan dalam pembuatan artikel dashboard ini. Saran dan masukan dapat dikirimkan ke email/LinkedIn penulis")
    with st.popover('News & Data Source'):
        st.markdown('kompas.co.id; gaikindo.or.id; autofun.co.id; oto.com; statista.com; aqicn.org; kompasiana.com')
    with st.popover('Author'):
        st.markdown("### Isaac Dwadattusyah Haikal Azziz")
        st.write("""
                - **Email:** Isaacazziz@gmail.com
                - **LinkedIn:** [Isaac Dha](https://linkedin.com/in/isaacdha/)
                - **GitHub:** [Isaac's Git](https://github.com/Isaacdha)
                """)

#BAGIAN 1 : POLUSI MOBIL LISTRIK VS BENSIN
if page == "🌍 Pollution":
    if language == 'English':
        st.subheader("SECTION 1: Pollution")
    else:
        st.subheader("BAGIAN 1 : Polusi")
    col11, col12 = st.columns([4,4], gap = "medium")
    with col11:
        if language == 'English':
            st.markdown('''<div style="text-align: justify;">
                        The fundamental difference between electric cars and fuel-powered cars is, of course, their pollution. Electric cars run on electricity stored in batteries,
                        so their operation produces minimal pollution. On the other hand, fuel-powered cars still rely on burning oil, which releases a lot of greenhouse gases
                        that cause air pollution.</div>''', unsafe_allow_html=True)
            st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
            st.markdown('''<div style="text-align: justify;">
                        According to Kompas.com, 75% of air pollution in Indonesia is caused by transportation, followed by power plants and heating at 9%, industry at 8%,
                        and domestic sources at 8%. These data are presented in the pie chart next to this. This fact is certainly one of the motivations for the government to support
                        the transition of car types both from regulations and investments.</div>''', unsafe_allow_html=True)
            st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
            st.markdown('''<div style="text-align: justify;">
                        From the arguments above, there is certainly a question. Is there a relationship between the transition of car energy from fuel to electricity on air pollution? To answer this,
                        we borrow data from Norway, which is one of the countries that has successfully made the energy transition for cars in the last 10 years. The data and
                        examination of the relationship between pollution and electric cars can be seen below.</div>''', unsafe_allow_html=True)
        else:
            st.markdown('''<div style="text-align: justify;">
                        Perbedaan mendasar dari mobil listrik dan mobil bbm tentu saja dari polusinya. Mobil listrik bergerak menggunakan energi listrik yang tersimpan pada baterai, 
                        sehingga dalam pengoperasiannya minim polusi. Disisi lain, Mobil bbm masih bergantung pada pembakaran minyak yang tentunya melepaskan banyak gas rumah kaca 
                        yang merupakan penyebab polusi udara.</div>''', unsafe_allow_html=True)
            st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
            st.markdown('''<div style="text-align: justify;">
                        Dikutip dari Kompas.com, 75% dari polusi udara di Indonesia disebabkan oleh transportasi, diikuti oleh pembangkit listrik dan pemanas pada 9%, Industri 8%, 
                        dan Domestik 8%. Data-data tersebut tersaji pada diagram lingkaran di samping ini. Fakta ini tentunya merupakan salah satu motivasi pemerintah dalam mendukung 
                        peralihan jenis mobil baik dari regulasi maupun investasi.</div>''', unsafe_allow_html=True)
            st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
            st.markdown('''<div style="text-align: justify;">
                        Dari argumen diatas pastinya terdapat pertanyaan. Apakah terdapat hubungan dari peralihan tenaga mobil dari BBM ke listrik pada polusi udara?. Untuk menjawab hal
                        tersebut, kita meminjam data dari Norwegia, yang merupakan salah satu negara yang berhasil melakukan peralihan energi mobil 10 tahun terakhir ini. Data dan
                        pemeriksaan hubungan dari polusi dan mobil listrik dapat kita lihat dibawah ini.</div>''', unsafe_allow_html=True)

    st.markdown(' ')
    with col12:
        if language == 'English':
            st.markdown('''<div style="text-align: center;">
                            Proportion of Air Pollution Causes (source: kompas)
                            </div>''', unsafe_allow_html=True)
        else:
            st.markdown('''<div style="text-align: center;">
                            Proporsi Penyebab Pencemaran Udara (sumberdata: kompas)
                            </div>''', unsafe_allow_html=True)
        #data_barchart.set_index('Alias', inplace=True)
        fig = px.pie(data_presentase, values='Presentase', names='Alias')
        #fig.layout.update(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    if language == 'Indonesian':
        with st.expander("Data Polusi & Kendaraan"):
            st.write('Berikut adalah data Polusi (pm10) dan Presentase kendaraan listrik (dilihat dari market share %) di Norwegia tahun 2010-2020 (sumber: statista.com & aqicn.org)')
            st.table(data_polusi)
    else:
        with st.expander("Pollution & Vehicle Data"):
            st.write('Here is the Pollution (pm10) and Electric Vehicle Market Share (%) data in Norway from 2010-2020 (source: statista.com & aqicn.org)')
            st.table(data_polusi)  
        
    with st.container(border=True):
        if language == 'English':
            st.markdown("#### Trend of Air Pollution & Electric Vehicle Market Share in Norway")
        else:
            st.markdown("#### Trend Polusi Udara & Market Share Kendaraan Listrik di Norwegia")
        col5, col6 = st.columns([7,5], gap = "medium")
        with col5:
            if language == 'English':
                st.markdown('***Trend of Air Pollution in Norway 2009-2020***')
                st.line_chart(data_r['Norways pm10 Pollution Index (pm10)'], height=200)
                st.markdown('***Trend of Electric Vehicle Market Share in Norway 2009-2020***')
                st.line_chart(data_r['Norways EV Vehicle Market Share (%)'], height=200)
            else:
                st.markdown('***Trend Polusi Udara di Norwegia 2009-2020***')
                st.line_chart(data_r['Norways pm10 Pollution Index (pm10)'], height=200)
                st.markdown('***Trend Market Share Kendaraan Listrik di Norwegia 2009-2020***')
                st.line_chart(data_r['Norways EV Vehicle Market Share (%)'], height=200)

        with col6:
            corr, pvalue = spearmanr(data_r['Norways pm10 Pollution Index (pm10)'], data_r['Norways EV Vehicle Market Share (%)'])
            st.metric("Spearman Correlation", round(corr, 3))
            # Center the Spearman Correlation metric
            center_correlation_metric = """
                <style>
                .stMetric {
                text-align: center;
                }
                .stMetric label {
                display: flex;
                justify-content: center;
                }
                </style>
                """
            st.markdown(center_correlation_metric, unsafe_allow_html=True)
            if language == 'English':
                st.markdown('''<div style="text-align: justify;">
                            Air pollution and the proportion of electric vehicles in Norway have a strong negative relationship.
                            This negative relationship indicates that the higher the proportion of electric vehicles, the lower the air pollution tends to be.
                            </div>''', unsafe_allow_html=True)
                st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
                st.markdown('''<div style="text-align: justify;">
                            From this relationship examination, it is clear that the transition from fuel-powered cars to electric vehicles will have a positive impact
                            on reducing air pollution in our country. Reduced air pollution will also benefit the health, performance, and progress of the Indonesian nation.
                            </div>''', unsafe_allow_html=True)
            else:
                st.markdown('''<div style="text-align: justify;">
                            Polusi udara dan Proporsi Kendaraan Listrik di Norwegia Memiliki Hubungan Negatif Yang Kuat,
                            Hubungan negatif tersebut menandakan semakin tinggi proporsi kendaraan listrik, maka polusi udara akan cenderung semakin rendah.
                            </div>''', unsafe_allow_html=True)
                st.markdown('<div style="font-size: small;"></div>', unsafe_allow_html=True)
                st.markdown('''<div style="text-align: justify;">
                            Dari pemeriksaan hubungan tersebut, tentunya sudah terjawab bahwa peralihan pemakaian mobil bbm ke mobil listrik akan menyebabkan 
                            pengaruh yang baik pada berkurangnya polusi udara di negara kita. Polusi udara yang berkurang akan bermanfaat juga bagi kesehatan, kinerja, dan kemajuan 
                            Bangsa Indonesia.
                            </div>''', unsafe_allow_html=True)

    st.write("---")
    
#Bagian 2 : COST MOBIL LISTRIK VS BENSIN
if page == "💰 Cost":
    if language == 'English':
        st.subheader("SECTION 2: Cost")
        st.markdown('''<div style="text-align: justify;">
                    The next difference and challenge for the energy transition is the cost of electric cars themselves. Cost is the money spent to procure/do something (KBBI), so the price and running costs are included in the cost components themselves. We will explore the cost differences of these two types of models one by one.
                    </div>''', unsafe_allow_html=True)
        st.markdown(' ')
    else:
        st.subheader("BAGIAN 2 : Cost / Biaya")
        st.markdown('''<div style="text-align: justify;">
                    Perbedaan selanjutnya sekaligus tantangan bagi peralihan energi adalah biaya (cost) dari mobil listrik itu sendiri. Biaya adalah uang yang 
                    dikeluarkan untuk mengadakan/melakukan sesuatu (KBBI), sehingga harga dan biaya jalan masuk dalam komponen biaya itu sendiri. perbedaan biaya 
                    kedua tipe model ini akan kita kulik satu-persatu.
                    </div>''', unsafe_allow_html=True)
        st.markdown(' ')

    st.write('---')
    #Harga
    if language == 'English':
        st.subheader("Price")
        st.markdown('''<div style="text-align: justify;">
                    The price of a product is greatly influenced by the availability of factories and resources in a country. 
                    The majority of electric cars in Indonesia, which are imported from foreign factories, certainly cause their prices to skyrocket.
                    For example, here is the price data of the 5 best-selling fuel cars and 4 best-selling electric cars in Indonesia during 2022.
                    </div>''', unsafe_allow_html=True)
        st.markdown(' ')
    else:
        st.subheader("Harga")
        st.markdown('''<div style="text-align: justify;">
                    Harga dari suatu produk sangat dipengaruhi oleh ketersediaan pabrik dan sumber daya suatu negara. 
                    Mayoritas dari mobil listrik di Indonesia yang merupakan barang import pabrik luar negeri tentunya menyebabkan harganya melambung naik.
                    Sebagai contoh, berikut adalah data harga dari 5 mobil bbm dan 4 mobil listrik terlaris di Indonesia selama 2022.
                    </div>''', unsafe_allow_html=True)
        st.markdown(' ')

    with st.expander('Sumber' if language == 'Indonesian' else 'Source'):
        st.markdown('***Sumber Data : Data Bulanan Penjualan Kendaraan Januari 2022 - Juni 2022 Gabungan Industri Kendaraan Bermotor Indonesia (GAIKINDO)***' if language == 'Indonesian' else '***Data Source: Monthly Vehicle Sales Data January 2022 - June 2022 Indonesian Automotive Industry Association (GAIKINDO)***')
        st.markdown('***Website : gaikindo.or.id***')
    st.write('')

    with st.container(border=True):
        col1, col2 = st.columns([4,6], gap = 'large')

        with col1:
            if language == 'English':
                st.markdown('***Table of Best-Selling Gas and Electric Car Prices in Indonesia***')
            else:
                st.markdown('***Tabel Harga Mobil BBM dan Listrik Terlaris di Indonesia***')
            st.dataframe(data_mobil_show[['Alias', 'Jenis', 'Harga', 'Kode']])

        with col2:
            agregat = st.checkbox('Agregat' if language == 'Indonesian' else 'Aggregate', value=True)
                    
            if agregat:
                data_bar = pd.DataFrame(np.random.randn(9, 2), columns=['Gasoline (BBM)', 'Elektrik'])
                for i in range(0, len(data_mobil_harga)):
                    if data_mobil_harga.loc[i, 'Jenis'] == 'Gasoline':
                        data_bar.loc[i, 'Gasoline (BBM)'] = data_mobil_harga.loc[i, 'Harga']
                        data_bar.loc[i, 'Electric'] = 0
                    else:
                        data_bar.loc[i, 'Electric'] = data_mobil_harga.loc[i, 'Harga']
                        data_bar.loc[i, 'Gasoline (BBM)'] = 0
                data_bar['Index'] = data_mobil_harga['Kode']
                data_bar.set_index('Index', inplace=True)
                data_bar_agg = pd.DataFrame(np.zeros((2,2)), columns=['Gasoline (BBM)', 'Electric'])
                data_bar_agg.iloc[0,0] = data_bar[data_bar["Gasoline (BBM)"] != 0]["Gasoline (BBM)"].mean()
                data_bar_agg.iloc[1,1] = data_bar[data_bar["Electric"] != 0]["Electric"].mean()
                if language == 'English':
                    st.markdown('''<div style="text-align: center;">
                        Price of Gas vs Electric Cars in Indonesia
                        </div>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<div style="text-align: center;">
                        Harga Mobil BBM vs Listrik di Indonesia
                        </div>''', unsafe_allow_html=True)
                data_bar_agg['Index'] = ['Gasoline (BBM)', 'Electric']
                data_bar_agg.set_index('Index', inplace=True)
                fig = px.bar(data_bar_agg, y=data_bar_agg.columns, labels={'index': '', 'variable': 'Type'})
                fig.update_layout(xaxis={'visible': False}, height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                if language == 'English':
                    st.markdown('''<div style="text-align: center;">
                            Price of Best-Selling Gas and Electric Cars in Indonesia
                            </div>''', unsafe_allow_html=True)
                else:
                    st.markdown('''<div style="text-align: center;">
                            Harga Mobil BBM dan Listrik Terlaris di Indonesia
                            </div>''', unsafe_allow_html=True)
                data_bar = pd.DataFrame(np.random.randn(9, 2), columns=['Gasoline (BBM)', 'Electric'])
                for i in range(0,len(data_mobil_harga)):
                    if data_mobil_harga['Jenis'][i] == 'Gasoline':
                        data_bar['Gasoline (BBM)'][i] = data_mobil_harga['Harga'][i]
                        data_bar['Electric'][i] = 0
                    else:
                        data_bar['Electric'][i] = data_mobil_harga['Harga'][i]
                        data_bar['Gasoline (BBM)'][i] = 0
                data_bar['Index'] = data_mobil_harga['Kode']
                data_bar.set_index('Index', inplace=True)
                st.bar_chart(data_bar, width=500, height=375)

    if language == 'English':
        st.markdown('''<div style="text-align: justify;">
                    From the data and graphs above, it is clear that electric cars are much more expensive compared to fuel-powered cars, which is certainly an obstacle for
                    people to switch to electric cars. This significant price difference makes people still loyal to using fuel-powered cars.
                    </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div style="text-align: justify;">
                    Dari data dan grafik diatas, tentunya terlihat bahwa mobil listrik sangat mahal dibandingkan dengan mobil bbm yang tentunya merupakan halangan bagi
                    masyarakat untuk beralih ke mobil listrik. perbedaan harga yang signifikan tersebut membuat masyarakat juga masih setia dalam menggunakan mobil bbm.
                    </div>''', unsafe_allow_html=True)
    st.markdown(' ')

    ##Grafik Simulasi
    st.write('---')
    st.subheader('Simulasi Cost' if language == 'Indonesian' else 'Cost Simulation')
    st.markdown('''<div style="text-align: justify;">
                Klaim dari beberapa media mengatakan bahwa memilih untuk menggunakan mobil listrik lebih hemat biaya dibandingkan memilih untuk menggunakan mobil bbm karena harga listrik yang 
                lebih murah dibandingkan bbm. Apakah klaim tersebut benar?. Untuk menjawab klaim tersebut, kita dapat melakukan simulasi sederhana menggunakan komponen dari biaya
                itu sendiri, yaitu harga dan biaya per KM dengan acuan harga bensin Rp.7650/liter (Pertalite) dan harga listrik Rp.2466/kwh (SPKLU) yang dapat dilihat pada grafik dibawah.
                </div>''' if language == 'Indonesian' else '''<div style="text-align: justify;">
                Claims from some media say that choosing to use electric cars is more cost-effective compared to choosing to use fuel-powered cars because the price of electricity is 
                cheaper than fuel. Is this claim true? To answer this claim, we can perform a simple simulation using the cost components themselves, namely the price and cost per KM 
                with a reference price of Rp.7650/liter (Pertalite) for fuel and Rp.2466/kwh (SPKLU) for electricity, which can be seen in the graph below.
                </div>''', unsafe_allow_html=True)
    st.markdown(' ')
    st.markdown(' ')
    st.markdown("***Simulasi Perbandingan Total Cost***" if language == 'Indonesian' else "***Total Cost Comparison Simulation***")
    car_choice = st.multiselect('Pilih Mobil Untuk Dibandingkan' if language == 'Indonesian' else 'Select Cars for Comparison', data_mobil['Alias'], ['EV-Based Vehicle', 'Gas-Based Vehicle'])

    col3, col4 = st.columns([3, 1], gap="large")
    with col3:
        if language == 'Indonesian':
            number_of_sim = st.slider('Jarak Perjalanan (KM)', min_value=500000, max_value=10000000, value=2000000, step=500000)
        else:
            number_of_sim = st.slider('Travel Distance (KM)', min_value=500000, max_value=10000000, value=2000000, step=500000)
        n = range(0, int(number_of_sim), int((number_of_sim/30)))
        sim_dataframe = pd.DataFrame()
        sim_dataframe['Index'] = list(n)
        sim_dataframe.set_index('Index', inplace=True)
        
        for i in car_choice:
            car_price = data_mobil[data_mobil['Alias'] == i]['Harga']
            car_consumption = data_mobil[data_mobil['Alias'] == i]['Biaya per KM']
            list = []
            for j in n:
                worth = car_price.iloc[0] + j * car_consumption.iloc[0]
                list.append(int(worth))
            sim_dataframe[i] = list
        
        st.line_chart(sim_dataframe, width = 800)

    with col4:
        if language == 'Indonesian':
            car_min_choice = st.selectbox('Pilih Mobil Sebagai Dasar Perhitungan Total Cost', car_choice)
        else:
            car_min_choice = st.selectbox('Select Car as Base for Total Cost Calculation', car_choice)
        base_price = data_mobil[data_mobil['Alias'] == car_min_choice]['Harga'].values[0]
        base_consumption = data_mobil[data_mobil['Alias'] == car_min_choice]['Biaya per KM'].values[0]
        car_comparison = car_choice.copy()
        car_comparison.remove(car_min_choice)

        for i in car_comparison:
            car_price = data_mobil[data_mobil['Alias'] == i]['Harga'].values[0]
            car_consumption = data_mobil[data_mobil['Alias'] == i]['Biaya per KM'].values[0]
            if car_price < base_price and car_consumption < base_consumption:
                if language == 'Indonesian':
                    st.write('Harga dan konsumsi per KM dari mobil ' + str(i) + ' Lebih rendah dibandingkan dengan mobil ' + str(car_min_choice) + ' Sehingga tidak terdapat penyelesaian')
                else:
                    st.write('The price and consumption per KM of the car ' + str(i) + ' are lower than the car ' + str(car_min_choice) + ' so there is no solution')
            elif car_price > base_price and car_consumption > base_consumption:
                if language == 'Indonesian':
                    st.write('Harga dan konsumsi per KM dari mobil ' + str(i) + ' Lebih tinggi dibandingkan dengan mobil ' + str(car_min_choice) + ' Sehingga tidak terdapat penyelesaian')
                else:
                    st.write('The price and consumption per KM of the car ' + str(i) + ' are higher than the car ' + str(car_min_choice) + ' so there is no solution')
            else:
                xsolve = round((base_price-car_price)/(car_consumption-base_consumption))
                if language == 'Indonesian':
                    st.write('Cost total dari mobil ' + str(i) + ' dan mobil ' + str(car_min_choice) + ' akan sama pada perjalanan kilometer ke-' + str(xsolve))
                else:
                    st.write('The total cost of the car ' + str(i) + ' and the car ' + str(car_min_choice) + ' will be the same at kilometer-' + str(xsolve))

    if language == 'Indonesian':
        st.markdown('''<div style="text-align: justify;">
                    Dari hasil dari simulasi diatas, dapat dilihat bahwa secara garis besar biaya total dari mobil listrik lebih besar dari biaya total dari mobil bbm dikarenakan salah satu 
                    komponen biaya, yaitu harga mobil listrik masih sangat mahal untuk saat ini. namun adanya investasi dan rencana pembangunan pabrik mobil listrik di Indonesia tentunya akan 
                    menurunkan harga mobil listrik di kemudian hari.
                    </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div style="text-align: justify;">
                    From the results of the simulation above, it can be seen that in general, the total cost of electric cars is greater than the total cost of fuel cars because one of the 
                    cost components, namely the price of electric cars, is still very expensive at this time. However, the investment and plans to build electric car factories in Indonesia 
                    will certainly reduce the price of electric cars in the future.
                    </div>''', unsafe_allow_html=True)
    st.write("---")

#Bagian 3 : STASIUN PENGISIAN MOBIL LISTRIK VS BENSIN
if page == "🔌 Charging Station":
    st.subheader("BAGIAN 3 : Stasiun Pengisian" if language == 'Indonesian' else "SECTION 3: Charging Stations")
    if language == 'Indonesian':
        st.markdown('''<div style="text-align: justify;">
                    Perbandingan lainnya yang tidak kalah penting adalah stasiun pengisian mobil listrik, Kesulitan menemukan SPKLU dan ketimpangan antara jumlah SPBU dan 
                    jumlah SPKLU merupakan halangan utama masyarakat dari memilih mobil listrik sebagai kendaraan sehari-harinya. Sebagai perbandingan, SPBU di Indonesia 
                    tercatat berjumlah sebanyak 5518 buah, jauh mengalahkan jumlah SPKLU dengan jumlah sebanyak 184 yang tersebar di pulau-pulau tertentu. Penyebaran SPKLU 
                    di Indonesia dapat dilihat pada grafik dibawah.
                    </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div style="text-align: justify;">
                    Another equally important comparison is the charging stations for electric cars. The difficulty of finding charging stations (SPKLU) and the disparity 
                    between the number of gas stations (SPBU) and the number of SPKLU is a major obstacle for people to choose electric cars as their daily vehicles. 
                    For comparison, there are 5518 gas stations in Indonesia, far surpassing the number of SPKLU, which is only 184 spread across certain islands. 
                    The distribution of SPKLU in Indonesia can be seen in the graph below.
                    </div>''', unsafe_allow_html=True)
    st.markdown(' ')
    st.markdown(' ')

    col9, col10 = st.columns([6.5, 3.5], gap="medium")
    with col9:
        if language == 'English':
            st.markdown('''<div style="text-align: center;">
                        Map of Electric Stations Distribution in Indonesia (source: kompasiana)
                        </div>''', unsafe_allow_html=True)
        else:
            st.markdown('''<div style="text-align: center;">
                        Peta Persebaran Stasiun Elektrik di Indonesia (sumberdata: kompasiana)
                        </div>''', unsafe_allow_html=True)
        st.image(load_image('resource/SPKLU-Transparent.png'), use_column_width=True)
        
    with col10:
        if language == 'English':
            st.markdown('''<div style="text-align: justify;">
                        From the distribution map of SPKLU beside, it can be seen that SPKLU in Indonesia is still concentrated only on the island of Java, while the regions of Kalimantan and Papua do not have any charging stations at all. This is certainly a challenge for both the government and electric car companies so that electric cars can be accessible to people throughout Indonesia.
                        </div>''', unsafe_allow_html=True)
        else:
            st.markdown('''<div style="text-align: justify;">
                        Dari grafik penyebaran SPKLU disamping, dapat dilihat bahwa SPKLU di Indonesia masih berpusat di Pulau Jawa saja, sementara itu daerah Kalimantan dan Papua masih belum
                        terdapat stasiun pengisian sama sekali. Hal ini tentunya menjadi tantangan baik bagi pemerintah maupun perusahaan mobil listrik agar mobil listrik dapat dijangkau masyarakat
                        di seluruh Indonesia.
                        </div>''', unsafe_allow_html=True)
    st.write("---")
    

#Bagian 4 : Kesimpulan
if page == "📄 Conclusion":
    st.subheader("Kesimpulan" if language == 'Indonesian' else "Conclusion")
    st.image(load_image('resource/Image.webp'), use_column_width=True)
    if language == 'Indonesian':
        st.markdown('''<div style="text-align: justify;">
                    Dari beberapa perbandingan diatas, kita dapat menyimpulkan bahwa banyak perbedaan antara mobil listrik dengan mobil berbahan bakar minyak. Indonesia sendiri masih belum siap jika terdapat peralihan besar-besaran 
                    mobil bbm ke mobil listrik. Tantangan utama dari peralihan tersebut yaitu harga dan fasilitas pengisian masih terus dimimalkan pemerintah dan perusahaan mobil listrik melalui investasi dan pembangunan pabrik lokal serta pihak PLN yang membuka kerjasama dengan swasta 
                    untuk perluasan SPKLU. Sangat diharapkan untuk pemerintah untuk mendukung program tersebut baik dari regulasi maupun investasi untuk mempercepat program peralihan mobil listrik tersebut demi Indonesia
                    yang lebih baik.
                    </div>''', unsafe_allow_html=True)
    else:
        st.markdown('''<div style="text-align: justify;">
                    From the comparisons above, we can conclude that there are many differences between electric cars and fuel-powered cars. Indonesia itself is not yet ready for a large-scale transition 
                    from fuel-powered cars to electric cars. The main challenges of this transition, namely price and charging facilities, are continuously being minimized by the government and electric car companies through investments and the construction of local factories, as well as PLN opening cooperation with the private sector 
                    for the expansion of charging stations (SPKLU). It is highly expected that the government will support this program both from regulations and investments to accelerate the electric car transition program for a better Indonesia.
                    </div>''', unsafe_allow_html=True)
    st.write("")
