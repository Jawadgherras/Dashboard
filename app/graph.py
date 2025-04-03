import pandas as pd
import numpy as np
import plotly.express as px
import os
import sys
import plotly.graph_objects as go

current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_VE" ,"data_VE.csv")
df = pd.read_csv(csv_path, encoding="ISO-8859-1", on_bad_lines="skip", sep=";")

current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_bornes" ,"bornes_totale_departement.csv")
df_1 = pd.read_csv(csv_path,sep=";", encoding="ISO-8859-1")


current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_bornes" ,"data_final.csv")
df_2= pd.read_csv(csv_path, encoding='utf-8', sep=',', low_memory=False) 
df_2 = df_2.rename(columns={
    "annee_mise_en_service": "Annee",
    "region": "nom_region",
    "depart": "nom_departement"
})

#df_2["nom_region"] = df_2["nom_region"].astype(str)
#df_2["nom_departement"] = df_2["nom_departement"].astype(str)
#df_2["nb_borne"] = df_2["nb_borne"].astype(int)

current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_TMJA" ,"tmja-departement-mean.csv")
df_tmja_d = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip", sep=",")
df_tmja_d["TMJA"] = df_tmja_d["TMJA"].round(2)


current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_TMJA" ,"tmja-region-mean.csv")
df_tmja_r = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip", sep=",")
df_tmja_r["TMJA"] = df_tmja_r["TMJA"].round(2)
df_tmja_r = df_tmja_r.rename(columns={
    "region": "nom_region"
})
df_tmja_r["TMJA"] = df_tmja_r["TMJA"].round(2)

current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_VE_bornes" ,"vehicules_electriques_par_borne.csv")
df_ve_b = pd.read_csv(csv_path,sep=",", encoding="utf-8", on_bad_lines="skip")

current_dir = os.path.dirname(sys.argv[0])
csv_path = os.path.join(current_dir, "..", "data", "data_VE_bornes" ,"vehicules_electriques_par_borne_reg.csv")
df_ve_b_r = pd.read_csv(csv_path,sep=",", encoding="utf-8", on_bad_lines="skip")

def graphique_interactif_france(df, annee):
    df_filtre = df[df["Annee"] == annee]

    if not df_filtre.empty:
        NB_VP_RECHARGEABLES_EL = df_filtre["NB_VP_RECHARGEABLES_EL"].sum()
        
        previous_NB_VP_RECHARGEABLES_EL = None

        df_precedent = df[df["Annee"] == annee - 1]
        if not df_precedent.empty:
            previous_NB_VP_RECHARGEABLES_EL = df_precedent["NB_VP_RECHARGEABLES_EL"].sum()
            variation = ((NB_VP_RECHARGEABLES_EL - previous_NB_VP_RECHARGEABLES_EL) / previous_NB_VP_RECHARGEABLES_EL) * 100
            color = "green " if variation > 0 else "red"
        else:
            variation = None
            color = "white"
    else:
        return None

    # Créer la vignette avec Plotly
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=NB_VP_RECHARGEABLES_EL,
        title={"text": f"<span style='color:white'>France</span>"},
        delta={
            "reference": previous_NB_VP_RECHARGEABLES_EL,
            "relative": True,
            "valueformat": ".2%"  
        } if previous_NB_VP_RECHARGEABLES_EL else None,
        number={"font": {"color": color, "size": 55}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#4a148c'
    )

    return fig


def graphique_interactif_dep(df, annee, departement):
    # Filtrer les données pour le département et l'année sélectionnée
    df_filtre = df[(df["departement"] == departement) & (df["Annee"] == annee)]
    
    # Vérifier si des données sont disponibles
    if not df_filtre.empty:
        NB_VP_RECHARGEABLES_EL = df_filtre["NB_VP_RECHARGEABLES_EL"].sum()  # Somme des véhicules rechargeables

        # Obtenir la valeur de l'année précédente
        df_precedent = df[(df["departement"] == departement) & (df["Annee"] == annee - 1)]
        previous_NB_VP_RECHARGEABLES_EL = df_precedent["NB_VP_RECHARGEABLES_EL"].sum() if not df_precedent.empty else None

        # Calcul de la variation en pourcentage
        if previous_NB_VP_RECHARGEABLES_EL and previous_NB_VP_RECHARGEABLES_EL != 0:
            variation = ((NB_VP_RECHARGEABLES_EL - previous_NB_VP_RECHARGEABLES_EL) / previous_NB_VP_RECHARGEABLES_EL) * 100
            color = "green" if variation > 0 else "red"
        else:
            variation = None
            color = "white"
    else:
        return None

    # Créer le graphique de la vignette
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=NB_VP_RECHARGEABLES_EL,
        title={"text": f"<span style='color:white'>{departement}</span>"},
        delta={
            "reference": previous_NB_VP_RECHARGEABLES_EL,
            "relative": True,
            "valueformat": ".2%"  
        } if previous_NB_VP_RECHARGEABLES_EL else None,
        number={"font": {"color": color, "size": 55}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#7e57c2'
    )

    return fig


def graphique_interactif_region(df, annee, region):
    # Filtrer les données pour la région et l'année sélectionnée
    df_filtre = df[(df["region"] == region) & (df["Annee"] == annee)]
    
    # Vérifier si des données sont disponibles
    if not df_filtre.empty:
        NB_VP_RECHARGEABLES_EL = df_filtre["NB_VP_RECHARGEABLES_EL"].sum()  # Somme des véhicules rechargeables

        # Obtenir la valeur de l'année précédente
        df_precedent = df[(df["region"] == region) & (df["Annee"] == annee - 1)]
        previous_NB_VP_RECHARGEABLES_EL = df_precedent["NB_VP_RECHARGEABLES_EL"].sum() if not df_precedent.empty else None

        # Calcul de la variation en pourcentage
        if previous_NB_VP_RECHARGEABLES_EL and previous_NB_VP_RECHARGEABLES_EL != 0:
            variation = ((NB_VP_RECHARGEABLES_EL - previous_NB_VP_RECHARGEABLES_EL) / previous_NB_VP_RECHARGEABLES_EL) * 100
            color = "green" if variation > 0 else "red"
        else:
            variation = None
            color = "white"
    else:
        return None

    # Créer le graphique de la vignette
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=NB_VP_RECHARGEABLES_EL,
        title={"text": f"<span style='color:white'>{region}</span>"},
        delta={
            "reference": previous_NB_VP_RECHARGEABLES_EL,
            "relative": True,
            "valueformat": ".2%"  
        } if previous_NB_VP_RECHARGEABLES_EL else None,
        number={"font": {"color": color, "size": 55}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#673ab7'
    )

    return fig


