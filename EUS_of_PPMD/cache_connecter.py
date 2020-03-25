#!/usr/bin/env python
# coding: utf-8

from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto import keyboard
from pywinauto.keyboard import send_keys
import pywinauto
import time
import pandas as pd
import os
import uuid

def cache_connecter(LocationDB=None, DirectoryForUserRequest=None, Catalog=None, HowManyCharactersAreCropped=7):


    def open_Cahce_Terminal(terminal_coords, cmd_line):
        app = Application().Start(cmd_line)

        def click_(coords):
            pywinauto.mouse.move(coords)
            pywinauto.mouse.click(button='left', coords=coords)

        command_list = [('send_keys', '{ENTER}'), ('send_keys', '{LEFT}{ENTER}'), ('click', terminal_coords),
                        ('send_keys', '{DOWN 5}{ENTER}')]
        for command in command_list:
            if command[0] == 'send_keys':
                send_keys(command[1], with_spaces=True)
            if command[0] == 'click':
                click_(command[1])
            time.sleep(1)

    def running_script_COS_upload(command_list):
        for command in command_list:
            time.sleep(1)
            keyboard.SendKeys(command)
            send_keys('{ENTER}', with_spaces=True)

    def add_quotes(line):
        return ('"') + line + ('"')

    def found_parameters_for_script_COS(ObjectDirectoryForUserRequest, Catalog):
        LineCacheFeatures = " ".join(list(ObjectDirectoryForUserRequest.FeatureCacheNames))
        FirstObject = list(ObjectDirectoryForUserRequest.FirstObjectName)[0]
        FileName = "\\" + Catalog + str(uuid.uuid4()) + ".txt"  # Генерируем случайное имя файла ВОЗМОЖНО ОШИБКА

        LineCacheFeatures, FirstObject, FileName = add_quotes(LineCacheFeatures), add_quotes(
            FirstObject), add_quotes(FileName)

        CommandForCacheTerminal = 'do ##class(ExtendsPersistent.DataDownload).Download'
        CommandForCacheTerminal += '({},{},{},{},{})'.format(
            Topic, LineCacheFeatures, FirstObject, HowManyCharactersAreCropped, FileName)

        DictSumbolForReplace = {'(': '{(}', ')': '{)}', ' ': '{SPACE}'}
        for sumbol in DictSumbolForReplace.keys():
            CommandForCacheTerminal = CommandForCacheTerminal.replace(sumbol, DictSumbolForReplace[sumbol])
        CommandForCacheTerminal += '{HOME}'
        return CommandForCacheTerminal

    for Topic in DirectoryForUserRequest.ObjectName.unique():
        ObjectDirectoryForUserRequest = DirectoryForUserRequest[DirectoryForUserRequest.ObjectName == Topic]

        cmd_line, login, password, NameDB, terminal_coords_x, terminal_coords_y = tuple(
            pd.read_csv('ConfigCache.txt', encoding='cp1251', sep=" ", header=None)[1])

        terminal_coords = (int(terminal_coords_x), int(terminal_coords_y))
        NameDB = add_quotes(NameDB)

        CommandForCacheTerminal = found_parameters_for_script_COS(
            ObjectDirectoryForUserRequest=ObjectDirectoryForUserRequest, Catalog=Catalog)

        open_Cahce_Terminal(terminal_coords=terminal_coords, cmd_line=cmd_line)

        running_script_COS_upload([login, password, 'zn' + '{SPACE}' + NameDB, CommandForCacheTerminal])
