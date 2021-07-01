import pandas as pd

url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
df = pd.read_csv(url)
df.to_csv("data/original_data/CASES_STATES.csv")