def graphique_bornes_dep(df_2, departement, annee):
    # Filtrer les données pour le département et l'année sélectionnée
    df_filtre = df_2[(df_2["nom_departement"] == departement) & (df_2["Annee"] == annee)]

    if df_filtre.empty:
        return None  # Aucune donnée pour ce département et cette année

    # Calculer la somme des bornes pour le département (en gérant les NaN)
    nb_bornes = df_filtre["nb_borne"].sum(skipna=True)

    # Récupérer les bornes de l'année précédente (en gérant les NaN)
    df_2_precedent = df_2[(df_2["nom_departement"] == departement) & (df_2["Annee"] == annee - 1)]
    previous_nb_borne = df_2_precedent["nb_borne"].sum(skipna=True) if not df_2_precedent.empty else 0

    # Vérifier et calculer la variation en pourcentage
    if previous_nb_borne > 0:
        variation = ((nb_bornes - previous_nb_borne) / previous_nb_borne) * 100
        color = "green" if variation > 0 else "red"
    else:
        variation = None
        color = "white"

    # Création du graphique
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_bornes,
        title={"text": f"<span style='color:white'>{departement}</span>"},
        delta={
            "reference": previous_nb_borne,
            "relative": True,
            "valueformat": ".2%"
        } if previous_nb_borne > 0 else None,  # Correction ici pour éviter le delta si previous_nb_borne est 0
        number={"font": {"color": color, "size": 50}, "valueformat": ".3s"}
    ))

    # Mise en page
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#7e57c2'
    )

    return fig



def vignette_borne_instal_reg(df_2, region, annee):
    # Filtrer les données pour la région et l'année sélectionnée
    df_filtre = df_2[(df_2["nom_region"] == region) & (df_2["Annee"] == annee)]

    if df_filtre.empty:
        return None  # Aucune donnée pour cette région et cette année

    # Calculer la somme des bornes pour la région
    nb_bornes = df_filtre["nb_borne"].sum()

    # Récupérer les bornes de l'année précédente
    df_2_precedent = df_2[(df_2["nom_region"] == region) & (df_2["Annee"] == annee - 1)]
    previous_nb_borne = df_2_precedent["nb_borne"].sum() if not df_2_precedent.empty else None

    # Calcul de la variation en pourcentage
    if previous_nb_borne is not None and previous_nb_borne > 0:
        variation = ((nb_bornes - previous_nb_borne) / previous_nb_borne) * 100
        color = "green" if variation > 0 else "red"
    else:
        variation = None
        color = "white"

    # Création du graphique
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_bornes,
        title={"text": f"<span style='color:white'>{region}</span>"},
        delta={
            "reference": previous_nb_borne,
            "relative": True,
            "valueformat": ".2%"
        } if previous_nb_borne is not None else None,  # Correction de la condition
        number={"font": {"color": color, "size": 50}, "valueformat": ".3s"}
    ))

    # Mise en page
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#673ab7'
    )

    return fig

    
def graphique_evolution_france_ve(df):
    df_france_evol = df.groupby('Annee')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_france_evol['Annee'], 
        y=df_france_evol['NB_VP_RECHARGEABLES_EL'], 
        mode='lines+markers',
        line=dict(color='#9575cd')
    ))

    fig.update_layout(
        title="Évolution des véhicules électriques en France",
        xaxis_title="",
        yaxis_title="Nombre de véhicules"
    )

    return fig

def graphique_evolution_france_b(df_2):
    df_france_evol = df_2[~df_2['Annee'].isin([2025, 1930,2002])].groupby(['Annee'])['nb_borne'].sum().reset_index()
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_france_evol['Annee'], 
        y=df_france_evol['nb_borne'], 
        mode='lines+markers',
        line=dict(color='#9575cd ')
    ))

    fig.update_layout(
        title="Évolution des bornes installées en France",
        xaxis_title="",
        yaxis_title="Nombre de bornes",
        
    )
    return fig


def graphique_interactif_france_b(df_2, annee):
    # Filtrer les données pour l'année sélectionnée et toutes les années précédentes
    df_filtre = df_2[df_2["Annee"] <= annee]

    if not df_filtre.empty:
        nb_borne = df_filtre["nb_borne"].sum()

        # Initialisation de la valeur précédente
        previous_nb_borne = None

        # Calculer la variation par rapport à l'année précédente
        df_precedent = df_2[df_2["Annee"] <= annee - 1]
        if not df_precedent.empty:
            previous_nb_borne = df_precedent["nb_borne"].sum()
            
            # Vérifier si previous_nb_borne est valide avant de calculer la variation
            if previous_nb_borne > 0:
                variation = ((nb_borne - previous_nb_borne) / previous_nb_borne) * 100
                color = "green" if variation > 0 else "red"
            else:
                variation = None
                color = "white"
        else:
            variation = None
            color = "white"
    else:
        return None  # Retourner None si aucune donnée n'est disponible

    # Création du graphique avec Plotly
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_borne,
        title={"text": f"<span style='color:white'>Bornes de recharge installées en France</span>"},
        delta={
            "reference": previous_nb_borne,
            "relative": True,
            "valueformat": ".2%"
        } if previous_nb_borne else None,
        number={"font": {"color": color, "size": 50}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#4a148c'
    )

    return fig


def graphique_bornes_region_1(df_2, region, annee):
    # Filtrer les données pour la région sélectionnée et toutes les années jusqu'à l'année sélectionnée
    df_filtre = df_2[(df_2["nom_region"] == region) & (df_2["Annee"] <= annee)]

    # ✅ Si aucune donnée, on arrête là
    if df_filtre.empty:
        return None

    nb_borne = df_filtre["nb_borne"].sum()

    # Calculer la variation par rapport à l'année précédente
    df_precedent = df_2[(df_2["nom_region"] == region) & (df_2["Annee"] <= annee - 1)]

    if not df_precedent.empty:
        previous_nb_borne = df_precedent["nb_borne"].sum()

        if previous_nb_borne > 0:
            variation = ((nb_borne - previous_nb_borne) / previous_nb_borne) * 100
            color = "green" if variation > 0 else "red"
        else:
            variation = None
            color = "white"
    else:
        previous_nb_borne = None
        variation = None
        color = "white"

    # Création du graphique avec Plotly
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_borne,
        title={"text": f"<span style='color:white'>Total bornes - {region}</span>"},
        delta={
            "reference": previous_nb_borne,
            "relative": True,
            "valueformat": ".2%"
        } if previous_nb_borne is not None else None,
        number={"font": {"color": color, "size": 50}, "valueformat": ".3s"}
    ))

    # Mise en page
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#673ab7'
    )

    return fig




