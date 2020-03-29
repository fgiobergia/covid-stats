import json
import pandas as pd
import os
from dateutil.parser import parse as parse_date
from datetime import date

def get_path(basedir, target):
    dirs = {
        "dati_province": "dati-province"
    }
    assert target in dirs
    return os.path.join(basedir, dirs[target])

def load_province_data(data_dir):
    assert os.path.isdir(data_dir)

    filepath = os.path.join(data_dir, "dati-json/dpc-covid19-ita-province.json")
    assert os.path.isfile(filepath)

    with open(filepath) as f:
        df = pd.DataFrame(json.load(f))
        df["data"] = df["data"].map(parse_date)
        df["date"] = df["data"].map(lambda d: d.date())
        df["time"] = df["data"].map(lambda d: d.time())
        return df

def load_province_population(data_dir="."):
    assert os.path.isdir(data_dir)
    filepath = os.path.join(data_dir, "province.csv")
    assert os.path.isfile(filepath)
    df = pd.read_csv(filepath, skiprows=[0])

    def converter(value):
        mapped = {
            "Bolzano/Bozen": "Bolzano",
            "Massa-Carrara": "Massa Carrara",
            "Valle d'Aosta/Vallée d'Aoste": "Aosta"
        }
        return mapped.get(value, value)
    
    df["Provincia"] = df["Provincia"].map(converter)
    return df

def get_latest_by_province(df, max_date):
    df_by = df[df["date"]<=max_date].sort_values("data")
    df_by["ndx"] = df_by.index
    ndx = df_by.groupby("codice_provincia")["ndx"].apply(max)
    df_result = df_by.loc[ndx]
    return df_result[df_result["denominazione_provincia"]!="In fase di definizione/aggiornamento"]

def get_population_by_province_function(pop_df):
    # expects "pop_df" to have a "totale" column
    def get_population_by_province(province):
        return int(pop_df.loc[(pop_df["Provincia"]==province)&(pop_df["Età"]=="Totale"), "totale"])
    return get_population_by_province
    
def cases_per_1000_inhabitants(df, pop_df, date="latest"):
    assert date == "latest" or isinstance(date, datetime.date)
    if date == "latest":
        date = df["date"].max()
    
    df_by = get_latest_by_province(df, date)
    province_extractor = get_population_by_province_function(pop_df)
    df_by["Popolazione"] = df_by["denominazione_provincia"].map(province_extractor)
    df_by["cases_per_1000"] = df_by["totale_casi"] / df_by["Popolazione"] * 1000
    return df_by


basedir = "COVID-19"
df = load_province_data(basedir)
pop = load_province_population()
pop["totale"] = pop["Totale Maschi"] + pop["Totale Femmine"]

d = cases_per_1000_inhabitants(df, pop)