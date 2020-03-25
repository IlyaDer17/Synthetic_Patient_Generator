#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd
import uuid
import time

def sql_connecter(LocationDB, DirectoryForUserRequest, Catalog):

    DirectoryForUserRequest.ObjectName = DirectoryForUserRequest.resourceType

    # Темы ресурсов являются названиями таблицы в БД SQL

    def found_parameters_for_sql_query(ObjectDirectoryForUserRequest, Catalog, Topic):
        LineSQLFeatures = " ".join(list(ObjectDirectoryForUserRequest.FeatureCacheNames))
        FileName = Catalog + str(uuid.uuid4()) + ".txt"  # Генерируем случайное имя файла
        CommandForDataBaseSQL = "SELECT " + LineSQLFeatures.replace(" ", ",") + ",epizod" + " FROM " + Topic
        return CommandForDataBaseSQL, FileName

    def load_data_from_sql(LocationDB, CommandForDataBaseSQL, FileName):
        con = sqlite3.connect(LocationDB)
        df = pd.read_sql(CommandForDataBaseSQL, con)
        df.to_csv(FileName, encoding='cp1251', sep='\t', index=None)

    for Topic in DirectoryForUserRequest.ObjectName.unique():
        ObjectDirectoryForUserRequest = DirectoryForUserRequest[DirectoryForUserRequest.ObjectName == Topic]
        CommandForDataBaseSQL, FileName = found_parameters_for_sql_query(Catalog=Catalog,
                                                                         ObjectDirectoryForUserRequest=ObjectDirectoryForUserRequest,
                                                                         Topic=Topic)
        load_data_from_sql(LocationDB=LocationDB, CommandForDataBaseSQL=CommandForDataBaseSQL, FileName=FileName)
