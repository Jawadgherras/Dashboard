import pandas as pd
import requests
from io import StringIO
import re
import numpy as np

data_bornes = pd.read_csv('Projet/data/data_bornes/bornes_brutes.csv')


URL_csv="https://www.data.gouv.fr/fr/datasets/r/eb76d20a-8501-400e-b336-d85724de5435"

response = requests.get(URL_csv)
if response.status_code == 200:
    data_bornes = pd.read_csv(StringIO(response.text)) 
else:
    raise Exception("Erreur lors du téléchargement des données")


def get_bornes():
    return data_bornes

data=get_bornes()
print(data)

len(data)

data.info()

len(data[data["consolidated_is_code_insee_verified"]==True])

data.loc[126163, ]

data["date_mise_en_service"]

data["date_mise_en_service"] =data["date_mise_en_service"].str.split().str[0]
data["date_mise_en_service"] = pd.to_datetime(data["date_mise_en_service"], format='%Y-%m-%d', errors='coerce')

#Date la plus ancienne et récente
data["date_mise_en_service"].min(), data["date_mise_en_service"].max()



################################ Traitement des donnees sans code insee ################################
#Regarder le code insee des communes
data_T=data[data["consolidated_is_code_insee_verified"]==True].copy()
data_T["code_insee_commune"]=data_T["code_insee_commune"].astype(str)

data_T_test=data_T[data_T["consolidated_code_postal"].isnull()].copy()

len(data_T)

data_code_insee=data_T.copy()

data_code_insee_test1=data_code_insee[data_code_insee["code_insee_commune"].isnull()]
data_code_insee_test2=data_code_insee[data_code_insee["code_insee_commune"].notnull()]

len(data_code_insee_test1), len(data_code_insee_test2)

data_T["adresse_station"].tail(10)

data_T.loc[126705,]

data_T["num_depart"]=data_T["code_insee_commune"].str[:2]
data_T["num_depart"].value_counts().unique()

data_T[data_T["num_depart"].isnull()]["code_insee_commune"]

data_T[data_T["num_depart"]=="75"][["code_insee_commune", "num_depart"]]


data_T.to_csv("Projet/data/data_bornes/data_T_modif.csv", index=False)









data_F=data[data["consolidated_is_code_insee_verified"]==False].copy()


data_F_test=data_F

data_F_test.info()

data_F_test["adresse_station"].tail(10)

data_F_test["code_insee_commune"].tail(10)

def extraction_num_dep(adresse_station):
    match = re.search(r'\b\d{5}\b', adresse_station)
    if match:
        return match.group()[:2]
    else:
        return None

data_F_test["num_depart"]=data_F_test["adresse_station"].apply(extraction_num_dep)

data_F_valide=data_F_test[data_F_test["num_depart"].notnull()]

data_F_valide.to_csv("Projet/data/data_bornes/data_F_valide.csv", index=False)

data_F_valide.head()

len(data_T)
len(data_F_valide)

len(data_T)+len(data_F_valide)


#Ajout de des donnees data_F dans le dataset data data_T
data_TTTTTT=pd.concat([data_T, data_F_valide])

data_TTTTTT=data_TTTTTT.reset_index(drop=True)

data_TTTTTT.tail(30)

len(data_TTTTTT)

data_TTTTTT.to_csv("Projet/data/data_bornes/data_valide_nondef_modif.csv", index=False)


################################ Stand-BY ################################

data_F_none=data_F_test[data_F_test["code_postal"].isnull()]

data_F_none.to_csv("Projet/data/data_bornes/data_F_none.csv", index=False)


data_F_none["adresse_station"].head(10)

data_F_none.loc[126622,]

data_test=data_F_none.copy()

data_test["adresse_station"]=data_test["adresse_station"].astype(str)


def extract_dept_from_address(adresse_station):
    match = re.search(r"\d{5}", adresse_station)
    if match:
        return match.group(1)[:2]  
    return None



#data_test["code_postal"]=data_test["adresse_station"].apply(extraction_code_postal)

data_test.loc[3674,]

data_test["code_postal"].unique()


