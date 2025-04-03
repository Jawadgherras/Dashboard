import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import branca.colormap as cm

df=pd.read_csv('Projet/data/data_TMJA/tmja-departement-mean.csv')
df.info()
df.head()
df["departement"].unique()

departement_geojson=gpd.read_file('Projet/data/data_TMJA/departement.geojson')
departement_geojson.info()
departement_geojson.head()

departement_geojson['nom'] = departement_geojson['nom'].str.strip().str.lower()
df['departement'] = df['departement'].str.strip().str.lower()

dep_tmja=departement_geojson.merge(df, left_on='nom', right_on='departement')

dep_tmja.info()

carte_dep_tmja = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

geojson_data = dep_tmja.to_json()

Choropleth(
    geo_data=geojson_data,  
    name='choropleth',
    data=dep_tmja,
    columns=['departement', 'TMJA'],  
    key_on='feature.properties.nom',  
    fill_color='YlOrRd',  
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='TMJA par département'
).add_to(carte_dep_tmja)


for _, row in dep_tmja.iterrows():
    popup_text = f"Département : {row['nom']}<br>TMJA : {row['TMJA']}"
    folium.GeoJsonPopup(fields=['nom', 'TMJA'], aliases=['departement', 'TMJA'], localize=True).add_to(folium.GeoJson(row['geometry'], popup=popup_text).add_to(carte_dep_tmja))

folium.LayerControl().add_to(carte_dep_tmja)

carte_dep_tmja.save('Projet/data/data_TMJA/Carte_dep_TMJA.html')



import pandas as pd
import geopandas as gpd
import folium
from folium import Choropleth
import json

# Charger les données
df = pd.read_csv('Projet/data/data_TMJA/tmja-departement-mean.csv')
departement_geojson = gpd.read_file('Projet/data/data_TMJA/departement.geojson')

# Assurer que les noms des départements sont normalisés
departement_geojson['nom'] = departement_geojson['nom'].str.strip().str.lower()
df['departement'] = df['departement'].str.strip().str.lower()

# Fusionner les données géographiques avec les données TMJA
dep_tmja = departement_geojson.merge(df, left_on='nom', right_on='departement')

# Convertir en GeoJSON
geojson_data = dep_tmja.to_json()

# Créer une carte Folium
carte_dep_tmja = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

# Vérification de la structure du GeoJSON pour debug
print(json.dumps(geojson_data)[:500])  # Affiche les 500 premiers caractères du GeoJSON

# Ajouter une carte choroplèthe
Choropleth(
    geo_data=geojson_data,  # Utilisation du GeoJSON correctement formaté
    name='choropleth',
    data=dep_tmja,
    columns=['departement', 'TMJA'],
    key_on='feature.properties.nom',  # Utilisation correcte de la clé dans le GeoJSON
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='TMJA par département'
).add_to(carte_dep_tmja)

# Ajouter des popups pour chaque département
for _, row in dep_tmja.iterrows():
    popup_text = f"Département : {row['nom']}<br>TMJA : {row['TMJA']}"
    folium.GeoJsonPopup(
        fields=['nom', 'TMJA'],
        aliases=['Département', 'TMJA'],
        localize=True
    ).add_to(folium.GeoJson(row['geometry'], popup=popup_text).add_to(carte_dep_tmja))

# Ajouter le contrôle de couche
folium.LayerControl().add_to(carte_dep_tmja)

# Sauvegarder la carte
carte_dep_tmja.save('Projet/data/data_TMJA/Carte_dep_TMJA.html')



##############################Carte des départements############################################



url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
departements = gpd.read_file(url_geojson)

dep_tmja=pd.read_csv('Projet/data/data_TMJA/tmja-departement-mean.csv')

departements = departements.merge(dep_tmja, left_on="nom", right_on="departement", how="left")

missing = departements[departements["TMJA"].isna()]
if not missing.empty:
    print("⚠️ Attention ! Certains départements n'ont pas été trouvés dans le fichier CSV :")
    print(missing["nom"].tolist())

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

min_tmja, max_tmja = departements["TMJA"].min(), departements["TMJA"].max()
colormap = cm.LinearColormap(colors=['#F3E5F5', '#240046', '#2a1b6a'], vmin=min_tmja, vmax=max_tmja, caption="TMJA par département")

folium.GeoJson(
    departements,
    name="TMJA",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["TMJA"]) if feature["properties"]["TMJA"] else "lightgray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom", "TMJA"], aliases=["Département", "TMJA"], localize=True),
).add_to(m)

colormap.add_to(m)

m.save("Projet/data/data_TMJA/carte_dep_tmja.html")


###########################Carte des régions###############################################
url_geojson = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson"

regions = gpd.read_file(url_geojson)
regions["nom"].unique()

df_tmja = pd.read_csv("Projet/data/data_TMJA/tmja-region-mean.csv")
df_tmja["region"].unique()

regions = regions.merge(df_tmja, left_on="nom", right_on="region", how="left")

missing = regions[regions["TMJA"].isna()]
if not missing.empty:
    print("⚠️ Certaines régions ne sont pas trouvées dans le fichier CSV :", missing["nom"].tolist())

m = folium.Map(location=[46.603354, 1.888334], zoom_start=5)

min_tmja, max_tmja = regions["TMJA"].min(), regions["TMJA"].max()
colormap = cm.LinearColormap(colors=['#F3E5F5', '#240046', '#2a1b6a'], vmin=min_tmja, vmax=max_tmja, caption="TMJA par région")

folium.GeoJson(
    regions,
    name="TMJA",
    style_function=lambda feature: {
        "fillColor": colormap(feature["properties"]["TMJA"]) if feature["properties"]["TMJA"] else "lightgray",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=["nom", "TMJA"], aliases=["Région", "TMJA"], localize=True),
).add_to(m)

colormap.add_to(m)

m.save("Projet/data/data_TMJA/carte_region_tmja.html")
