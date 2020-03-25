import pandas as pd
import os
import json


def to_FHIR(Topic, DirectoryForUserRequest):
    def write_to_json(df, Topic):

        def dict_episod_diag_add(list_key_value):

            DictEpisodDiag = {}

            for key, value in list_key_value:
                if len(value) > 0:
                    if (type(value) == list) & (len(value) == 1):
                        value = value[0]
                    DictEpisodDiag[key] = value

            return DictEpisodDiag


    def Create_list_key_value(EpisodDiag, Topic):


        dict_list_key_value = {
            "Измерения": [("resourceType", "Observation"), ('id', df.loc[EpisodDiag]['epizod']), ("text", " Measurement "),
                          ("component", [{"valueQuantity": {"value": df.loc[EpisodDiag][" Measurement"], "unit": " unit"}}])]}

        return dict_list_key_value[Topic]

    for EpisodDiag in list(df.index):
        list_key_value = Create_list_key_value(
            EpisodDiag=EpisodDiag, Topic=Topic)

        DictEpisodDiag = dict_episod_diag_add(list_key_value=list_key_value)

        with open('for_data_FHIR/' + EpisodDiag + '.json', 'w') as f:
            json.dump(DictEpisodDiag, f)

#по id данные выгружаются в форме заданного ресурса


    def measurement_to_FHIR(DirectoryForUserRequest):
        df = pd.read_csv("Results/SummaryFile.txt", encoding='cp1251', sep='\t',
                         usecols=list(DirectoryForUserRequest.columns))

        measurement = df.columns[1]
        df = df[df.measurement.apply(lambda x: x == x)]
        df.index = df.epizod

        write_to_json(df=df, Topic=Topic)


    dict_resurs_script = {"Измерения": measurement_to_FHIR}

#словарь ресурс-функция для приведения к данному ресурсу"""

    dict_resurs_script[Topic](DirectoryForUserRequest=DirectoryForUserRequest)