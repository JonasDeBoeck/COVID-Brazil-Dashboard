import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def atualiza_dados(sheet_page = 'Data_subregions', pasta=None, dataset='dados'):

    scope = ['https://spreadsheets.google.com/feeds',

             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('data/credentials/cred-sir.json',scope)
    client = gspread.authorize(creds)

    sheet =  client.open(dataset)
    d = sheet.worksheet(sheet_page)
    df = pd.DataFrame(d.get_all_records())
    if 'Data' in df.columns:
        df.loc[:,'Data'] = pd.to_datetime(df.Data)
        df.loc[:,'Data'] = df['Data'].dt.strftime('%m/%d/%Y')
    if pasta is not None:
        df.to_csv(f"{pasta}/{dataset} - {sheet_page}.csv")
    else:
        df.to_csv(f"data\original_data\SUBREGION_DATA.csv")

atualiza_dados()