data_commune=pd.read_csv("Projet/data/data_bornes/donnees_communes.csv", sep=";", dtype={"REG":str, "DEP":str, "Région":str, "COM":str, "Commune":str})

data_commune.info()

data_commune.head()

def extraction_num_dep_(ville):
    match = data_commune[data_commune["Commune"].str.lower() == ville.lower()]
    if not match.empty:
        match["departement"].values[0]  
    else:
        None

data_test["adresse_station"]

data_test["adresse_station"]

data_test.loc[126625, ]

################################ Stand-BY ################################

##Pour demain
#1. Revoir pour les data_F_none, solution pour récupérer les codes postaux
#2. Vérifier pour les data_valide_nondef_modif ✅
#3. Ajouter les colonnes nom_departement et nom_region dans le dataset data_valide_nondef_modif ✅
#4. Pour chaque bornes, la demultplier en plusieurs lignes pour plusieurs années 
#5. Pour le dataset data_valide_nondef_modif, faire la somme des bornes par département et par région pour chaque année


data_valide_nondef_modif=pd.read_csv("Projet/data/data_bornes/data_valide_nondef_modif.csv")

data_valide_nondef_modif['num_depart'] = data_valide_nondef_modif['num_depart'].astype(str)

departements ={'1': 'Ain', '2': 'Aisne', '3': 'Allier', '4': 'Alpes-de-Haute-Provence', '5': 'Hautes-Alpes',
             '6': 'Alpes-Maritimes', '7': 'Ardèche', '8': 'Ardennes', '9': 'Ariège', '10': 'Aube',
             '11': 'Aude', '12': 'Aveyron', '13': 'Bouches-du-Rhône', '14': 'Calvados', '15': 'Cantal',
             '16': 'Charente', '17': 'Charente-Maritime', '18': 'Cher', '19': 'Corrèze', '21': 'Côte-d\'Or',
             '22': 'Côtes-d\'Armor', '23': 'Creuse', '24': 'Dordogne', '25': 'Doubs', '26': 'Drôme',
             '27': 'Eure', '28': 'Eure-et-Loir', '29': 'Finistère', '2A': 'Corse-du-Sud', '2B': 'Haute-Corse',
             '30': 'Gard', '31':'Haute-Garonne', '32': 'Gers', '33': 'Gironde', '34': 'Hérault', '35': 'Ille-et-Vilaine',
             '36': 'Indre', '37': 'Indre-et-Loire', '38': 'Isère', '39': 'Jura', '40': 'Landes', '41': 'Loir-et-Cher',
             '42': 'Loire', '43': 'Haute-Loire', '44': 'Loire-Atlantique', '45': 'Loiret', '46': 'Lot', '47': 'Lot-et-Garonne',
             '48': 'Lozère', '49': 'Maine-et-Loire', '50': 'Manche', '51': 'Marne', '52': 'Haute-Marne', '53': 'Mayenne',
             '54': 'Meurthe-et-Moselle', '55': 'Meuse', '56': 'Morbihan', '57': 'Moselle', '58': 'Nièvre', '59': 'Nord',
             '60': 'Oise', '61': 'Orne', '62': 'Pas-de-Calais', '63': 'Puy-de-Dôme', '64': 'Pyrénées-Atlantiques',
             '65': 'Hautes-Pyrénées', '66': 'Pyrénées-Orientales', '67': 'Bas-Rhin', '68': 'Haut-Rhin', '69': 'Rhône',
             '70': 'Haute-Saône', '71': 'Saône-et-Loire', '72': 'Sarthe', '73': 'Savoie', '74': 'Haute-Savoie',
             '75': 'Paris', '76': 'Seine-Maritime', '77': 'Seine-et-Marne', '78': 'Yvelines', '79': 'Deux-Sèvres',
             '80': 'Somme', '81': 'Tarn', '82': 'Tarn-et-Garonne', '83': 'Var', '84': 'Vaucluse', '85': 'Vendée',
             '86': 'Vienne', '87': 'Haute-Vienne', '88': 'Vosges', '89': 'Yonne', '90': 'Territoire de Belfort',
             '91': 'Essonne', '92': 'Hauts-de-Seine', '93': 'Seine-Saint-Denis', '94': 'Val-de-Marne', '95': 'Val-d\'Oise'
             }

