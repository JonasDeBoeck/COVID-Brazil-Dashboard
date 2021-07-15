import pandas as pd
import Utils
import matplotlib.pyplot as plt
import os
import shutil

subregion_metadata = pd.read_csv("data/filtered_data/SUBREGION_METADATA.csv")

for subregion in subregion_metadata.itertuples():
    os.makedirs(f"data/resulted_data/neural_network/temp/{subregion[1]}", exist_ok = True)
    subregion_data = pd.read_csv(f"data/filtered_data/subregions/{subregion[1]}/GENERAL_COVID_DATA.csv")
    start_day = 10
    end_day = 31
    prev = 0

    subregion_data = subregion_data.rename(columns={"DATE": "Data", "ACTIVE_CASES": "At", "CUMULATIVE_RECOVERED": "Rt", "CUMULATIVE_DEATHS": "Óbitos", "CUMULATIVE_CASES": "Confirmados"})
    subregion_data = subregion_data.tail(31)
    for dLen in range(start_day, end_day):
        ds = subregion_data[["At"]]
        ini = ds[ds["At"] > 0]
        nData = len(ini)
        sl1 = 31 - dLen
        sl = 31
        learner, df = Utils.run_region(subregion[1], sl1, sl, subregion_data, subregion[3], step=14)
        df.to_csv(f"data/resulted_data/neural_network/temp/{subregion[1]}/Subregions_Pred_{dLen}D_prev-{prev}-{subregion[1]}.csv")

    Utils.run_unifica('Outputs', subregion[1], unify = True, crop = 14, MM = False, dia_ini = start_day, dia_fim = end_day - 1, recalc_rt=True, prev=prev, gen_graphs=False) 

shutil.rmtree("data/resulted_data/neural_network/temp/")