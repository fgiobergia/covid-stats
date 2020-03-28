import json
import pandas as pd
import os

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
        return json.load(f)

# No longer needed
def load_date(data_dir, date="latest"):
    assert os.path.isdir(data_dir)
    assert date == "latest" or date.isdecimal()
    
    dir_dati_provincie = get_path(data_dir, "dati_province")

    if date == "latest":
        filename = max(os.listdir(dir_dati_provincie))
    else:
        filename = f"dpc-covid19-ita-province-{date}.csv"
    
    filepath = os.path.join(dir_dati_provincie, filename)
    assert os.path.isfile(filepath)

    df = pd.read_csv(filepath)
    return df

basedir = "COVID-19"
province = load_province(basedir)
df = load_date("COVID-19", "latest")