def graphique_bornes_dep_1(df_2, departement, annee):
    # Filtrer les données pour le département sélectionné et toutes les années jusqu'à l'année sélectionnée
    df_filtre = df_2[(df_2["nom_departement"] == departement) & (df_2["Annee"] <= annee)]

    if df_filtre.empty:
        return None  # Aucune donnée pour ce département et cette année

    # Calculer la somme des bornes pour le département
    nb_bornes = df_filtre["nb_borne"].sum()

    # Calculer la variation par rapport à l'année précédente
    df_precedent = df_2[(df_2["nom_departement"] == departement) & (df_2["Annee"] <= annee - 1)]

    if not df_precedent.empty:
        previous_nb_borne = df_precedent["nb_borne"].sum()

        if previous_nb_borne > 0:
            variation = ((nb_bornes - previous_nb_borne) / previous_nb_borne) * 100
            color = "green" if variation > 0 else "red"
        else:
            variation = None
            color = "white"
    else:
        previous_nb_borne = None
        variation = None
        color = "white"

    # Création du graphique avec Plotly
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_bornes,
        title={"text": f"<span style='color:white'>Total bornes - {departement}</span>"},
        delta={
            "reference": previous_nb_borne,
            "relative": True,
            "valueformat": ".2%"
        } if previous_nb_borne is not None else None,
        number={"font": {"color": color, "size": 50}, "valueformat": ".3s"}
    ))

    # Mise en page
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#7e57c2'
    )

    return fig


def graphique_tmja_dep(df_tmja_d, departement):
        # Filtrer les données pour le département sélectionné (sans distinction d'année)
    df_filtre = df_tmja_d[df_tmja_d["nom_departement"] == departement]

    if df_filtre.empty:
        return None  # Aucune donnée pour ce département

    # Récupérer directement la valeur de nb_borne (une ligne = un département)
    tmja = df_filtre["TMJA"].iloc[0]  # On prend la première ligne car chaque département est unique

    # Création du graphique avec Plotly (sans variation)
    fig = go.Figure(go.Indicator(
        mode="number",
        value=tmja,
        title={"text": f"<span style='color:white'>Total TMJA - {departement}</span>"},
        number={"font": {"color": "white", "size": 50}, "valueformat": ".3s"}
    ))

    # Mise en page
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#7e57c2'
    )

    return fig

def graphique_tmja_region(df_tmja_r, region):
    df_filtre = df_tmja_r[df_tmja_r["nom_region"] == region]

    if df_filtre.empty:
        return None  

    nb_bornes = df_filtre["TMJA"].sum()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=nb_bornes,
        title={"text": f"<span style='color:white'>Total TMJA - {region}</span>"},
        number={"font": {"color": "white", "size": 50}, "valueformat": ".3s"}
    ))

    # Mise en page
    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#673ab7'
    )
    return fig

def graphique_tmja_france(df_tmja_r):
    tmja = df_tmja_r["TMJA"].sum()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=tmja,
        title={"text": f"<span style='color:white'>Total des TMJA en France</span>"},
        number={"font": {"color": "white", "size": 50}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#4a148c')

    return fig


def barplot_tmja_region(df_tmja_r):
    # Regrouper les données par région et calculer la somme des TMJA
    df_tmja_region = df_tmja_r.groupby("nom_region")["TMJA"].sum().reset_index()

    # Garder uniquement le top 10 régions avec TMJA le plus élevé
    df_tmja_top10 = df_tmja_region.sort_values(by="TMJA", ascending=False).head(10)

    fig = px.bar(
        df_tmja_top10,
        y="nom_region",
        x="TMJA",
        title="Top 10 Régions par TMJA",
        labels={"nom_region": "Région", "TMJA": "Trafic Moyen Journalier Annuel"},
        text="TMJA",
        orientation="h",
        category_orders={"nom_region": df_tmja_top10["nom_region"].tolist()[::-1]},
        color_discrete_sequence=["#4a148c"]
    )

    # Mise en page personnalisée
    fig.update_layout(
        xaxis_title="TMJA",
        yaxis_title="",
        template='simple_white',
    )

    return fig



def barplot_tmja_dep(df_tmja_d):
    # Regrouper les données par département et calculer la somme des TMJA
    df_tmja_dep = df_tmja_d.groupby("nom_departement")["TMJA"].sum().reset_index()

    # Garder uniquement le top 10 départements avec TMJA le plus élevé
    df_tmja_top10 = df_tmja_dep.sort_values(by="TMJA", ascending=False).head(10)

    fig = px.bar(
        df_tmja_top10,
        y="nom_departement",
        x="TMJA",
        title="Top 10 Départements par TMJA",
        labels={"nom_departement": "Département", "TMJA": "Trafic Moyen Journalier Annuel"},
        text="TMJA",
        orientation="h",
        category_orders={"nom_departement": df_tmja_top10["nom_departement"].tolist()[::-1]},
        color_discrete_sequence=["#9575cd "]
    )

    # Mise en page personnalisée
    fig.update_layout(
        xaxis_title="TMJA",
        yaxis_title="",
        template='simple_white',
    )

    return fig


def vignette_el_b_fr(df_ve_b, annee):
    df_filtre = df_ve_b[df_ve_b["Annee"] == annee]

    if not df_filtre.empty:
        nb_el_borne = df_filtre["nb_el/borne"].mean()
        
        previous_nb_el_borne = None

        # Calculer la variation par rapport à l'année précédente
        df_precedent = df_ve_b[df_ve_b["Annee"] == annee - 1]
        if not df_precedent.empty:
            previous_nb_el_borne = df_precedent["nb_el/borne"].sum()
            variation = ((nb_el_borne - previous_nb_el_borne) / previous_nb_el_borne) * 100
            color = "red " if variation > 0 else "green"
        else:
            variation = None
            color = "white"
    else:
        return None

    # Créer la vignette avec Plotly
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_el_borne,
        title={"text": f"<span style='color:white'>Véhicules/bornes - France</span>"},
        delta={
            "reference": previous_nb_el_borne,
            "relative": True,
            "valueformat": ".2%",
            "increasing": {"color": "red"},   
            "decreasing": {"color": "green"} 
        } if previous_nb_el_borne else None,
        number={"font": {"color": color, "size": 55}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#4a148c'
    )

    return fig


def vignette_el_b_dep(df_ve_b, annee, departement):
    # Filtrer les données pour le département et l'année sélectionnée
    df_filtre = df_ve_b[(df_ve_b["nom_departement"] == departement) & (df_ve_b["Annee"] == annee)]
    
    # Vérifier si des données sont disponibles
    if not df_filtre.empty:
        nb_el_borne = df_filtre["nb_el/borne"].sum()  # Somme des véhicules rechargeables

        # Obtenir la valeur de l'année précédente
        df_precedent = df_ve_b[(df_ve_b["nom_departement"] == departement) & (df_ve_b["Annee"] == annee - 1)]
        previous_nb_el_borne = df_precedent["nb_el/borne"].sum() if not df_precedent.empty else None

        # Calcul de la variation en pourcentage
        if previous_nb_el_borne and previous_nb_el_borne != 0:
            variation = ((nb_el_borne - previous_nb_el_borne) / previous_nb_el_borne) * 100
            color = "red" if variation > 0 else "green"
        else:
            variation = None
            color = "white"
    else:
        return None

    # Créer le graphique de la vignette
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_el_borne,
        title={"text": f"<span style='color:white'>Véhicules/bornes - {departement}</span>"},
        delta={
            "reference": previous_nb_el_borne,
            "relative": True,
            "valueformat": ".2%",
            "increasing": {"color": "red"},   
            "decreasing": {"color": "green"} 
        } if previous_nb_el_borne else None,
        number={"font": {"color": color, "size": 55}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#7e57c2'
    )

    return fig


def vignette_el_b_reg(df_ve_b_r, annee, region):
    df_filtre = df_ve_b_r[(df_ve_b_r["nom_region"] == region) & (df_ve_b_r["Annee"] == annee)]
    
    if df_filtre.empty:
        return None

    nb_el_borne = df_filtre["nb_el/borne"].mean()

    df_precedent = df_ve_b_r[(df_ve_b_r["nom_region"] == region) & (df_ve_b_r["Annee"] == annee - 1)]
    previous_nb_el_borne = df_precedent["nb_el/borne"].mean() if not df_precedent.empty else None

    if previous_nb_el_borne and previous_nb_el_borne != 0:
        variation = ((nb_el_borne - previous_nb_el_borne) / previous_nb_el_borne) * 100
        color = "red" if variation > 0 else "green"
    else:
        variation = None
        color = "white"

    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_el_borne,
        title={"text": f"<span style='color:white'>Véhicules/bornes - {region}</span>"},
        delta={
            "reference": previous_nb_el_borne,
            "relative": True,
            "valueformat": ".2%",
            "increasing": {"color": "red"},   
            "decreasing": {"color": "green"} 
        } if previous_nb_el_borne else None,
        number={
            "font": {"color": color, "size": 55},
            "valueformat": ".2f"
        }
    ))

    fig.update_layout(
        height=170,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#673ab7'
    )

    return fig