regions = {
    '1': 'Auvergne-Rhône-Alpes', '2': 'Hauts-de-France', '3': 'Auvergne-Rhône-Alpes',
    '4': 'Provence-Alpes-Côte d\'Azur', '5': 'Provence-Alpes-Côte d\'Azur', '6': 'Provence-Alpes-Côte d\'Azur',
    '7': 'Auvergne-Rhône-Alpes', '8': 'Grand Est', '9': 'Occitanie', '10': 'Grand Est',
    '11': 'Occitanie', '12': 'Occitanie', '13': 'Provence-Alpes-Côte d\'Azur',
    '14': 'Normandie', '15': 'Auvergne-Rhône-Alpes', '16': 'Nouvelle-Aquitaine',
    '17': 'Nouvelle-Aquitaine', '18': 'Centre-Val de Loire', '19': 'Nouvelle-Aquitaine',
    '21': 'Bourgogne-Franche-Comté', '22': 'Bretagne', '23': 'Nouvelle-Aquitaine',
    '24': 'Nouvelle-Aquitaine', '25': 'Bourgogne-Franche-Comté', '26': 'Auvergne-Rhône-Alpes',
    '27': 'Normandie', '28': 'Centre-Val de Loire', '29': 'Bretagne', '2A': 'Corse', '2B': 'Corse',
    '30': 'Occitanie', '31': 'Occitanie', '32': 'Occitanie', '33': 'Nouvelle-Aquitaine',
    '34': 'Occitanie', '35': 'Bretagne', '36': 'Centre-Val de Loire', '37': 'Centre-Val de Loire',
    '38': 'Auvergne-Rhône-Alpes', '39': 'Bourgogne-Franche-Comté', '40': 'Nouvelle-Aquitaine',
    '41': 'Centre-Val de Loire', '42': 'Auvergne-Rhône-Alpes', '43': 'Auvergne-Rhône-Alpes',
    '44': 'Pays de la Loire', '45': 'Centre-Val de Loire', '46': 'Occitanie', '47': 'Nouvelle-Aquitaine',
    '48': 'Occitanie', '49': 'Pays de la Loire', '50': 'Normandie', '51': 'Grand Est',
    '52': 'Grand Est', '53': 'Pays de la Loire', '54': 'Grand Est', '55': 'Grand Est',
    '56': 'Bretagne', '57': 'Grand Est', '58': 'Bourgogne-Franche-Comté', '59': 'Hauts-de-France',
    '60': 'Hauts-de-France', '61': 'Normandie', '62': 'Hauts-de-France', '63': 'Auvergne-Rhône-Alpes',
    '64': 'Nouvelle-Aquitaine', '65': 'Occitanie', '66': 'Occitanie', '67': 'Grand Est',
    '68': 'Grand Est', '69': 'Auvergne-Rhône-Alpes', '70': 'Bourgogne-Franche-Comté',
    '71': 'Bourgogne-Franche-Comté', '72': 'Pays de la Loire', '73': 'Auvergne-Rhône-Alpes',
    '74': 'Auvergne-Rhône-Alpes', '75': 'Île-de-France', '76': 'Normandie', '77': 'Île-de-France',
    '78': 'Île-de-France', '79': 'Nouvelle-Aquitaine', '80': 'Hauts-de-France',
    '81': 'Occitanie', '82': 'Occitanie', '83': 'Provence-Alpes-Côte d\'Azur',
    '84': 'Provence-Alpes-Côte d\'Azur', '85': 'Pays de la Loire', '86': 'Nouvelle-Aquitaine',
    '87': 'Nouvelle-Aquitaine', '88': 'Grand Est', '89': 'Bourgogne-Franche-Comté',
    '90': 'Bourgogne-Franche-Comté', '91': 'Île-de-France', '92': 'Île-de-France',
    '93': 'Île-de-France', '94': 'Île-de-France', '95': 'Île-de-France', '2A': 'Corse-du-sud', '2B': 'Haute-Corse'
}

