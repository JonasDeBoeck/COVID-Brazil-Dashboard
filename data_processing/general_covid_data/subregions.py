import pandas as pd
import os

metadata = pd.read_csv("data/filtered_data/SUBREGION_METADATA.csv")
data = pd.read_csv("data/original_data/SUBREGION_DATA.csv")

for subregion in metadata["SUBREGION"]:
    if not os.path.exists(f"data/filtered_data/subregions/{subregion}"):
        os.mkdir(f"data/filtered_data/subregions/{subregion}")

    subregion_data = data[ data["SP-Subregião"] == subregion ] 
    subregion_data = subregion_data.reset_index(drop=True)
    subregion_data = subregion_data[["Data", "SP-Subregião", "Novos Casos", "Confirmados", "Novos Óbitos", "Óbitos", "Novas Dose1", "Vac 1", "Novas Dose2", "Vac 2"]]
    subregion_data = subregion_data.fillna(0)
    subregion_data[["Novas Dose1", "Vac 1", "Novas Dose2", "Vac 2"]] = subregion_data[["Novas Dose1", "Vac 1", "Novas Dose2", "Vac 2"]].astype(int)
    subregion_data = subregion_data.rename(columns={"Data": "DATE", "SP-Subregião": "REGION", "Novos Casos": "NEW_CASES", "Confirmados": "CUMULATIVE_CASES",
                                                    "Novos Óbitos": "NEW_DEATHS", "Óbitos": "CUMULATIVE_DEATHS", "Novas Dose1": "NEW_FIRST_DOSES", 
                                                    "Vac 1": "CUMULATIVE_FIRST_DOSES", "Novas Dose2": "NEW_SECOND_DOSES", "Vac 2": "CUMULATIVE_SECOND_DOSES"
    })

    subregion_data["CUMULATIVE_RECOVERED"] = 0

    for index, row in subregion_data.iterrows():
        if index >= 14:
            subregion_data.iloc[index, 10] = subregion_data.iloc[index - 14, 3] - subregion_data.iloc[index - 14, 5]

    subregion_data["NEW_RECOVERED"] = 0

    for index, row in subregion_data.iterrows():
        if index >= 1:
            subregion_data.iloc[index, 11] = subregion_data.iloc[index, 10] - subregion_data.iloc[index - 1, 10]
        else:
            subregion_data.iloc[index, 11] = subregion_data.iloc[index, 6]

    subregion_data["ACTIVE_CASES"] = 0

    for index, row in subregion_data.iterrows():
        subregion_data.iloc[index, 12] = subregion_data.iloc[index, 3] - subregion_data.iloc[index, 5] - subregion_data.iloc[index, 10]

    subregion_data["DATE"] = pd.to_datetime(subregion_data["DATE"]).dt.strftime("%Y-%m-%d")
    
    subregion_data.to_csv(f"data/filtered_data/subregions/{subregion}/GENERAL_COVID_DATA.csv")