import pandas as pd
import os

# Example of data processor
df = pd.read_csv("data/original_data/CASES_STATES.csv")

state = "SP"

# Create directory for state
os.mkdir(f"data/filtered_data/{state}")

# Filter data on state
sp_df = df[ df["state"] == state ]

# Get desired columns
filtered_df = sp_df[["date", "state", "newCases", "totalCases", "newDeaths", "deaths", "recovered"]]

# Fill NaN values in beginning of dataset with 0
filtered_df["recovered"] = filtered_df["recovered"].fillna(0)

# Reset the index
filtered_df = filtered_df.reset_index(drop=True)

# Cast the recovered to ints
filtered_df["recovered"] = filtered_df["recovered"].astype(int)

# Calculate new recovered for each day by subtracting cumulative recovered from the day itself and the day before
filtered_df["NEW_RECOVERED"] = 0
for index, row in filtered_df.iterrows():
    if index >= 1:
        filtered_df.iloc[index, 7] = filtered_df.iloc[index, 6] - filtered_df.iloc[index - 1, 6]

# Estimate active cases A(t) = C(t) - R(t) - D(t)
filtered_df["ACTIVE_CASES"] = filtered_df["totalCases"] - filtered_df["recovered"] - filtered_df["deaths"]

# Rename columns to fit dashboard
filtered_df = filtered_df.rename(columns={"date": "DATE", "state": "REGION", "newCases": "NEW_CASES", "totalCases": "CUMULATIVE_CASES", "newDeaths": "NEW_DEATHS", "deaths": "CUMULATIVE_DEATHS", "recovered": "CUMULATIVE_RECOVERED"})

filtered_df.to_csv(f"data/filtered_data/{state}/CASES_DEATHS_RECOVERED_ACTIVE.csv")