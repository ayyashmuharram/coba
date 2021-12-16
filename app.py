import pandas as pd #pip install pandas openpyxl
#import plotly.express as px
import streamlit as st #pip install streamlit
from PIL import Image
import json

st.set_page_config(page_title="Produksi Minyak",
                   page_icon="blackpink.png",
                   layout="wide")

#Main Page
st.title("Produksi Minyak Mentah")
st.markdown("*Mungkin eksekusi program membutuhkan waktu pemrosesan*")

#Logo BlackOil
image = Image.open('blackoil.png')
st.sidebar.image(image)

#Import file csv
df1 = pd.read_csv("produksi_minyak_mentah.csv")

file_json = open("kode_negara_lengkap.json")
data = json.loads(file_json.read())

list_hapus_baris=[]
#jumlahterhapus=0
urutan=0
for i in df1.loc():
    urutan2=0
    hapus=1
    for j in data:
        kode1=(df1.loc[urutan,"kode_negara"])
        kode2=data[urutan2]['alpha-2']
        kode3=data[urutan2]['alpha-3']
        #print("kode 1 adalah",kode1)
        #print("kode 2 adalah",kode2)
        #print("kode 3 adalah",kode3)
        if kode1==kode2 or kode1==kode3:
            df1.loc[urutan,"kode_negara"]=data[urutan2]['name']
            hapus=0
            #print('negara berubah menjadi',df1.loc[urutan,"kode_negara"])
        #print("ini adalah urutan kode negara",urutan,"dan urutan json",urutan2)
        urutan2=urutan2+1
    if hapus==1:
        #jumlahterhapus=jumlahterhapus+1
        #print(df1.index[urutan])
        list_hapus_baris.append(df1.index[urutan])
    urutan=urutan+1
    if urutan==5839:break

#print(list_hapus_baris)
df=df1.drop(df1.index[list_hapus_baris[0:]])

#sidebar
st.sidebar.header("Pilihan" )
st.sidebar.subheader("Silahkan pilih statistik negara yang ingin ditampilkan ataupun statistik tahun yang ingin ditampilkan")
st.sidebar.subheader("Apabila ingin secara cepat menghapus untuk memilih negara tertentu klik lingkaran dengan tanda 'x' di kanan tengah pilihan")
negara = st.sidebar.multiselect(
    "Pilih Negara:",
    options=df["kode_negara"].unique(),
    default=df["kode_negara"].unique()
)

tahun = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=df["tahun"].unique(),
    default=df["tahun"].unique()
)

df_selection = df.query(
    "kode_negara == @negara & tahun == @tahun"
)

#st.dataframe(df_selection)

#Produksi Minyak Berdasarkan Tahun
produksi_berdasarkan_tahun = (
    df_selection.groupby(by=["tahun"]).sum()[["produksi"]].sort_values(by="produksi")
)
fig_produksi_tahun = px.bar(
    produksi_berdasarkan_tahun,
    x=produksi_berdasarkan_tahun.index,
    y="produksi",
    title="<b>Total Produksi Minyak berdasarkan Tahun</b>",
    color_discrete_sequence=["#ff94e0"] * len(produksi_berdasarkan_tahun),
    template="plotly_white",
)
fig_produksi_tahun.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_produksi_tahun)

#Production by country (Bar Chart)
produksi_berdasarkan_negara = (
    df_selection.groupby(by=["kode_negara"]).sum()[["produksi"]].sort_values(by="produksi")     
)
fig_produksi_negara = px.bar(
    produksi_berdasarkan_negara,
    x="produksi",
    y=produksi_berdasarkan_negara.index,
    orientation="h",
    title="<b>Total Produksi Minyak berdasarkan Negara</b>",
    color_discrete_sequence=["#ff59c7"] * len(produksi_berdasarkan_negara),
    template="plotly_white",
)

fig_produksi_negara.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_produksi_negara)

#left_column, right_column = st.columns(2)
#left_column.plotly_chart(fig_produksi_tahun, use_container_width=True)
#right_column.plotly_chart(fig_produksi_negara, use_container_width=True)

#Total Produksi
total_produksi = int(df_selection["produksi"].sum())
#average_rating = round(df_selection["Rating"].mean(),1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Produksi")
    st.subheader(f" {total_produksi:,}")


#hide streamlit style
hide_st_style = """
            <style>
            #MainMenu {Visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("Informasi tentang negara tersebut")

for y in produksi_berdasarkan_negara:
    st.markdown(y)


 


