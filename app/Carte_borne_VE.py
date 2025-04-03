import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import branca.colormap as cm


###Carte des départements
data=pd.read_csv('Projet/data/data_VE/data_VE_bornes_annee_dep.csv')
data.info()
annee_selectionnee = 2024
#data=data[data["Annee"]==annee_selectionnee]
#data[data["departement"]=="Maine-et-Loire"]
#data[data["departement"]=="Haute-Corse"]

url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
departements = gpd.read_file(url_geojson)
departements.info()


departements = departements.merge(data, left_on="nom", right_on="departement", how="left")

missing = departements[departements["nb_el/borne"].isna()]
if not missing.empty:
    print("⚠️ Attention ! Certains départements n'ont pas été trouvés dans le fichier CSV :")
    print(missing["nom"].tolist())

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

min_nb_el_borne, max_nb_el_borne = departements["nb_el/borne"].min(), departements["nb_el/borne"].max()


colormap = cm.LinearColormap(colors=['green', 'yellow', 'red'], vmin=min_nb_el_borne, vmax=max_nb_el_borne, caption=f"nb_el/borne par département en {annee_selectionnee}") 

folium.GeoJson(
    departements,
    name="TMJA",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["nb_el/borne"]) if feature["properties"]["nb_el/borne"] else "lightgray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom", "nb_el/borne"], aliases=["Département", "nb_el/borne"], localize=True),
).add_to(m)

colormap.add_to(m)

m.save(f"Projet/data/data_VE/carte_dep_nb_el_borne_{annee_selectionnee}.html")





##############################Carte des régions

###Carte des départements
data=pd.read_csv('Projet/data/data_VE/data_VE_bornes_annee_modif.csv')
data.info()
data.head(60)
annee_selectionnee = 2020
data=data[data["Annee"]==annee_selectionnee]
#data[data["departement"]=="Maine-et-Loire"]
#data[data["departement"]=="Haute-Corse"]

url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"
regions = gpd.read_file(url_geojson)
regions.info()
regions


regions = regions.merge(data, left_on="nom", right_on="region", how="left")
regions.info()

missing = regions[regions["nb_el/borne"].isna()]
if not missing.empty:
    print("⚠️ Attention ! Certains départements n'ont pas été trouvés dans le fichier CSV :")
    print(missing["nom"].tolist())

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

min_nb_el_borne, max_nb_el_borne = regions["nb_el/borne"].min(), regions["nb_el/borne"].max()


colormap = cm.LinearColormap(colors=['green', 'yellow', 'red'], vmin=min_nb_el_borne, vmax=max_nb_el_borne, caption=f"nb_el/borne par régions en {annee_selectionnee}") 

folium.GeoJson(
    regions,
    name="TMJA",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["nb_el/borne"]) if feature["properties"]["nb_el/borne"] else "lightgray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom", "nb_el/borne"], aliases=["region", "nb_el/borne"], localize=True),
).add_to(m)

colormap.add_to(m)

m.save(f"Projet/data/data_VE/carte_reg_nb_el_borne_{annee_selectionnee}.html")