data_valide_nondef_modif["depart"]=data_valide_nondef_modif["num_depart"].map(departements)
data_valide_nondef_modif["region"]=data_valide_nondef_modif["num_depart"].map(regions)

data_valide_nondef_modif.info()


data_valide_nondef_modif[data_valide_nondef_modif["nom_amenageur"]=="QoWatt"][["nom_amenageur", "adresse_station", 'nbre_pdc', "id_pdc_itinerance",  "date_mise_en_service", "depart", "region"]].head(60)

data_valide_nondef_modif[data_valide_nondef_modif["num_depart"]=="28"][["nom_amenageur", ""]]

#Idée pour ce que je dois fair pour les colonnes des points de charges, si j'ai un nombre de lignes avec la meme adresse égale à nbr_pdc associé
#Alors je remplie la nouvelle colonne des points de charges avec le nombre de points de charges nbr_pdc et par année et je consorve donc une ligne par adresse et on fait les cumules si on a plusieurs années
#Si le nombre de lignes avec la meme adresse est différent alors je somme tous les nbre_pdc de chaque ligne avec la meme adresse et je remplie la nouvelle colonne des points de charges avec cette somme et par année et il me reste donc une ligne par adresse et on fait les cumules si on a plusieurs années
#D'abord on remplie les données des points et années puis on supprime les doublons pour avoir une ligne par adresse et par année

data_valide_nondef_modif2=data_valide_nondef_modif.copy()

data_valide_nondef_modif2.info()

data_valide_nondef_modif2["date_mise_en_service"] = pd.to_datetime(data_valide_nondef_modif2["date_mise_en_service"])

data_valide_nondef_modif2["annee_mise_en_service"] = data_valide_nondef_modif2["date_mise_en_service"].dt.year






###############################################
data_valide_nondef_modif2["nb_lignes"] = data_valide_nondef_modif2.groupby(["adresse_station", "annee_mise_en_service"])['adresse_station'].transform('count')
#data_valide_nondef_modif2["nb_bornes"] = data_valide_nondef_modif2.groupby(["adresse_station", "annee_mise_en_service"])['adresse_station'].transform('count')

#data["nb_bornes"] = data.apply(lambda row: row["nbre_pdc"] if row["nb_lignes"] == row["nbre_pdc"] else row["nbre_pdc"].max(), axis=1)

def nb_bornes(group):
    if (group["nbre_pdc"] == 1).all():
        return group["nbre_pdc"].sum()
    elif len(group) == group["nbre_pdc"].iloc[0]:
        return group["nbre_pdc"]
    else:
        return group["nbre_pdc"].max()

data_valide_nondef_modif2 = data_valide_nondef_modif2.groupby(["adresse_station", "annee_mise_en_service"], as_index=False).apply(nb_bornes)
data_valide_nondef_modif2.columns = ["adresse_station", "annee_mise_en_service", "nb_bornes"]

data_valide_nondef_modif2["nb_bornes_cum"] = data_valide_nondef_modif2.groupby("adresse_station")["nb_bornes"].cumsum()
data_valide_nondef_modif2.info()


data_valide_nondef_modif2

###############################################OU 

#data_valide_nondef_modif2["nb_bornes"] = data_valide_nondef_modif2.apply(lambda row: row["nbre_pdc"] if row["nb_lignes"] == row["nbre_pdc"] else row["nbre_pdc"].max(), axis=1)

#data_agg = data_valide_nondef_modif2.groupby(["adresse_station", "annee_mise_en_service"], as_index=False).agg(
#    nb_bornes=("nbre_pdc", lambda x: x.sum() if (x == 1).all() else x.iloc[0] if len(x) == x.iloc[0] else x.max())
#)
###############################################








data_valide_nondef_modif.loc[7506,]

data_valide_nondef_modif2[data_valide_nondef_modif2["nom_amenageur"]=="QoWatt"][["nom_amenageur", "adresse_station", 'date_mise_en_service', 'nbre_pdc', "nb_bornes"]]

data_valide_nondef_modif[data_valide_nondef_modif["nom_amenageur"]=="QoWatt"][["nom_amenageur", "adresse_station", 'date_mise_en_service', 'nbre_pdc']]