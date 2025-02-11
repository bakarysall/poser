import pandas as pd
import streamlit as st
import os

# ---- TITRE ----
st.markdown("<h1 style='text-align: center; color: black;'>MY DATA APP</h1>", unsafe_allow_html=True)

st.markdown("""
This app allows you to analyze data from a single CSV file.  
* **Python libraries:** pandas, streamlit, matplotlib, seaborn  
* **Data source:** [CoinAfrique](https://sn.coinafrique.com/)
""")

# ---- CHARGER LES DONNÉES ----
@st.cache_data(show_spinner=False)  # Désactivation du spinner pour éviter certains bugs
def load_data():
    base_path = "C:/Users/MICROSOFT/Desktop/fatima"
    files = {
        "Chaussures Enfant": os.path.join(base_path, "Chauss_enfant.csv"),
        "Chaussures Homme": os.path.join(base_path, "chaussure_homme.csv"),
        "Vêtements Enfant": os.path.join(base_path, "vetement_enfant.csv"),
        "Vêtements Homme": os.path.join(base_path, "Vet_homme.csv"),
    }
    dataframes = {}
    for name, path in files.items():
        st.write(f"Vérification du fichier : {path}")  # Debug
        if os.path.exists(path):
            try:
                dataframes[name] = pd.read_csv(path, encoding='ISO-8859-1')
            except Exception as e:
                st.error(f"Erreur lors du chargement du fichier {name}: {e}")
                dataframes[name] = pd.DataFrame()
        else:
            st.error(f"⚠️ Fichier introuvable : {path}")
            dataframes[name] = pd.DataFrame()
    return dataframes

data = load_data()

# ---- CHOISIR UN FICHIER À AFFICHER ----
selected_data = st.selectbox("Sélectionnez un dataset :", list(data.keys()))
df = data[selected_data]

# ---- Vérification si le dataframe est vide ----
if df.empty:
    st.warning(f"Aucune donnée disponible pour {selected_data}. Veuillez choisir un autre fichier.")
    st.stop()

# ---- AFFICHER LES DONNÉES ----
st.subheader(f"📊 Aperçu des données : {selected_data}")
st.write(f"Dimensions : {df.shape[0]} lignes, {df.shape[1]} colonnes")
st.dataframe(df)

# ---- GRAPHIQUES (TEMPORAIREMENT COMMENTÉS POUR TEST) ----
# if df.shape[1] >= 6:
#     col5 = df.columns[4]
#     col6 = df.columns[5]
    
#     st.subheader(f"📊 Relation entre {col5} et {col6}")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.scatterplot(data=df, x=col5, y=col6, ax=ax, color='blue')
#     ax.set_xlabel(col5)
#     ax.set_ylabel(col6)
#     ax.set_title(f"Relation entre {col5} et {col6}")
#     st.pyplot(fig)

# if "type_chaussure" in df.columns and "price" in df.columns:
    
#     st.subheader("📊 Distribution des prix par type de chaussure")
#     fig1, ax1 = plt.subplots(figsize=(10, 6))
#     sns.boxplot(data=df, x="type_chaussure", y="price", palette="magma", ax=ax1)
#     ax1.set_title("Distribution des prix par type de chaussure")
#     ax1.set_xlabel("Type de chaussure")
#     ax1.set_ylabel("Prix (FCFA)")
#     plt.xticks(rotation=45)
#     st.pyplot(fig1)

#     st.subheader("📊 Prix moyen par type de chaussure")
#     fig2, ax2 = plt.subplots(figsize=(10, 6))
#     df_grouped = df.groupby("type_chaussure")["price"].mean().reset_index()
#     sns.barplot(data=df_grouped, x="type_chaussure", y="price", palette="coolwarm", ax=ax2)
#     ax2.set_title("Prix moyen par type de chaussure")
#     ax2.set_xlabel("Type de chaussure")
#     ax2.set_ylabel("Prix moyen (FCFA)")
#     plt.xticks(rotation=45)
#     st.pyplot(fig2)
# else:
#     st.warning("Les colonnes 'type_chaussure' et 'price' sont absentes des données sélectionnées.")