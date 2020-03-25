#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import time


def file_collection_for_request_user(Catalog):

    def IsFileUploaded(FileName):
        FileSizeNow, SizeAfter5Seconds = 0, 1
        while FileSizeNow != SizeAfter5Seconds:
            FileSizeNow = os.path.getsize(Catalog + FileName)
            time.sleep(5)
            SizeAfter5Seconds = os.path.getsize(Catalog + FileName)
        return True

    FilsNames = [name for name in os.listdir(Catalog)]
    SummaryFile = pd.DataFrame(columns=['epizod'])

    for FileName in FilsNames:
        if IsFileUploaded(FileName):
            File = pd.read_csv(Catalog + FileName, encoding='cp1251', sep='\t', low_memory=False)
            File.rename({'ObjectName': 'epizod'}, axis=1, inplace=True)
            if (SummaryFile.shape[0] > 0) & (File.shape[0] > 0):
                SumbolInFileEpizod = min(len(File.epizod[0]), len(SummaryFile.epizod[0]))
                crop_episode_to_merge = lambda x: x[0:SumbolInFileEpizod]
                SummaryFile.epizod, File.epizod = SummaryFile.epizod.apply(crop_episode_to_merge), File.epizod.apply(
                    crop_episode_to_merge)
            SummaryFile = pd.merge(SummaryFile, File, on='epizod', how='outer')

    SummaryFile.to_csv("Results/SummaryFile.txt", encoding='cp1251',
                       sep='\t', index=None)
    return SummaryFile
    # SummaryFile-итоговый чистый файл с всеми признаками