def graphique_evolution_base100_fr(df_vehicules, df_bornes):
    df_fr_elec = (
        df_vehicules[(df_vehicules['Annee'] >= 2020) & (df_vehicules['Annee'] < 2025)]
        .groupby('Annee')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
    )

    base_vehicules = df_fr_elec[df_fr_elec['Annee'] == 2020]['NB_VP_RECHARGEABLES_EL'].iloc[0]
    df_fr_elec['base100_vehicules'] = df_fr_elec['NB_VP_RECHARGEABLES_EL'] / base_vehicules * 100

    df_fr_bornes = (
        df_bornes[(df_bornes['Annee'] >= 2020) & (df_bornes['Annee'] < 2025)]
        .groupby('Annee')['nb_borne']
        .sum()
        .reset_index()
    )
    df_fr_bornes['cumul_borne'] = df_fr_bornes['nb_borne'].cumsum()

    base_bornes = df_fr_bornes[df_fr_bornes['Annee'] == 2020]['cumul_borne'].iloc[0]
    df_fr_bornes['base100_bornes'] = df_fr_bornes['cumul_borne'] / base_bornes * 100

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_fr_elec['Annee'],
        y=df_fr_elec['base100_vehicules'],
        mode='lines+markers',
        name='Véhicules électriques',
        line=dict(color='#5e35b1 ')
    ))

    fig.add_trace(go.Scatter(
        x=df_fr_bornes['Annee'],
        y=df_fr_bornes['base100_bornes'],
        mode='lines+markers',
        name='Bornes électriques',
        line=dict(color='#d1c4e9 ')
    ))

    fig.update_layout(
        title={
            'text': "Évolution comparée des véhicules et bornes électriques en France",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Évolution (base 100)",
        legend=dict(x=0.02, y=0.98),
        #height=500
    )

    return fig


def graphique_evolution_base100_reg(df_vehicules, df_bornes, region_selectionnee):
    df_reg_elec = (
        df_vehicules[(df_vehicules['region'] == region_selectionnee) & (df_vehicules['Annee'] >= 2020) & (df_vehicules['Annee'] < 2025)]
        .groupby('Annee')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
    )

    base_vehicules = df_reg_elec[df_reg_elec['Annee'] == 2020]['NB_VP_RECHARGEABLES_EL'].iloc[0]
    df_reg_elec['base100_vehicules'] = df_reg_elec['NB_VP_RECHARGEABLES_EL'] / base_vehicules * 100

    df_reg_bornes = (
        df_bornes[(df_bornes['nom_region'] == region_selectionnee) & (df_bornes['Annee'] >= 2020) & (df_bornes['Annee'] < 2025)]
        .groupby('Annee')['nb_borne']
        .sum()
        .reset_index()
    )
    df_reg_bornes['cumul_borne'] = df_reg_bornes['nb_borne'].cumsum()

    base_bornes = df_reg_bornes[df_reg_bornes['Annee'] == 2020]['cumul_borne'].iloc[0]
    df_reg_bornes['base100_bornes'] = df_reg_bornes['cumul_borne'] / base_bornes * 100

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_reg_elec['Annee'],
        y=df_reg_elec['base100_vehicules'],
        mode='lines+markers',
        name='Véhicules électriques',
        line=dict(color='#5e35b1 ')
    ))

    fig.add_trace(go.Scatter(
        x=df_reg_bornes['Annee'],
        y=df_reg_bornes['base100_bornes'],
        mode='lines+markers',
        name='Bornes électriques',
        line=dict(color='#d1c4e9 ')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution comparée des véhicules et bornes électriques en {region_selectionnee}",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Évolution (base 100)",
        legend=dict(x=0.02, y=0.98),
    )

    return fig


def graphique_evolution_base100_dep(df_vehicules, df_bornes, departement_selectionne):
    df_dep_elec = (
        df_vehicules[(df_vehicules['departement'] == departement_selectionne) & (df_vehicules['Annee'] >= 2020) & (df_vehicules['Annee'] < 2025)]
        .groupby('Annee')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
    )

    base_vehicules = df_dep_elec[df_dep_elec['Annee'] == 2020]['NB_VP_RECHARGEABLES_EL'].iloc[0]
    df_dep_elec['base100_vehicules'] = df_dep_elec['NB_VP_RECHARGEABLES_EL'] / base_vehicules * 100

    df_dep_bornes = (
        df_bornes[(df_bornes['nom_departement'] == departement_selectionne) & (df_bornes['Annee'] >= 2020) & (df_bornes['Annee'] < 2025)]
        .groupby('Annee')['nb_borne']
        .sum()
        .reset_index()
    )
    df_dep_bornes['cumul_borne'] = df_dep_bornes['nb_borne'].cumsum()

    base_bornes = df_dep_bornes[df_dep_bornes['Annee'] == 2020]['cumul_borne'].iloc[0]
    df_dep_bornes['base100_bornes'] = df_dep_bornes['cumul_borne'] / base_bornes * 100

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_dep_elec['Annee'],
        y=df_dep_elec['base100_vehicules'],
        mode='lines+markers',
        name='Véhicules électriques',
        line=dict(color='#5e35b1 ')
    ))

    fig.add_trace(go.Scatter(
        x=df_dep_bornes['Annee'],
        y=df_dep_bornes['base100_bornes'],
        mode='lines+markers',
        name='Bornes électriques',
        line=dict(color='#d1c4e9 ')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution comparée des véhicules et bornes électriques dans le département {departement_selectionne}",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Évolution (base 100)",
        legend=dict(x=0.02, y=0.98),
    )

    return fig

def barplot_top_regions_ve(df, annee_selectionnee):
    top_regions = (
        df[df['Annee'] == annee_selectionnee]
        .groupby('region')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
        .sort_values(by='NB_VP_RECHARGEABLES_EL', ascending=False)
        .head(10)
    )

    top_regions = top_regions.rename(columns={'NB_VP_RECHARGEABLES_EL': 'Nombre de véhicules électriques', 'region': 'Région'})

    fig = px.bar(
        top_regions,
        x='Nombre de véhicules électriques',
        y='',
        orientation='h',
        text_auto=True,
        title=f"Top 10 régions par nombre de véhicules électriques ({annee_selectionnee})",
        color_discrete_sequence=["#4a148c"]
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        template='simple_white',
        height=500
    )

    return fig

def barplot_bottom_regions_ve(df, annee_selectionnee):
    bottom_regions = (
        df[df['Annee'] == annee_selectionnee]
        .groupby('region')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
        .sort_values(by='NB_VP_RECHARGEABLES_EL', ascending=True)
        .head(10)
    )

    bottom_regions = bottom_regions.rename(columns={'NB_VP_RECHARGEABLES_EL': 'Nombre de véhicules électriques', 'region': 'Région'})

    fig = px.bar(
        bottom_regions,
        x='Nombre de véhicules électriques',
        y='',
        orientation='h',
        text_auto=True,
        title=f"Top 10 régions avec le moins de véhicules électriques ({annee_selectionnee})",
        color_discrete_sequence=["#4a148c"]
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        template='simple_white',
        height=500
    )

    return fig

def barplot_bottom_departements_ve(df, annee_selectionnee):
    bottom_departements = (
        df[df['Annee'] == annee_selectionnee]
        .groupby('departement')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
        .sort_values(by='NB_VP_RECHARGEABLES_EL', ascending=True)
        .head(10)
    )

    bottom_departements = bottom_departements.rename(columns={'NB_VP_RECHARGEABLES_EL': 'Nombre de véhicules électriques', 'departement': 'Département'})

    fig = px.bar(
        bottom_departements,
        x='Nombre de véhicules électriques',
        y='',
        orientation='h',
        text_auto=True,
        title=f"Top 10 départements avec le moins de véhicules électriques ({annee_selectionnee})",
        color_discrete_sequence=["#9575cd"]
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        template='simple_white',
        height=500
    )

    return fig


def barplot_top_departements_ve(df, annee_selectionnee):
    top_departements = (
        df[df['Annee'] == annee_selectionnee]
        .groupby('departement')['NB_VP_RECHARGEABLES_EL']
        .sum()
        .reset_index()
        .sort_values(by='NB_VP_RECHARGEABLES_EL', ascending=False)
        .head(10)
    )

    top_departements = top_departements.rename(columns={'NB_VP_RECHARGEABLES_EL': 'Nombre de véhicules électriques', 'departement': 'Département'})

    fig = px.bar(
        top_departements,
        x='Nombre de véhicules électriques',
        y='',
        orientation='h',
        text_auto=True,
        title=f"Top 10 départements avec le plus de véhicules électriques ({annee_selectionnee})",
        color_discrete_sequence=["#9575cd"]
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        template='simple_white',
        height=500
    )

    return fig

def barplot_bornes_regions(df_2, choix_classement, annee_selectionnee_b):
    # Filtrer les données pour l'année sélectionnée
    df_bornes_filtre = df_2[df_2['Annee'] == annee_selectionnee_b]

    # Regrouper les données par région et calculer la somme des bornes
    top_regions_bornes = df_bornes_filtre.groupby('nom_region')['nb_borne'].sum().reset_index()

    # Trier les régions en fonction du choix (Top 10 ou Flop 10)
    if choix_classement == "Top 10":
        top_regions_bornes = top_regions_bornes.sort_values(by='nb_borne', ascending=False).head(10)
        titre = f"Top 10 régions par nombre de bornes de recharge ({annee_selectionnee_b})"
    else:
        top_regions_bornes = top_regions_bornes.sort_values(by='nb_borne', ascending=True).head(10)
        titre = f"Flop 10 régions par nombre de bornes de recharge ({annee_selectionnee_b})"

    # Créer le barplot avec Plotly Express
    fig = px.bar(
        top_regions_bornes,
        y='nom_region',
        x='nb_borne',
        orientation='h',
        text_auto=True,
        title=titre,
        labels={'nom_region': 'Région', 'nb_borne': 'Nombre de bornes de recharge'},
        color_discrete_sequence=["#4a148c"]
    )

    # Mise en page du graphique
    fig.update_layout(template='simple_white', yaxis=dict(autorange="reversed"))

    return fig


def barplot_bornes_departements(df_2, choix_classement, annee_selectionnee_b):
    # Filtrer les données pour l'année sélectionnée
    df_bornes_filtre = df_2[df_2['Annee'] == annee_selectionnee_b]

    # Regrouper les données par département et calculer la somme des bornes
    top_departements_bornes = df_bornes_filtre.groupby('nom_departement')['nb_borne'].sum().reset_index()

    # Trier les départements en fonction du choix (Top 10 ou Flop 10)
    if choix_classement == "Top 10":
        top_departements_bornes = top_departements_bornes.sort_values(by='nb_borne', ascending=False).head(10)
        titre = f"Top 10 départements par nombre de bornes de recharge ({annee_selectionnee_b})"
    else:
        top_departements_bornes = top_departements_bornes.sort_values(by='nb_borne', ascending=True).head(10)
        titre = f"Flop 10 départements par nombre de bornes de recharge ({annee_selectionnee_b})"

    # Créer le barplot avec Plotly Express
    fig = px.bar(
        top_departements_bornes,
        y='nom_departement',
        x='nb_borne',
        orientation='h',
        text_auto=True,
        title=titre,
        labels={'nom_departement': 'Département', 'nb_borne': 'Nombre de bornes de recharge'},
        color_discrete_sequence=["#9575cd "]
    )

    # Mise en page du graphique
    fig.update_layout(template='simple_white', yaxis=dict(autorange="reversed"))

    return fig

def vignette_borne_instal_fr(df_2, annee):
    # Filtrer les données pour l'année sélectionnée uniquement
    df_filtre = df_2[df_2["Annee"] == annee]

    if not df_filtre.empty:
        nb_borne = df_filtre["nb_borne"].sum()

        # Initialisation de la valeur précédente
        previous_nb_borne = None

        # Calculer la variation par rapport à l'année précédente
        df_precedent = df_2[df_2["Annee"] == annee - 1]
        if not df_precedent.empty:
            previous_nb_borne = df_precedent["nb_borne"].sum()
            
            # Vérifier si previous_nb_borne est valide avant de calculer la variation
            if previous_nb_borne > 0:
                variation = ((nb_borne - previous_nb_borne) / previous_nb_borne) * 100
                color = "green" if variation > 0 else "red"
            else:
                variation = None
                color = "white"
        else:
            variation = None
            color = "white"
    else:
        return None  # Retourner None si aucune donnée n'est disponible

    # Création du graphique avec Plotly
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=nb_borne,
        title={"text": f"<span style='color:white'>Bornes de recharge installées en France</span>"},
        delta={
            "reference": previous_nb_borne,
            "relative": True,
            "valueformat": ".2%"
        } if previous_nb_borne else None,
        number={"font": {"color": color, "size": 50}, "valueformat": ".3s"}
    ))

    fig.update_layout(
        height=150,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='#4a148c'
    )

    return fig

