import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ---- TITRE ----
st.markdown("<h1 style='text-align: center; color: black;'>MY DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app allows you to analyze data from a single CSV file.  
* **Python libraries:** pandas, streamlit, matplotlib, seaborn  
* **Data source:** [CoinAfrique](https://sn.coinafrique.com/)
""")

# ---- CHARGER LES DONNÉES ----
@st.cache_data
def load_data():
    # Chemins relatifs vers les fichiers CSV
    files = {
        "Chaussures Enfant": "data/Chauss_enfant.csv",
        "Chaussures Homme": "data/chaussure_homme.csv",
        "Vêtements Enfant": "data/vetement_enfant.csv",
        "Vêtements Homme": "data/Vet_homme.csv",
    }

    dataframes = {}
    for name, path in files.items():
        try:
            dataframes[name] = pd.read_csv(path, encoding='ISO-8859-1')
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier {name}: {e}")
            dataframes[name] = pd.DataFrame()
    return dataframes

data = load_data()

# ---- CHOISIR UN FICHIER À AFFICHER ----
selected_data = st.selectbox("Sélectionnez un dataset :", list(data.keys()))
df = data[selected_data]

# ---- AFFICHER LES DONNÉES ----
st.subheader(f"📊 Aperçu des données : {selected_data}")
st.write(f"Dimensions : {df.shape[0]} lignes, {df.shape[1]} colonnes")
st.dataframe(df)

if df.shape[1] >= 6:
    col5 = df.columns[4]
    col6 = df.columns[5]
    
    # ---- GRAPHIQUE ENTRE 5ÈME ET 6ÈME COLONNE ----
    st.subheader(f"📊 Relation entre {col5} et {col6}")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x=col5, y=col6, ax=ax, color='blue')
    ax.set_xlabel(col5)
    ax.set_ylabel(col6)
    ax.set_title(f"Relation entre {col5} et {col6}")
    st.pyplot(fig)

# ---- GRAPHIQUES ----
st.subheader("📈 Visualisations")

if "type_chaussure" in df.columns and "price" in df.columns:
    
    # ---- GRAPHIQUE 1 : Distribution des prix par type de chaussure ----
    st.subheader("📊 Distribution des prix par type de chaussure")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="type_chaussure", y="price", palette="magma", ax=ax1)
    ax1.set_title("Distribution des prix par type de chaussure")
    ax1.set_xlabel("Type de chaussure")
    ax1.set_ylabel("Prix (FCFA)")
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    # ---- GRAPHIQUE 2 : Prix moyen par type de chaussure ----
    st.subheader("📊 Prix moyen par type de chaussure")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    df_grouped = df.groupby("type_chaussure")["price"].mean().reset_index()
    sns.barplot(data=df_grouped, x="type_chaussure", y="price", palette="coolwarm", ax=ax2)
    ax2.set_title("Prix moyen par type de chaussure")
    ax2.set_xlabel("Type de chaussure")
    ax2.set_ylabel("Prix moyen (FCFA)")
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.warning("Les colonnes 'type_chaussure' et 'price' sont absentes des données sélectionnées.")