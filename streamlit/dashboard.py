import streamlit as st
import squarify
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from streamlit_option_menu import option_menu

champions = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/champions.csv", index_col=0)
city_most_order_40 = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/city_most_order_40.csv", index_col=0)
city_most_order = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/city_most_order.csv", index_col=0)
top_frequency = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/top_frequency.csv", index_col=0)
top_monetary = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/top_monetary.csv", index_col=0)
top_product_most_buy = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/top_product_most_buy.csv", index_col=0)
top_recency = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/top_recency.csv", index_col=0)
rfm = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/rfm.csv", index_col=0)
product_most_buy = pd.read_csv("~/Dicoding/analisis-data-dicoding/submission-analisis-data/datasets/finals/product_most_buy.csv", index_col=0)


# Sidebar navigation
with st.sidebar:
    selected = option_menu("E-Commerce Analysis", ["Exploratory Data Analysis (EDA)", "RFM Analysis"], 
                           icons=['house', 'bar-chart', 'graph-up'], menu_icon="cast", default_index=0)

if selected == 'Exploratory Data Analysis (EDA)':
    # Pertanyaan 1
    st.title("Pertanyaan 1")
    st.text("Kota dengan pembelian terbesar dan berhasil menyumbang 40% total transaksi (berdasarkan harga barang yang terjual).")

    ## Preprocessing
    city_most_order['cumulative_sum'] = city_most_order['price'].cumsum() # Baris ini akan menghasilkan nilai kumulatif dari setiap price yang sudah dijumlahkan.
    total = city_most_order['price'].sum()
    city_most_order['cumcut'] = city_most_order['cumulative_sum']/total  # Baris ini akan menghasilkan setiap kotanya memberikan nilai kontribusinya seberapa besar (kumulatif tiap baris)

    city_most_order_40 = city_most_order[city_most_order['cumcut'] <= 0.4]
    city_most_order_40["label"] = city_most_order_40['customer_city'] + "\nUSD:" + city_most_order_40['price'].astype(str)

    ## Visualization
    ### Top City
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Kote Dengan Penjualan Terbesar", value=f"Sao Paulo: {city_most_order_40['price'].max()}")
    with col2: 
        st.metric("Kota Dengan Penjualan Terendah", value=f"polo petroquimico: {city_most_order['price'].min()}")

    ### Treemap
    fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(sizes=city_most_order_40.price, label=city_most_order_40.label, color=sns.color_palette("pastel"), text_kwargs={'fontsize':7}, ax=ax)
    ax.axis('off')
    st.pyplot(fig)

    st.info("""
            Kesimpulan:
            
            Sao Paulo merupakan kota yang memiliki nilai barang yang terjual tertinggi mencapai 1949872 US Dollar.
            Hal ini menjadikan kota ini sebagai kota dengan sumbangsih terbesar pada total transaksi. Diikuti oleh Rio de Janeiro di peringkat kedua dengan total harga barang terjual mencapai 992850 US Dollar.
            """)
    
    # Pertanyaan 2
    st.title("Pertanyaan 2")
    st.text("Produk yang paling laris dibeli dari kota Sao Paulo dengan pembelian terbanyak dengan menyumbang 50% transaksi.")

    ## Visualization
    ### Top Product
    st.metric("Product Paling Banyak Dibeli", value=f"Beleza Saude: {top_product_most_buy['price'].max()} USD")
    st.metric("Product Paling Sedikit Dibeli", value=f"portateis_cozinha ...: {product_most_buy['price'].min()} USD")

    ### Visualisasi Treemap
    fig, ax = plt.subplots(figsize=(8, 6))
    squarify.plot(sizes=top_product_most_buy.price, label=top_product_most_buy.label, color=sns.color_palette("pastel"), text_kwargs={'fontsize':7}, pad=2, ax=ax)
    plt.axis('off')
    st.pyplot(fig)

    st.info("""
            Kesimpulan:

            Di kota Sao Paulo, kategori produk Beleza Saude, Cama Mesa Banho, dan Relogios Presentes merupakan urutan ketiga teratas yang berhasil terjual dan menjadi paling banyak dibeli.
            Ketiga barang tersebut memberikan kontribusi besar pada 70% transaksi yang terjadi di kota tersebut.
            """)

if selected == 'RFM Analysis':
    st.title("Customer Segmentation with RFM (Recency, Frequency, Monetary) Analysis")
    st.markdown("""
            **RFM** adalah metode segmentasi pelanggan berdasarkan tiga perilaku utama:

            - **Recency**: Seberapa baru pelanggan melakukan transaksi terakhir  
            - **Frequency**: Seberapa sering pelanggan melakukan transaksi dalam periode tertentu  
            - **Monetary**: Seberapa banyak uang yang dibelanjakan pelanggan
            """)
    
    st.markdown("""
                Setiap pelanggan akan diberikan scoring dari 1-5 untuk menentukan seberapa kuat RFM mereka masing-masing.
                Jika seorang pelanggan mendapatkan score **555**, menandakan bahwa pelanggan tersebut memiliki skor recency 5, frequency 5, dan monetary 5. 

                Berikut adalah visualisasi yang menggambarkan seberapa banyak score yang muncul di dataset e-commerce ini.
            """)
    
    # Visualisasi
    fig, ax = plt.subplots(figsize=(12,8))
    sns.countplot(data=rfm, x='RFM_score', order=rfm['RFM_score'].value_counts().index, ax=ax)
    plt.xticks(rotation=45)
    plt.title("Distribusi Pelanggan Berdasarkan RFM Score")
    st.pyplot(fig)

    st.info("""
            Kesimpulan:

            Dari visualisasi di atas, bisa disimpulkan bahwa score Recency 4, Frequency 2, dan Monetary 2 menempati posisi dengan customer terbanyak.
            Artinya, banyak customer yang dikategorikan loyal dengan e-commerce ini. 

            Bahkan, berbeda sedikit selisihnya dengan Recency 1, Frequency 5, dan Monetary 5 yang menempati posisi kedua.
            Segmentasi ini walaupun jarang membeli, tapi sekalinya membeli selalu dalam jumlah besar dan frekuensi yang banyak.
            """)

    st.markdown("""
            Untuk melihat tabel lebih lengkap setiap dataset (diambil top 50), dapat klik tab berikut.
            """)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Champions (Perfect RFM)", "Recency (R)", "Frequency (F)", "Monetary (M)"])
    with tab1:
        filtered_champions = champions.head(50)
        st.table(data=filtered_champions)
    with tab2:
        filtered_recency = top_recency.head(50)
        st.table(data=filtered_recency)
    with tab3: 
        filtered_frequency = top_frequency.head(50)
        st.table(data=filtered_frequency)
    with tab4:
        filtered_monetary = top_monetary.head(50)
        st.table(data=filtered_monetary)
    



