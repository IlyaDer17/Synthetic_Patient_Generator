#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pywinauto.application import Application
import pywinauto
import time
import pandas as pd
import sqlite3
import uuid
import os
import time
from pywinauto.keyboard import SendKeys
from pywinauto import keyboard
from pywinauto.keyboard import send_keys
import shutil
import warnings

warnings.filterwarnings('ignore')

from cache_connecter import cache_connecter
from sql_connecter import sql_connecter
from support_function import create_new_catalog
from support_function import parametrs_from_config
from file_collection_for_request_user import file_collection_for_request_user
from to_FHIR import to_FHIR

LocationDB, FeaturesTable, TypeDB, Catalog, CatalogMyPC = parametrs_from_config('config_main.txt')

print(pd.read_csv(FeaturesTable)[['FeatureNames', 'resourceType']])
Topic = input("Посмотрите на таблицу признаков и введите ресурс/список признаков (индексы через пробел) для выгрузки")

Directory = pd.read_csv(FeaturesTable)
if Topic in set(Directory.resourceType):  # Если задан ресурс а не набор признаков
    DirectoryForUserRequest = Directory[Directory.resourceType == Topic]
    ToFhir = input("Вы выбрали ресурс. Оформить его в виде ресурса FHIR?(yes/no")
else:  # Если задан набор признаков
    DirectoryForUserRequest = Directory[Directory.index.isin(Topic.split(" "))]

create_new_catalog(Catalog=CatalogMyPC)

DictConnecterTypeDB = {"SQL": sql_connecter
    , "Cache": cache_connecter}

DictConnecterTypeDB[TypeDB](LocationDB=LocationDB, DirectoryForUserRequest=DirectoryForUserRequest, Catalog=Catalog)
file_collection_for_request_user(Catalog=CatalogMyPC)

if ToFhir == "yes":
    to_FHIR()