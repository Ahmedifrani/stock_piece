
import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Recherche de pièces", page_icon="🔍")

# Titre de l'application
st.title("🔍 Recherche de pièces dans le stock")

# Charger le fichier Excel
fichier = "DatabaseParts.xlsx"

try:
    # Lire le fichier et la feuille "Reference"
    reference_df = pd.read_excel(fichier, sheet_name="Reference")
    
    # Nettoyer la colonne "Reference"
    reference_df["Reference"] = reference_df["Reference"].astype(str).str.strip().str.upper()

    # Filtrer les pièces disponibles
    stock_disponible = reference_df[
        reference_df["Quantite"].notna() & (reference_df["Quantite"] > 0)
    ].sort_values(by="Quantite", ascending=False)

    # Colonnes à afficher
    colonnes_a_afficher = ["Reference", "Type", "Designation", "Couleur", "Position", "Quantite"]

    # Afficher le nombre total de pièces
    st.info(f"📦 Nombre total de pièces disponibles : {stock_disponible.shape[0]}")

    # Formulaire visuel
    with st.form("formulaire_recherche"):
        st.subheader("🔎 Formulaire de recherche")
        reference_input = st.text_input("Entre la référence de la pièce à rechercher :").strip().upper()
        submit_button = st.form_submit_button("Rechercher")

    # Si l'utilisateur a cliqué sur "Rechercher"
    if submit_button:
        if reference_input:
            resultat = stock_disponible[stock_disponible["Reference"] == reference_input]

            if not resultat.empty:
                st.success("✅ Pièce trouvée :")
                st.dataframe(resultat[colonnes_a_afficher], use_container_width=True)
            else:
                st.error("❌ Référence non trouvée dans le stock.")
        else:
            st.warning("⚠️ Merci de saisir une référence avant de cliquer sur Rechercher.")

    # Affichage du tableau complet dans un volet déroulant
    with st.expander("📋 Voir la liste complète des pièces disponibles"):
        st.dataframe(stock_disponible[colonnes_a_afficher], use_container_width=True)

except FileNotFoundError:
    st.error("❌ Le fichier 'DatabaseParts.xlsx' est introuvable. Vérifie qu'il est bien dans le même dossier que ce script.")
except Exception as e:
    st.error(f"❌ Une erreur est survenue : {e}")
