import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import branca.colormap as cm

####Carte des bornes par département

data_dep_bornes = pd.read_csv('Projet/data/data_bornes/departement_annee_cum.csv')
data_dep_bornes.info()
annee_selectionnee = 2024
data_dep=data_dep_bornes[data_dep_bornes["annee_mise_en_service"]==annee_selectionnee]

url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
departements = gpd.read_file(url_geojson)
departements.info()

departements = departements.merge(data_dep, left_on="nom", right_on="depart", how="left")

missing = departements[departements["cumsum_borne"].isna()]
if not missing.empty:
    print("⚠️ Attention ! Certains départements n'ont pas été trouvés dans le fichier CSV :")
    print(missing["nom"].tolist())

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)


min_bornes, max_bornes = departements["cumsum_borne"].min(), departements["cumsum_borne"].max()

colormap = cm.LinearColormap(colors=['red', 'yellow', 'green'], vmin=min_bornes, vmax=max_bornes, caption=f"Nombre de bornes par département en {annee_selectionnee}") 

folium.GeoJson(
    departements,
    name="cumsum_borne",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["cumsum_borne"]) if feature["properties"]["cumsum_borne"] else "lightgray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom", "cumsum_borne"], aliases=["Département", "Nombre de bornes"], localize=True),
).add_to(m)

colormap.add_to(m)

m.save(f"Projet/data/data_bornes/carte_dep_bornes_{annee_selectionnee}.html")




####Carte des bornes par régions

data_dep_bornes = pd.read_csv('Projet/data/data_bornes/region_annee_cum.csv')
data_dep_bornes.info()
annee_selectionnee = 2024
data_reg=data_dep_bornes[data_dep_bornes["annee_mise_en_service"]==annee_selectionnee]


url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"
regions = gpd.read_file(url_geojson)
regions.info()

regions = regions.merge(data_reg, left_on="nom", right_on="region", how="left")


missing = regions[regions["cumsum_borne"].isna()]
if not missing.empty:
    print("⚠️ Attention ! Certaines régions n'ont pas été trouvées dans le fichier CSV :")
    print(missing["nom"].tolist())

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)


min_bornes, max_bornes = regions["cumsum_borne"].min(), regions["cumsum_borne"].max()

colormap = cm.LinearColormap(colors=['#4527a0', '#7e57c2', '#d1c4e9'], vmin=min_bornes, vmax=max_bornes, caption=f"Nombre de bornes par region en {annee_selectionnee}") 

folium.GeoJson(
    regions,
    name="cumsum_borne",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["cumsum_borne"]) if feature["properties"]["cumsum_borne"] else "lightgray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom", "cumsum_borne"], aliases=["Région", "Nombre de bornes"], localize=True),
).add_to(m)

colormap.add_to(m)

m.save(f"Projet/data/data_bornes/carte_reg_bornes_{annee_selectionnee}.html")