def barplot_bornes_regions_tot(df_2, choix_classement, annee_selectionnee_b):
    # Filtrer les données pour l'année sélectionnée
    df_bornes_filtre = df_2[df_2['Annee'] <= annee_selectionnee_b]

    # Regrouper les données par région et calculer la somme des bornes
    top_regions_bornes = df_bornes_filtre.groupby('nom_region')['nb_borne'].sum().reset_index()

    # Trier les régions en fonction du choix (Top 10 ou Flop 10)
    if choix_classement == "Top 10":
        top_regions_bornes = top_regions_bornes.sort_values(by='nb_borne', ascending=False).head(10)
        titre = f"Top 10 régions par nombre de bornes de recharge ({annee_selectionnee_b})"
    else:
        top_regions_bornes = top_regions_bornes.sort_values(by='nb_borne', ascending=True).head(10)
        titre = f"Flop 10 régions par nombre de bornes de recharge ({annee_selectionnee_b})"

    # Créer le barplot avec Plotly Express
    fig = px.bar(
        top_regions_bornes,
        y='nom_region',
        x='nb_borne',
        orientation='h',
        text_auto=True,
        title=titre,
        labels={'nom_region': 'Région', 'nb_borne': 'Nombre de bornes de recharge'},
        color_discrete_sequence=["#4a148c"]
    )

    # Mise en page du graphique
    fig.update_layout(template='simple_white', yaxis=dict(autorange="reversed"))

    return fig


