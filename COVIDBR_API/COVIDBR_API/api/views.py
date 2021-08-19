from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.settings import api_settings
import pandas as pd
import csv
import json
import os
import re

wdir = os.getcwd()
wdir = re.sub(r'COVIDBR_API', '', wdir)

# Create your views here.
@api_view(('GET',))
def cases(request, region: str = None):
    data = []
    with open(f"{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_data = {"DATE": row["DATE"], "REGION": row["REGION"], "NEW_CASES": row["NEW_CASES"], 
                        "CUMULATIVE_CASES": row["CUMULATIVE_CASES"], "NEW_RECOVERED": row["NEW_RECOVERED"], 
                        "CUMULATIVE_RECOVERED": row["CUMULATIVE_RECOVERED"], "NEW_DEATHS": row["NEW_DEATHS"], 
                        "CUMULATIVE_DEATHS": row["CUMULATIVE_DEATHS"], "ACTIVE_CASES": row["ACTIVE_CASES"]}
            data.append(row_data)

    res = json.dumps(data, ensure_ascii=False).encode("utf8")
    return HttpResponse(res, content_type="application/json")

@api_view(('GET',))
def vaccinations(request, region: str = None):
    data = []
    with open(f"{wdir}/data/filtered_data/subregions/{region}/GENERAL_COVID_DATA.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_data = {"DATE": row["DATE"], "REGION": row["REGION"], "NEW_FIRST_DOSES": row["NEW_FIRST_DOSES"], 
                        "CUMULATIVE_FIRST_DOSES": row["CUMULATIVE_FIRST_DOSES"], "NEW_SECOND_DOSES": row["CUMULATIVE_SECOND_DOSES"]}
            data.append(row_data)

    res = json.dumps(data, ensure_ascii=False).encode("utf8")
    return HttpResponse(res, content_type="application/json")

@api_view(('GET',))
def predictions(request, region: str = None):
    data = []

    with open(f"{wdir}/data/resulted_data/neural_network/{region}/pred_all.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["SP-Subregião"].lower() == region.lower():
                row_data = {"DATE": row["Data"], "REGION": row["SP-Subregião"], "INFECTIONS": row["Infected"], "RECOVERED": row["Recovered"],
                            "DEATH": row["Death"], "SUSCEPTIBLE": row["Susceptible"], "RT": row["Rt"], "TRAIN": row["Used in Train"]}
                data.append(row_data)

    res = json.dumps(data, ensure_ascii=False).encode("utf8")
    return HttpResponse(res, content_type="application/json")

# @api_view(('GET',))
# def hospitalisations(request, region: str = None):
#     data = []

#     with open(f"{wdir}/data/filtered_data/HOSP.csv", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             if row["REGION"].lower() == region.lower():
#                 row_data = {"DATE": row["DATE"], "REGION": row["REGION"], "TOTAL_IN_ICU": row["TOTAL_IN_ICU"], "NEW_IN": row["NEW_IN"]}
#                 data.append(row_data)

#     res = json.dumps(data, ensure_ascii=False).encode("utf8")
#     return HttpResponse(res, content_type="application/json")

# @api_view(('GET',))
# def mobility(request, region: str = None):
#     data = []

#     with open(f"{wdir}/data/filtered_data/MOBILITY.csv", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             check = row["sub_region_2"].replace(" ", "").lower()
#             if check == region.lower():
#                 row_data = {"DATE": row["date"], "SUBREGION": row["sub_region_2"], "RETAIL": row["retail_and_recreation_percent_change_from_baseline"],
#                 "GROCERY": row["grocery_and_pharmacy_percent_change_from_baseline"], "PARKS": row["parks_percent_change_from_baseline"],
#                 "TRANSIT": row["transit_stations_percent_change_from_baseline"], "WORKPLACE": row["workplaces_percent_change_from_baseline"], 
#                 "RESIDENTIAL": row["residential_percent_change_from_baseline"]}
#                 data.append(row_data)

#             if region.lower() == "belgium":
#                 if row["sub_region_1"] == "":
#                     row_data = {"DATE": row["date"], "REGION": row["country_region"], "RETAIL": row["retail_and_recreation_percent_change_from_baseline"],
#                 "GROCERY": row["grocery_and_pharmacy_percent_change_from_baseline"], "PARKS": row["parks_percent_change_from_baseline"],
#                 "TRANSIT": row["transit_stations_percent_change_from_baseline"], "WORKPLACE": row["workplaces_percent_change_from_baseline"], 
#                 "RESIDENTIAL": row["residential_percent_change_from_baseline"]}
#                 data.append(row_data)

#     res = json.dumps(data, ensure_ascii=False).encode("utf8")
#     return HttpResponse(res, content_type="application/json")