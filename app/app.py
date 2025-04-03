# dashboard.py
import streamlit as st
import pandas as pd
from graph import *
import os
import sys
import altair as alt
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Véhicules électriques",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")

st.markdown("""
<style>
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        background-color: rgba(50, 50, 50, 0.9);
        padding: 10px 0;
        text-align: center;
        transition: transform 0.3s;
        transform: translateY(100%);
    }

    .nav-container:hover {
        transform: translateY(0);
    }
    
    .nav-container label {
        color: white !important;
        font-size: 16px;
        }
    .element.style {
    position: relative;
    width: 261.333px;
    height: 450px;
    
    .stButton>button {
    background-color: #9fa8da; 
    color: #9fa8da;
    border-radius: 8px;
    }
</style>
""",unsafe_allow_html=True) 

with st.container():
    st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
    
    page = st.radio(
        "",
        ["🏁 Présentation du projet", "🚗 Voitures électriques", "🔌Bornes de recharge", "🛣️TMJA", "⚡Vehicules par borne","📈 Objectifs 2030"],
        horizontal=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

if page == "🏁 Présentation du projet":
    st.title("🔋Dashboard voitures électriques")

    st.markdown("""
    <style>
    .presentation-texte, .themes-liste {
        font-size: 20px;
        line-height: 1.8;
        color: white;
        text-align: justify;
        margin-top: 10px;
    }
    .themes-liste {
        margin-left: 20px;
    }
    .credits {
        margin-top: 40px;
        font-size: 16px;
        color: #999999;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])  # texte à gauche uniquement

    with col1:
        st.markdown("### 🌍 Contexte")

        st.markdown("""
        <div class="presentation-texte">
            Ce projet a été réalisé dans le cadre de la saison 3 du défi <strong>Open Data University</strong>, qui vise à valoriser les données ouvertes à travers la création de dashboards interactifs et accessibles.<br><br>
            Ce tableau de bord offre une vue d’ensemble de l’évolution du parc de véhicules électriques et des infrastructures de recharge en France sur plusieurs années. Cet état des lieux permet d’évaluer l’écart entre la situation actuelle et les objectifs fixés pour 2030, afin de questionner leur faisabilité et la trajectoire à suivre.
            <br><br>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🔍 Thématiques abordées")
        st.markdown("""
        <div class="themes-liste">
        - 🚗 <strong>Véhicules électriques</strong><br>
        - 🔌 <strong>Bornes de recharge</strong><br>
        - 🛣️ <strong>TMJA (Trafic Moyen Journalier Annuel)</strong><br>
        - ⚡ <strong>Analyse croisée véhicules / bornes de recharge</strong><br>
        - 📈 <strong>Objectifs gouvernementaux à l'horizon 2030</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="credits" style="text-align: center; margin-top: 60px;">
            Projet réalisé par <strong>Jawad Gherras</strong>, <strong>Gabriel Edinger</strong> et <strong>Romain Siette</strong>.
        </div>
        """, unsafe_allow_html=True)
        
        with col2:
            st.image("image_voiture-removebg.png", width=900)

elif page == "🚗 Voitures électriques":
    st.title("🚗 Voitures électriques")
    annees = sorted(df['Annee'].unique())
    regions = sorted(df['region'].dropna().unique())
    departements = sorted(df['departement'].dropna().unique())
    
    # Barre de sélection en haut
    col_top1, col_top2, col_top3 = st.columns(3)
    st.markdown("""
        <style>
        /* Texte et track du slider */
        .stSlider > div[data-baseweb="slider"] > div {
            color: white !important; /* Couleur du texte */
        }

        /* Barre active du slider */
        .stSlider > div[data-baseweb="slider"] > div > div {
            background: #7e57c2 !important; /* Couleur de la barre */
        }

        /* Curseur (le bouton rond) */
        .stSlider [role="slider"] {
            background-color: #9575cd  !important;  /* Couleur du curseur */
            border: 2px solid white;               /* Contour blanc */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
    with col_top1:
        annee_selectionnee = annee_selectionnee = st.slider(
            "📅 Choisissez une année d'analyse",
            min_value=2020,
            max_value=2024,
            value=2022,
            step=1
        )
    with col_top2:
        region_selectionnee = st.selectbox("Sélectionnez la région", regions, key='reg')
        
    departements_filtrés = sorted(df[df['region'] == region_selectionnee]['departement'].unique())

    with col_top3:
        departement_selectionne = st.selectbox("Sélectionnez le département", departements_filtrés, key='dep')

    # Conteneur principal pour la mise en page dynamique
    placeholder = st.empty()

    with placeholder.container():
        kpi_fr,kpi_reg,kpi_dep = st.columns(3)
        
        
        with kpi_fr:
            fig_fr = graphique_interactif_france(df, annee_selectionnee)
            if fig_fr:
                st.plotly_chart(fig_fr)
            else:
                st.warning("Pas de données disponibles pour la France.")
        
        with kpi_reg:
            fig_reg = graphique_interactif_region(df, annee_selectionnee, region_selectionnee)
            if fig_reg:
                st.plotly_chart(fig_reg)
            else:
                st.warning("Pas de données disponibles pour la région sélectionnée.")       
        
        with kpi_dep:
            fig_dep = graphique_interactif_dep(df, annee_selectionnee, departement_selectionne)
            if fig_dep:
                st.plotly_chart(fig_dep)
            else:
                st.warning("Pas de données disponibles pour le département sélectionné.")
                
                st.markdown("""
        <style>
        /* Texte et track du slider */
        .stSlider > div[data-baseweb="slider"] > div {
            color: white !important; /* Couleur du texte */
        }

        /* Barre active du slider */
        .stSlider > div[data-baseweb="slider"] > div > div {
            background: #7e57c2 !important; /* Couleur de la barre */
        }

        /* Curseur (le bouton rond) */
        .stSlider [role="slider"] {
            background-color: #9575cd  !important;  /* Couleur du curseur */
            border: 2px solid white;               /* Contour blanc */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
                
        current_dir = os.path.dirname(__file__)
        cartes_dir = os.path.join(current_dir, "..", "Cartes", "cartes_ve")

        carte_dep_path = os.path.join(cartes_dir, f"carte_dep_nbVE{annee_selectionnee}.html")
        carte_reg_path = os.path.join(cartes_dir, f"carte_reg_nbVE{annee_selectionnee}.html")
        
        col_map_reg_ve, col_map_dep_ve = st.columns(2)
        with col_map_reg_ve:
            
            st.markdown(f"### Carte des régions - {annee_selectionnee}")
            with open(carte_reg_path, 'r', encoding='utf-8') as f:
                    carte_reg_ve_html = f.read()
                    components.html(carte_reg_ve_html, height=450, width=500)
        with col_map_dep_ve:
            st.markdown(f"### Carte des départements - {annee_selectionnee}")
            with open(carte_dep_path, 'r', encoding='utf-8') as f:
                carte_dep_ve_html = f.read()
                components.html(carte_dep_ve_html, height=450, width=500)
        
        
        col_but_ve1, col_but_ve2, col_but_ve3 = st.columns(3)
        with col_but_ve2:
            st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
            choix_graphe = st.radio(
                "📈 Sélectionnez la zone d'analyse :",
                ["France", "Région", "Département"],
                horizontal=True
            )
        
        fig_col1, fig_col2 = st.columns(2)        
        with fig_col1:
            # Affichage conditionnel du graphique
            if choix_graphe == "France":
                fig = graphique_evolution_france_ve(df)
                st.plotly_chart(fig, use_container_width=True, key="evol_france_ve")

            elif choix_graphe == "Région":
                fig = graphique_evolution_ve_region(df, region_selectionnee)
                st.plotly_chart(fig, use_container_width=True, key="evol_reg_ve")

            elif choix_graphe == "Département":
                fig = graphique_evolution_ve_departement(df, departement_selectionne)
                st.plotly_chart(fig, use_container_width=True, key="evol_dep_ve")
        
        with fig_col2:
            if choix_graphe == "France":
                valeur = "France"
            elif choix_graphe == "Région":
                valeur = region_selectionnee
            elif choix_graphe == "Département":
                valeur = departement_selectionne

            # Appel de la fonction camembert
            fig_camembert = camembert_repartition_motorisation(df, annee_selectionnee, choix_graphe, valeur)

            if fig_camembert:
                st.plotly_chart(fig_camembert)
            else:
                st.warning("Aucune donnée disponible pour cette sélection.")
                
        st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
    choix_classement = st.radio("Afficher les régions et départements par :", ["Top 10", "Bottom 10"], horizontal=True)

    col_regions, col_departements = st.columns(2)

    with col_regions:
        if choix_classement == "Top 10":
            fig_regions = barplot_top_regions_ve(df, annee_selectionnee)
        else:
            fig_regions = barplot_bottom_regions_ve(df, annee_selectionnee)

        st.plotly_chart(fig_regions, use_container_width=True, key = "barplot_regions_ve")

    # Graphiques départements (colonne droite)
    with col_departements:
        if choix_classement == "Top 10":
            fig_departements = barplot_top_departements_ve(df, annee_selectionnee)
        else:
            fig_departements = barplot_bottom_departements_ve(df, annee_selectionnee)

        st.plotly_chart(fig_departements, use_container_width=True, key = "barplot_departements_ve")

elif page == "🔌Bornes de recharge":
    st.title("🔌Bornes de Recharge")
    annees_bornes = sorted(df_2['Annee'].unique())
    regions_bornes = sorted(df_2['nom_region'].dropna().unique())
    departements_bornes = sorted(df_2['nom_departement'].dropna().unique())
    st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
    onglet = st.radio(
        "Choisissez une vue :",
        ["🔌Bornes de recharge", "🛠️Installation des bornes de recharge"],
        horizontal=True
    )
    if onglet == "🔌Bornes de recharge":
        col_b_1, col_b_2, col_b_3 = st.columns(3)
        
        with col_b_1:
            st.markdown("""
        <style>
        /* Texte et track du slider */
        .stSlider > div[data-baseweb="slider"] > div {
            color: white !important; /* Couleur du texte */
        }

        /* Barre active du slider */
        .stSlider > div[data-baseweb="slider"] > div > div {
            background: #7e57c2 !important; /* Couleur de la barre */
        }

        /* Curseur (le bouton rond) */
        .stSlider [role="slider"] {
            background-color: #9575cd  !important;  /* Couleur du curseur */
            border: 2px solid white;               /* Contour blanc */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
            annee_selectionnee_b_1 = annee_selectionnee = st.slider(
                "📅 Choisissez une année d'analyse",
                min_value=2010,
                max_value=2025,
                value=2022,
                step=1
            )
        with col_b_2:
            region_selectionnee_b_1 = st.selectbox("Sélectionnez la région", regions_bornes, key='reg_b')
            departements_filtrés = sorted(df_2[df_2['nom_region'] == region_selectionnee_b_1]['nom_departement'].unique())
        with col_b_3:
            departement_selectionne_b_1 = st.selectbox("Sélectionnez le département", departements_filtrés, key='dep_b')
               
        placeholder = st.empty()
        
        with placeholder.container():
            kpi_france_b, kpi_b_reg, kpi_b_dep = st.columns(3)
    
        with kpi_france_b:
            fig_fr_2 = graphique_interactif_france_b(df_2, annee_selectionnee_b_1)  
            if fig_fr_2:
                st.plotly_chart(fig_fr_2)
            else:
                st.warning("Pas de données disponibles pour la France.")

        with kpi_b_reg:
            if region_selectionnee_b_1 in df_2['nom_region'].values:
                fig_reg_2 = graphique_bornes_region_1(df_2 ,region_selectionnee_b_1,annee_selectionnee_b_1)  # Suppression de l'année
            else:
                fig_reg_2 = None

            if fig_reg_2:
                st.plotly_chart(fig_reg_2)
            else:
                st.warning("Pas de données disponibles pour la région sélectionnée.")

        with kpi_b_dep:
            if departement_selectionne_b_1 in df_2['nom_departement'].values:
                fig_dep_2 = graphique_bornes_dep_1(df_2,departement_selectionne_b_1,annee_selectionnee_b_1)  # Suppression de l'année
            else:
                fig_dep_2 = None

            if fig_dep_2:
                st.plotly_chart(fig_dep_2)
            else:
                st.warning("Pas de données disponibles pour le département sélectionné.")
                
        map_col1, map_col2, map_col3 = st.columns(3)
        st.markdown("""
        <style>
        /* Texte et track du slider */
        .stSlider > div[data-baseweb="slider"] > div {
            color: white !important; /* Couleur du texte */
        }

        /* Barre active du slider */
        .stSlider > div[data-baseweb="slider"] > div > div {
            background: #7e57c2 !important; /* Couleur de la barre */
        }

        /* Curseur (le bouton rond) */
        .stSlider [role="slider"] {
            background-color: #9575cd  !important;  /* Couleur du curseur */
            border: 2px solid white;               /* Contour blanc */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
        with map_col2:
                annee_selectionnee = st.slider(
                "📅 Choisissez une année d'analyse",
                min_value=2020,
                max_value=2024,
                value=2022,
                step=1
            )
        current_dir = os.path.dirname(__file__)
        cartes_dir = os.path.join(current_dir, "..", "Cartes", "Répartitions des bornes")

        carte_dep_path = os.path.join(cartes_dir, f"carte_dep_bornes_{annee_selectionnee}.html")
        carte_reg_path = os.path.join(cartes_dir, f"carte_reg_bornes_{annee_selectionnee}.html")
        
        col_map_reg, col_map_dep = st.columns(2)
        with col_map_reg:
            
            st.markdown(f"### Carte des régions - {annee_selectionnee}")
            with open(carte_reg_path, 'r', encoding='utf-8') as f:
                    carte_reg_html = f.read()
                    components.html(carte_reg_html, height=450, width=500)
        with col_map_dep:
            st.markdown(f"### Carte des départements - {annee_selectionnee}")
            with open(carte_dep_path, 'r', encoding='utf-8') as f:
                carte_dep_html = f.read()
                components.html(carte_dep_html, height=450, width=500)
        
        col_button1, col_button2, col_button3 = st.columns(3)
        with col_button2:
            st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
            choix_classement = st.radio("", ["Top 10", "Bottom 10"], horizontal=True)
         
        col_choix1, col_choix2 = st.columns(2)   
        with col_choix1: 
            fig_regions = barplot_bornes_regions_tot(df_2, choix_classement, annee_selectionnee_b_1)
            st.plotly_chart(fig_regions, use_container_width=True, key="barplot_regions_tot")           

        with col_choix2:
            fig_departements = barplot_bornes_departements_tot(df_2, choix_classement, annee_selectionnee_b_1)
            st.plotly_chart(fig_departements, use_container_width=True, key="barplot_departements_tot")
            
        
            # Colonnes pour régions et départements
        col_regions, col_departements = st.columns(2)
        
        with col_regions:
            df_reg_evol = df_2[(df_2['nom_region'] == region_selectionnee_b_1) & (df_2['Annee'] >= 2010)].groupby('Annee')['nb_borne'].sum().reset_index()
            df_reg_evol['nb_borne'] = df_reg_evol['nb_borne'].cumsum() 
            fig_reg_evol = go.Figure()
            fig_reg_evol.add_trace(go.Scatter(x=df_reg_evol['Annee'], y=df_reg_evol['nb_borne'], mode='lines+markers',line=dict(color='#9575cd ')))
            fig_reg_evol.update_layout(xaxis_title="", yaxis_title="Nombre de bornes" ,title={
                    'text': f"Évolution du nombre bornes pour {region_selectionnee_b_1}",
                    'font': {'size': 15}  
                })
            st.plotly_chart(fig_reg_evol, key="evol_reg_tot")

        with col_departements:
            df_dep_evol = df_2[(df_2['nom_departement'] == departement_selectionne_b_1) & (df_2['Annee'] >= 2010)].groupby('Annee')['nb_borne'].sum().reset_index()
            df_dep_evol['nb_borne'] = df_dep_evol['nb_borne'].cumsum()  
            fig_dep_evol = go.Figure()
            fig_dep_evol.add_trace(go.Scatter(x=df_dep_evol['Annee'], y=df_dep_evol['nb_borne'], mode='lines+markers',line=dict(color='#9575cd ')))
            fig_dep_evol.update_layout(xaxis_title="", yaxis_title="Nombre de bornes" ,title={
                    'text': f"Évolution du nombre bornes pour {departement_selectionne_b_1}",
                    'font': {'size': 15}  
                })
            
            st.plotly_chart(fig_dep_evol, key="evol_dep_tot")
            
            st.markdown('### Répartition des bornes de recharge en France')
            carte_html_path = os.path.join(current_dir, "..", "Cartes", "carte_de_France_bornes_VE_cluster_filtree.html")

            with open(carte_html_path, 'r', encoding='utf-8') as f:
                    carte_html = f.read()

            components.html(carte_html,height=500)
        
            
        
    elif onglet == "🛠️Installation des bornes de recharge":
        col_b_1, col_b_2, col_b_3 = st.columns(3)
        st.markdown("""
        <style>
        /* Texte et track du slider */
        .stSlider > div[data-baseweb="slider"] > div {
            color: white !important; /* Couleur du texte */
        }

        /* Barre active du slider */
        .stSlider > div[data-baseweb="slider"] > div > div {
            background: #7e57c2 !important; /* Couleur de la barre */
        }

        /* Curseur (le bouton rond) */
        .stSlider [role="slider"] {
            background-color: #9575cd  !important;  /* Couleur du curseur */
            border: 2px solid white;               /* Contour blanc */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)
        with col_b_1:
            annee_selectionnee_b = st.slider(
            "📅 Choisissez une année d'analyse",
            min_value=2010,
            max_value=2025,
            value=2022,
            step=1
        )

        with col_b_2:
            region_selectionnee_b = st.selectbox("Sélectionnez la région", regions_bornes, key='reg_b')
        departements_filtrés = sorted(df_2[df_2['nom_region'] == region_selectionnee_b]['nom_departement'].unique())
        with col_b_3:
            departement_selectionne_b = st.selectbox("Sélectionnez le département", departements_filtrés, key='dep_b')
        
        placeholder = st.empty()

        with placeholder.container():
            kpi_france_b,kpi_b_reg, kpi_b_dep = st.columns(3)
            
            with kpi_france_b:
                if annee_selectionnee_b in df_2['Annee'].values:
                    fig_fr_2 = vignette_borne_instal_fr(df_2, annee_selectionnee_b)
                else:
                    fig_fr_2 = None 
                
                if fig_fr_2:
                    st.plotly_chart(fig_fr_2, key="vignette_fr_instal")
                else:
                    st.warning("Pas de données disponibles pour la France.")
            
            
            with kpi_b_reg:
                if annee_selectionnee_b in df_2['Annee'].values and region_selectionnee_b in df_2['nom_region'].values:
                    fig_reg_2 = vignette_borne_instal_reg(df_2,region_selectionnee_b, annee_selectionnee_b)
                else:
                    fig_reg_2 = None
                if fig_reg_2:
                    st.plotly_chart(fig_reg_2, key="vignette_reg_instal")
                else:
                    st.warning("Pas de données disponibles pour la région sélectionnée.")

            with kpi_b_dep:
                if annee_selectionnee_b in df_2['Annee'].values and departement_selectionne_b in df_2['nom_departement'].values:
                    fig_dep_2 = graphique_bornes_dep(df_2, departement_selectionne_b, annee_selectionnee_b)
                else:
                    fig_dep_2 = None
                if fig_dep_2:
                    st.plotly_chart(fig_dep_2, key="vignette_dep_instal")
                else:
                    st.warning("Pas de données disponibles pour le département sélectionné.")
            
                
            fig_col1, fig_col2, fig_col3 = st.columns(3)
            
            with fig_col1:
                fig_france_evol = graphique_evolution_france_b(df_2)
                st.plotly_chart(fig_france_evol)
            
            with fig_col2:
                #st.markdown("### Évolution des véhicules électriques par région")
                df_reg_evol = df_2[(df_2['nom_region'] == region_selectionnee_b) & (~df_2["Annee"].isin([2025, 1930,2002]))].groupby('Annee')['nb_borne'].sum().reset_index()
                fig_reg_evol = go.Figure()
                fig_reg_evol.add_trace(go.Scatter(x=df_reg_evol['Annee'], y=df_reg_evol['nb_borne'], mode='lines+markers',line=dict(color='#9575cd ')))
                fig_reg_evol.update_layout(xaxis_title="", yaxis_title="Nombre de bornes" ,title={
                        'text': f"Évolution des bornes installées pour {region_selectionnee_b}",
                        'font': {'size': 15}  # Diminuer la taille du titre
                    })
                st.plotly_chart(fig_reg_evol)
            with fig_col3:
                #st.markdown("### Évolution des véhicules électriques par département")
                df_dep_evol = df_2[(df_2['nom_departement'] == departement_selectionne_b)&(~df_2["Annee"].isin([2025, 1930, 2002]))].groupby('Annee')['nb_borne'].sum().reset_index()
                fig_dep_evol = go.Figure()
                fig_dep_evol.add_trace(go.Scatter(x=df_dep_evol['Annee'], y=df_dep_evol['nb_borne'], mode='lines+markers',line=dict(color='#9575cd ')))
                fig_dep_evol.update_layout(xaxis_title="", yaxis_title="Nombre de bornes" ,title={
                        'text': f"Évolution des bornes installées pour {departement_selectionne_b}",
                        'font': {'size': 15}  # Diminuer la taille du titre
                    })
                st.plotly_chart(fig_dep_evol, key="evol_dep_instal")
                st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
                
            choix_classement = st.radio("Classement bornes de recharge :", ["Top 10", "Bottom 10"], horizontal=True)

            # Colonnes pour régions et départements
            col_regions, col_departements = st.columns(2)

            with col_regions:
                fig_regions = barplot_bornes_regions(df_2, choix_classement, annee_selectionnee_b)
                st.plotly_chart(fig_regions, use_container_width=True, key="barplot_regions_instal")

            with col_departements:
                fig_departements = barplot_bornes_departements(df_2, choix_classement, annee_selectionnee_b)
                st.plotly_chart(fig_departements, use_container_width=True, key="barplot_departements_instal")

            
elif page == "🛣️TMJA":
    st.title("🛣️TMJA")
    regions_tmja = sorted(df_tmja_r['nom_region'].unique())
    departements_tmja = sorted(df_tmja_d['nom_departement'].unique())
    col_b_1, col_b_2 = st.columns(2)

    with col_b_1:
            region_selectionnee_tmja = st.selectbox("Sélectionnez la région", regions_tmja, key='reg_b')
            departements_filtrés = sorted(df_tmja_d[df_tmja_d['nom_region'] == region_selectionnee_tmja]['nom_departement'].unique())
    with col_b_2:
            departement_selectionne_tmja = st.selectbox("Sélectionnez le département", departements_filtrés, key='dep_tmja')
               
    placeholder = st.empty()
        
    with placeholder.container():
            kpi_france_tmja, kpi_tmja_reg, kpi_tmja_dep = st.columns(3)
    
    with kpi_france_tmja:
            fig_fr_2 = graphique_tmja_france(df_tmja_r)  
            if fig_fr_2:
                st.plotly_chart(fig_fr_2)
            else:
                st.warning("Pas de données disponibles pour la France.")

    with kpi_tmja_reg:
            if region_selectionnee_tmja in df_tmja_r['nom_region'].values:
                fig_reg_2 = graphique_tmja_region(df_tmja_r, region_selectionnee_tmja) 
            else:
                fig_reg_2 = None

            if fig_reg_2:
                st.plotly_chart(fig_reg_2)
            else:
                st.warning("Pas de données disponibles pour la région sélectionnée.")

    with kpi_tmja_dep:
            if departement_selectionne_tmja in df_tmja_d['nom_departement'].values:
                fig_dep_2 = graphique_tmja_dep(df_tmja_d, departement_selectionne_tmja)  # Suppression de l'année
            else:
                fig_dep_2 = None

            if fig_dep_2:
                st.plotly_chart(fig_dep_2)
            else:
                st.warning("Pas de données disponibles pour le département sélectionné.")
                
    map_col3, map_col4 = st.columns(2)

    with map_col3:
        st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
        niveau_carte = st.radio(
            "",
            ["Département", "Région"],
            horizontal=True)

    with map_col3:
        if niveau_carte == "Département":
            carte_html_path = os.path.join(current_dir, "..", "Cartes", "carte_dep_tmja.html")
        else:
            carte_html_path = os.path.join(current_dir, "..", "Cartes", "carte_region_tmja.html")

        with open(carte_html_path, 'r', encoding='utf-8') as f:
            carte_html = f.read()

        components.html(carte_html, height=500, width=500)

    with map_col4:
        st.markdown("### TMJA par " + niveau_carte.lower())

        if niveau_carte == "Département":
            fig_bar = barplot_tmja_dep(df_tmja_d) 
        else:
            fig_bar = barplot_tmja_region(df_tmja_r)

        st.plotly_chart(fig_bar, use_container_width=True, width=400)
    
    #st.markdown("### Ratios avec bornes de recharge")
    # = st.radio("Choisissez le type de carte :", ["Bornes / TMJA", "TMJA / Bornes"], horizontal=True)

    # Colonnes pour régions et départements
    #col_regions, col_departements = st.columns(2)

    # Définir le chemin de base pour les fichiers
    #current_dir = os.path.dirname(os.path.abspath(__file__))

    # Charger les cartes selon la sélection
    #if type_carte == "Bornes / TMJA":
     #   carte_region = "carte_reg_nb_borne_TMJA.html"
#carte_dep = "carte_dep_nb_borne_TMJA.html"
   # else:
   #     carte_region = "carte_reg_TMJA_nb_borne.html"
    #    carte_dep = "carte_dep_TMJA_nb_borne.html"

    # Affichage des cartes
    #with col_regions:
      #  st.markdown("### Régions")
      #  path_region = os.path.join(current_dir, "..", "Cartes","cartes_bornes_tmja" ,carte_region)
      #  with open(path_region, 'r', encoding='utf-8') as f:
      #      html_region = f.read()
       # components.html(html_region, height=500)

   # with col_departements:
      #  st.markdown("### Départements")
      #  path_dep = os.path.join(current_dir, "..", "Cartes", "cartes_bornes_tmja",carte_dep)
      #  with open(path_dep, 'r', encoding='utf-8') as f:
      #      html_dep = f.read()
      #  components.html(html_dep, height=500)
    
    

elif page == "⚡Vehicules par borne":
    st.title("⚡Véhicules par Borne")
    annees = sorted(df_ve_b['Annee'].unique())
    regions = sorted(df_ve_b['nom_region'].dropna().unique())
    departements = sorted(df_ve_b['nom_departement'].dropna().unique())
    
    col_top1, col_top2, col_top3 = st.columns(3)

    # 🎨 Personnalisation du slider
    st.markdown("""
        <style>
        /* Texte et track du slider */
        .stSlider > div[data-baseweb="slider"] > div {
            color: white !important; /* Couleur du texte */
        }

        /* Barre active du slider */
        .stSlider > div[data-baseweb="slider"] > div > div {
            background: #7e57c2 !important; /* Couleur de la barre */
        }

        /* Curseur (le bouton rond) */
        .stSlider [role="slider"] {
            background-color: #9575cd  !important;  /* Couleur du curseur */
            border: 2px solid white;               /* Contour blanc */
        }
        .stSlider > div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 🎚️ Ton slider
    with col_top1:
        annee_selectionnee = st.slider(
            "📅 Choisissez une année d'analyse",
            min_value=2020,
            max_value=2024,
            value=2022,
            step=1
        )

    with col_top2:
        region_selectionnee = st.selectbox("Sélectionnez la région", regions, key='reg')
        
    departements_filtrés = sorted(df_ve_b[df_ve_b['nom_region'] == region_selectionnee]['nom_departement'].unique())

    with col_top3:
        departement_selectionne = st.selectbox("Sélectionnez le département", departements_filtrés, key='dep')

    placeholder = st.empty()

    with placeholder.container():
        kpi_fr,kpi_reg,kpi_dep = st.columns(3)
        
        
        with kpi_fr:
            fig_fr = vignette_el_b_fr(df_ve_b, annee_selectionnee)
            if fig_fr:
                st.plotly_chart(fig_fr)
            else:
                st.warning("Pas de données disponibles pour la France.")
        
        with kpi_reg:
            fig_reg = vignette_el_b_reg(df_ve_b_r, annee_selectionnee, region_selectionnee)
            if fig_reg:
                st.plotly_chart(fig_reg)
            else:
                st.warning("Pas de données disponibles pour la région sélectionnée.")       
        
        with kpi_dep:
            fig_dep = vignette_el_b_dep(df_ve_b, annee_selectionnee, departement_selectionne)
            if fig_dep:
                st.plotly_chart(fig_dep)
            else:
                st.warning("Pas de données disponibles pour le département sélectionné.")

        #col_map1, col_map3 = st.columns(2)  # col2 = slider centré, prend 1/2 de l'espace

        #with col_map2:

        #st.markdown(f"### 🔍 Année sélectionnée : `{annee}`")
        col_map_ve_b_1, col_map_ve_b_2 = st.columns(2)

        current_dir = os.path.dirname(__file__)
        cartes_dir = os.path.join(current_dir, "..", "Cartes", "Cartes_VE_bornes")

        carte_dep_path = os.path.join(cartes_dir, f"carte_dep_nb_el_borne_{annee_selectionnee}.html")
        carte_reg_path = os.path.join(cartes_dir, f"carte_reg_nb_el_borne_{annee_selectionnee}.html")

        with col_map_ve_b_1:
            st.markdown(f"### Carte des régions - {annee_selectionnee}")
            with open(carte_reg_path, 'r', encoding='utf-8') as f:
                carte_reg_html = f.read()
            components.html(carte_reg_html, height=450, width=500)

        with col_map_ve_b_2:
            st.markdown(f"### Carte des départements - {annee_selectionnee}")
            with open(carte_dep_path, 'r', encoding='utf-8') as f:
                carte_dep_html = f.read()
            components.html(carte_dep_html, height=450, width=500)
        
        col_choix1, col_choix2, col_choix3 = st.columns(3)
        with col_choix2:
            
            st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


            choix_graphe_vpb = st.radio(
                        "📈 Sélectionnez la zone d'évolution :",
                        ["France", "Région", "Département"],
                        horizontal=True
                    )   
        col_evol_vpb,col_base100 = st.columns(2)
        with col_base100:
            st.markdown("### Évolution des véhicules par borne (base 100)")
            if choix_graphe_vpb == "France":
                fig = graphique_evolution_base100_fr(df_ve_b, df_ve_b_r)
                st.plotly_chart(fig, use_container_width=True, key="evol_france_vpb_base100")
            elif choix_graphe_vpb == "Région":
                fig = graphique_evolution_base100_reg(df, df_2,region_selectionnee)
                st.plotly_chart(fig, use_container_width=True, key="evol_reg_vpb_base100")
            elif choix_graphe_vpb == "Département":
                fig = graphique_evolution_base100_dep(df, df_2, departement_selectionne)
                st.plotly_chart(fig, use_container_width=True, key="evol_dep_vpb_base100")
        
        with col_evol_vpb:
            st.markdown("### Évolution des véhicules par borne")
            if choix_graphe_vpb == "France":
                fig = graphique_evolution_france_vpb(df_ve_b)
                st.plotly_chart(fig, use_container_width=True, key="evol_france_vpb")
            elif choix_graphe_vpb == "Région":
                fig = graphique_evolution_vpb_region(df_ve_b,region_selectionnee)
                st.plotly_chart(fig, use_container_width=True, key="evol_reg_vpb")
            elif choix_graphe_vpb == "Département":
                fig = graphique_evolution_vpb_dep(df_ve_b, departement_selectionne)
                st.plotly_chart(fig, use_container_width=True, key="evol_dep_vpb")
                
elif page == "📈 Objectifs 2030":
    st.title("📈 Objectifs gouvernementaux pour 2030 vs Réalité actuelle")

    st.markdown("## 🎯 Objectifs du gouvernement à horizon 2030")

    st.markdown("""
    <style>
    .card-objectif {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        margin-bottom: 15px;
    }
    .card-objectif h2 {
        margin-bottom: 0;
        font-size: 30px;
        color: #4CAF50;
    }
    .card-objectif p {
        margin-top: 5px;
        font-size: 16px;
        color: #cccccc;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class="card-objectif">
            <h2>5,7 M</h2>
            <p>Véhicules électriques en circulation</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card-objectif">
            <h2>7 M</h2>
            <p>Points de recharge (publics + privés)</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card-objectif">
            <h2>400 000</h2>
            <p>Bornes publiques</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="card-objectif">
            <h2>50 000</h2>
            <p>Bornes à haute puissance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="card-objectif">
            <h2>14,25</h2>
            <p>Ratio véhicules éléctriques/borne</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("## 📊 Données actuelles en 2024")


    col_a1, col_a2, col_a3 = st.columns(3)

    with col_a1:
        st.markdown(f"""
        <div class="card-objectif">
            <h2>1.88M</h2>
            <p>Véhicules électriques en 2024</p>
        </div>
        """, unsafe_allow_html=True)

    with col_a2:
        st.markdown(f"""
        <div class="card-objectif">
            <h2>126 000</h2>
            <p>Bornes publiques en 2024</p>
        </div>
        """, unsafe_allow_html=True)

    with col_a3:
        st.markdown(f"""
        <div class="card-objectif">
            <h2>15</h2>
            <p>Ratio véhicules éléctriques/borne en 2024</p>
        </div>
        """, unsafe_allow_html=True)

    st.title("🔮Prédictions")
    #annees = sorted(df['Annee'].unique())
    regions = sorted(df['region'].dropna().unique())
    departements = sorted(df['departement'].dropna().unique())
    
    # Barre de sélection en haut
    col_top1, col_top2 = st.columns(2)

    with col_top1:
        region_selectionnee = st.selectbox("Sélectionnez la région", regions, key='reg_pred')
    with col_top2:
        departements_filtrés = sorted(df[df['region'] == region_selectionnee]['departement'].unique())
        departement_selectionne = st.selectbox("Sélectionnez le département", departements_filtrés, key='dep_pred')
    
    col_but1, col_but2, col_but3 = st.columns(3)
    with col_but2:
        st.markdown("""
    <style>
    /* Style du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] {
        background-color: #7e57c2 !important;  /* Violet */
        color: white !important;
        border-radius: 8px;
    }

    /* Cercle intérieur (radio button) du bouton sélectionné */
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child {
        background-color: white !important;  /* Cercle externe */
        border: 2px solid white !important;
    }
    div[data-testid="stRadio"] > div > label[data-selected="true"] span[data-baseweb="radio"] > div:first-child > div {
        background-color: #7e57c2 !important;  /* Cercle violet interne */
    }

    /* Style général des boutons */
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #7e57c2 !important;
        border-radius: 8px;
        padding: 6px 12px;
        margin-right: 6px;
        color: #cfcfcf;
        transition: all 0.2s ease-in-out;
    }

    /* Effet au survol */
    div[data-testid="stRadio"] > div > label:hover {
        background-color: #9575cd22;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
        choix_graphe_pred = st.radio(
                    "📈 Sélectionnez la zone d'évolution :",
                    ["France", "Région", "Département"],
                    horizontal=True
                )
    col_pred1, col_pred2 = st.columns(2)    
    with col_pred1:

            if choix_graphe_pred == "France":
                fig = graphique_evolution_france_ve_pred(df)
                st.plotly_chart(fig, use_container_width=True, key="evol_france_ve_pred")

            elif choix_graphe_pred == "Région":
                fig = graphique_evolution_ve_region_pred(df, region_selectionnee)
                st.plotly_chart(fig, use_container_width=True, key="evol_reg_ve_pred")

            elif choix_graphe_pred == "Département":
                fig = graphique_evolution_ve_departement_pred(df, departement_selectionne)
                st.plotly_chart(fig, use_container_width=True, key="evol_dep_ve_pred")

    with col_pred2:
            if choix_graphe_pred == "France":
                fig=graphique_evolution_bornes_france_pred(df_2)
                st.plotly_chart(fig, use_container_width=True, key="evol_b_france_tot_pred")
            elif choix_graphe_pred == "Région":
                fig_reg_evol_pred = graphique_evolution_bornes_region_pred(df_2, region_selectionnee)
                st.plotly_chart(fig_reg_evol_pred, key="evol_reg_tot_pred", use_container_width=True)
            elif choix_graphe_pred == "Département":
                fig_dep_evol_pred = graphique_evolution_bornes_dep_pred(df_2, departement_selectionne)
                st.plotly_chart(fig_dep_evol_pred, key="evol_dep_tot_pred", use_container_width=True)
    
    if choix_graphe_pred == "France":
        fig=graphique_evolution_france_vpb_pred(df_ve_b)
        st.plotly_chart(fig, use_container_width=True, key="vpb_fr_pred")
    elif choix_graphe_pred == "Région":
        fig_reg_evol_pred = graphique_evolution_vpb_region_pred(df_ve_b, region_selectionnee)
        st.plotly_chart(fig_reg_evol_pred, key="vpb_reg_pred", use_container_width=True)
    elif choix_graphe_pred == "Département":
        fig_dep_evol_pred = graphique_evolution_vpb_dep_pred(df_ve_b, departement_selectionne)
        st.plotly_chart(fig_dep_evol_pred, key="vpb_dep_pred", use_container_width=True)