def barplot_bornes_departements_tot(df_2, choix_classement, annee_selectionnee_b):
    # Filtrer les données pour l'année sélectionnée
    df_bornes_filtre = df_2[df_2['Annee'] <= annee_selectionnee_b]

    # Regrouper les données par département et calculer la somme des bornes
    top_departements_bornes = df_bornes_filtre.groupby('nom_departement')['nb_borne'].sum().reset_index()

    # Trier les départements en fonction du choix (Top 10 ou Flop 10)
    if choix_classement == "Top 10":
        top_departements_bornes = top_departements_bornes.sort_values(by='nb_borne', ascending=False).head(10)
        titre = f"Top 10 départements par nombre de bornes de recharge ({annee_selectionnee_b})"
    else:
        top_departements_bornes = top_departements_bornes.sort_values(by='nb_borne', ascending=True).head(10)
        titre = f"Flop 10 départements par nombre de bornes de recharge ({annee_selectionnee_b})"

    # Créer le barplot avec Plotly Express
    fig = px.bar(
        top_departements_bornes,
        y='nom_departement',
        x='nb_borne',
        orientation='h',
        text_auto=True,
        title=titre,
        labels={'nom_departement': 'Département', 'nb_borne': 'Nombre de bornes de recharge'},
        color_discrete_sequence=["#9575cd "]
    )

    fig.update_layout(template='simple_white', yaxis=dict(autorange="reversed"))

    return fig

