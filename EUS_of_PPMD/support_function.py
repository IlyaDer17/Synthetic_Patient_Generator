#!/usr/bin/env python
# coding: utf-8

# In[18]:
import os
import shutil
import pandas as pd

def create_new_catalog(Catalog):
    if os.path.exists(Catalog):
        shutil.rmtree(Catalog)
        os.makedirs(Catalog)
    else:
        os.makedirs(Catalog)


def parametrs_from_config(Config):
    return tuple(pd.read_csv(Config, header=None, sep=" ")[1])