def graphique_evolution_ve_region(df, region):
    df_reg_evol = df[df['region'] == region].groupby('Annee')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_reg_evol['Annee'],
        y=df_reg_evol['NB_VP_RECHARGEABLES_EL'],
        mode='lines+markers',
        name="Véhicules électriques",
        line=dict(color='#9575cd ')
    ))

    fig.update_layout(
        title={
            'text': f"🚗 Évolution des véhicules électriques – {region}",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Nombre de véhicules",
        font=dict(color="white"),
    )

    return fig

def graphique_evolution_ve_departement(df, departement):
    df_dep_evol = df[df['departement'] == departement].groupby('Annee')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_dep_evol['Annee'],
        y=df_dep_evol['NB_VP_RECHARGEABLES_EL'],
        mode='lines+markers',
        name="Véhicules électriques",
        line=dict(color='#9575cd ')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution des véhicules électriques – {departement}",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Nombre de véhicules",
        font=dict(color="white"),
  
    )

    return fig

def camembert_repartition_motorisation(df, annee, niveau, valeur):
    # Filtrer selon le niveau
    if niveau == "Région":
        df_filtre = df[(df['Annee'] == annee) & (df['region'] == valeur)]
    elif niveau == "Département":
        df_filtre = df[(df['Annee'] == annee) & (df['departement'] == valeur)]
    elif niveau == "France":
        df_filtre = df[df['Annee'] == annee]
    else:
        return None

    if df_filtre.empty:
        return None

    # Agréger les données
    total_ve = df_filtre["NB_VP_RECHARGEABLES_EL"].sum()
    total_gaz = df_filtre["NB_VP_RECHARGEABLES_GAZ"].sum()
    total_vehicules = df_filtre["NB_VP"].sum()
    total_thermique = total_vehicules - (total_ve + total_gaz)

    parts = {
        "Électrique": total_ve,
        "Gaz": total_gaz,
        "Thermique": total_thermique if total_thermique > 0 else 0
    }

    fig = px.pie(
        names=list(parts.keys()),
        values=list(parts.values()),
        title=f"Répartition des types de véhicules – {valeur} ({annee})",
        color_discrete_sequence=["#d1c4e9", "#ab47bc", "#512da8"]  
    )

    fig.update_traces(textinfo="percent+label")
    fig.update_layout(
    )

    return fig

def graphique_evolution_ve_region_pred(df, region):
    # Données réelles
    df_reg_evol = df[df['region'] == region].groupby('Annee')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

    # Régression linéaire sur les données existantes
    X = df_reg_evol['Annee']
    y = df_reg_evol['NB_VP_RECHARGEABLES_EL']
    coeffs = np.polyfit(X, y, deg=1)

    # Générer prédiction jusqu’à 2030
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred + coeffs[1]

    # Création du graphique
    fig = go.Figure()

    # Courbe réelle
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Véhicules électriques réels",
        line=dict(color='royalblue')
    ))

    # Courbe prédite
    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Projection jusqu'à 2030",
        line=dict(dash='dash', color='#8e24aa')
    ))

    # Mise en page
    fig.update_layout(
        title={
            'text': f"🚗 Évolution des véhicules électriques – {region} (avec projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="Année",
        yaxis_title="Nombre de véhicules",
    )

    return fig

def graphique_evolution_ve_departement_pred(df, departement):
    # Filtrer les données pour le département
    df_dep_evol = df[df['departement'] == departement].groupby('Annee')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

    # Régression linéaire
    X = df_dep_evol['Annee']
    y = df_dep_evol['NB_VP_RECHARGEABLES_EL']
    coeffs = np.polyfit(X, y, deg=1)

    # Prédiction jusqu'en 2030
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred + coeffs[1]

    # Figure
    fig = go.Figure()

    # Courbe réelle
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Véhicules électriques réels",
        line=dict(color='royalblue')
    ))

    # Courbe prédite
    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Tendance jusqu'à 2030",
        line=dict(dash='dash', color='#8e24aa')
    ))

    fig.update_layout(
        title={
            'text': f"📈 Évolution des véhicules électriques – {departement} (avec projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="Année",
        yaxis_title="Nombre de véhicules",
    )

    return fig


def graphique_evolution_france_ve_pred(df):
    # Données réelles
    df_france_evol = df.groupby('Annee')['NB_VP_RECHARGEABLES_EL'].sum().reset_index()

    # Régression linéaire
    X = df_france_evol['Annee']
    y = df_france_evol['NB_VP_RECHARGEABLES_EL']
    coeffs = np.polyfit(X, y, deg=1)

    # Générer les années jusqu'en 2030
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred + coeffs[1]

    # Création du graphique
    fig = go.Figure()

    # Données réelles
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Véhicules électriques réels",
        line=dict(color='royalblue')
    ))

    # Projection
    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Projection jusqu'à 2030",
        line=dict(dash='dash', color='#8e24aa')
    ))

    # Layout
    fig.update_layout(
        title="📈 Évolution des véhicules électriques en France (avec projection 2030)",
        xaxis_title="Année",
        yaxis_title="Nombre de véhicules",

    )

    return fig



def graphique_evolution_bornes_region_pred(df_2, region):
    # Filtrer les données
    df_reg_evol = df_2[
        (df_2['nom_region'] == region) &
        (df_2['Annee'] >= 2010) &
        (df_2['Annee'] != 2025)
    ].groupby('Annee')['nb_borne'].sum().reset_index()

    if df_reg_evol.empty or len(df_reg_evol) < 3:
        return None  # Trop peu de points pour une régression quadratique

    # Cumul
    df_reg_evol['nb_borne'] = df_reg_evol['nb_borne'].cumsum()

    # Régression quadratique
    X = df_reg_evol['Annee']
    y = df_reg_evol['nb_borne']
    coeffs = np.polyfit(X, y, deg=2)

    # Projection
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred**2 + coeffs[1] * annees_pred + coeffs[2]

    # Création du graphique
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Bornes installées (cumul)",
        line=dict(color='orange')
    ))

    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Projection jusqu'à 2030",
        line=dict(dash='dash', color='#8e24aa ')
    ))

    fig.update_layout(
        title={
            'text': f"🔌 Évolution des bornes – {region} (avec projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="Année",
        yaxis_title="Nombre de bornes",
    )

    return fig




def graphique_evolution_bornes_france_pred(df_2):
    df_france_evol = df_2[(df_2['Annee'] >= 2010) & (df_2['Annee'] != 2025)].groupby('Annee')['nb_borne'].sum().reset_index()
    
    df_france_evol['nb_borne'] = df_france_evol['nb_borne'].cumsum()

    X = df_france_evol['Annee']
    y = df_france_evol['nb_borne']
    coeffs = np.polyfit(X, y, deg=2)

    # Projection jusqu'à 2030 avec le modèle polynomial
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred**2 + coeffs[1] * annees_pred + coeffs[2]

    # Création du graphique
    fig = go.Figure()

    # Données réelles
    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Bornes installées (cumul)",
        line=dict(color='orange')
    ))

    # Projection
    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Projection jusqu'à 2030",
        line=dict(dash='dash', color='#8e24aa')
    ))

    # Mise en forme
    fig.update_layout(
        title={
            'text': "🔌 Évolution des bornes en France (avec projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="Année",
        yaxis_title="Nombre de bornes",
    )

    return fig


def graphique_evolution_bornes_dep_pred(df_2, departement):
    df_dep_evol = df_2[
        (df_2['nom_departement'] == departement) &
        (df_2['Annee'] >= 2010) &
        (df_2['Annee'] != 2025)
    ].groupby('Annee')['nb_borne'].sum().reset_index()

    if df_dep_evol.empty or len(df_dep_evol) < 3:
        return None  

    df_dep_evol['nb_borne'] = df_dep_evol['nb_borne'].cumsum()

    X = df_dep_evol['Annee']
    y = df_dep_evol['nb_borne']

    if X.empty or y.empty:
        return None  

    coeffs = np.polyfit(X, y, deg=2)
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred**2 + coeffs[1] * annees_pred + coeffs[2]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X, y=y, mode='lines+markers', name="Bornes installées (cumul)", line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=annees_pred, y=prediction, mode='lines', name="Projection jusqu'à 2030", line=dict(dash='dash', color='#8e24aa ')))

    fig.update_layout(
        title={
            'text': f"🔌 Évolution des bornes – {departement} (avec projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Nombre de bornes"
    )

    return fig

def graphique_evolution_france_vpb(df_ve_b):
    df_france_evol = df_ve_b.groupby('Annee')['nb_el/borne'].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_france_evol['Annee'], 
        y=df_france_evol['nb_el/borne'], 
        mode='lines+markers',
        line=dict(color='#5c6bc0')
        
    ))

    fig.update_layout(
        title="Évolution des véhicules par borne en France",
        xaxis_title="",
        yaxis_title="Véhicules/borne"
        )

    return fig

def graphique_evolution_vpb_region(df_ve_b, region):
    df_reg_evol = df_ve_b[df_ve_b['nom_region'] == region].groupby('Annee')['nb_el/borne'].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_reg_evol['Annee'],
        y=df_reg_evol['nb_el/borne'],
        mode='lines+markers',
        name="Véhicules électriques",
        line=dict(color='#5c6bc0')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution des véhicules par borne – {region}",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Véhicules/borne",
        font=dict(color="white"),
    )

    return fig

def graphique_evolution_vpb_dep(df_ve_b, departement):
    df_dep_evol = df_ve_b[df_ve_b['nom_departement'] == departement].groupby('Annee')['nb_el/borne'].mean().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_dep_evol['Annee'],
        y=df_dep_evol['nb_el/borne'],
        mode='lines+markers',
        name="Véhicules électriques",
        line=dict(color='#5c6bc0')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution des véhicules par borne – {departement}",
            'font': {'size': 15}
        },
        xaxis_title="",
        yaxis_title="Véhicules/borne",
        font=dict(color="white"),
  
    )

    return fig


from scipy.optimize import curve_fit

def modele_exponentiel(x, a, b, c):
    return a * np.exp(-b * x)

def graphique_evolution_france_vpb_pred(df_ve_b):
    df_france_evol = df_ve_b.groupby('Annee')['nb_el/borne'].mean().reset_index()

    X = df_france_evol['Annee'].values
    y = df_france_evol['nb_el/borne'].values

    if len(X) < 3:
        return None

    # Centrer les années pour éviter des valeurs trop grandes
    X_centered = X - X.min()

    # Ajustement du modèle exponentiel décroissant
    try:
        popt, _ = curve_fit(modele_exponentiel, X_centered, y, maxfev=10000)
        a, b, c = popt
    except RuntimeError:
        return None  # Si l'ajustement échoue

    # Prédiction jusqu’en 2030
    annees_pred = np.arange(X.min(), 2031)
    X_pred_centered = annees_pred - X.min()
    y_pred = modele_exponentiel(X_pred_centered, a, b, c)

    # Création du graphique
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Historique",
        line=dict(color='royalblue')
    ))

    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=y_pred,
        mode='lines',
        name="Projection jusqu’à 2030",
        line=dict(dash='dash', color='#8e24aa ')
    ))

    fig.update_layout(
        title="📈 Évolution des véhicules par borne en France (projection 2030)",
        xaxis_title="Année",
        yaxis_title="Véhicules / borne"
    )

    return fig

def graphique_evolution_vpb_region_pred(df_ve_b, region):
    df_reg_evol = df_ve_b[df_ve_b['nom_region'] == region].groupby('Annee')['nb_el/borne'].mean().reset_index()

    X = df_reg_evol['Annee']
    y = df_reg_evol['nb_el/borne']

    if len(X) < 3:
        return None  

    coeffs = np.polyfit(X, y, deg=1)
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred + coeffs[1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Historique",
        line=dict(color='#388e3c')
    ))

    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Projection jusqu'à 2030",
        line=dict(color='#8e24aa', dash='dash')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution des véhicules par borne – {region} (projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="Année",
        yaxis_title="Véhicules / borne"
    )

    return fig

def graphique_evolution_vpb_dep_pred(df_ve_b, departement):
    df_dep_evol = df_ve_b[df_ve_b['nom_departement'] == departement].groupby('Annee')['nb_el/borne'].mean().reset_index()

    X = df_dep_evol['Annee']
    y = df_dep_evol['nb_el/borne']

    if len(X) < 3:
        return None

    coeffs = np.polyfit(X, y, deg=1)
    annees_pred = np.arange(X.min(), 2031)
    prediction = coeffs[0] * annees_pred + coeffs[1]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=X,
        y=y,
        mode='lines+markers',
        name="Historique",
        line=dict(color='#388e3c')
    ))

    fig.add_trace(go.Scatter(
        x=annees_pred,
        y=prediction,
        mode='lines',
        name="Projection jusqu'à 2030",
        line=dict(color='#8e24aa', dash='dash')
    ))

    fig.update_layout(
        title={
            'text': f"Évolution des véhicules par borne – {departement} (projection 2030)",
            'font': {'size': 15}
        },
        xaxis_title="Année",
        yaxis_title="Véhicules / borne"
    )

    return fig

