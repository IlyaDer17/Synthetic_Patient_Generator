**Руководство для практического использования модуля выгрузки данных из БД Cache**
https://github.com/IlyaDer17/Synthetic_Patient_Generator/blob/master/README.md

**Процесс работы.**

Сначала модуль для выгрузки данных подключается к БД, выгружает и структурирует данные согласно пользовательскому запросу.

**Схема работы модуля**

![Image alt](https://github.com/IlyaDer17/Synthetic_Patient_Generator/blob/master/Work_Scheme.png)

**Пример результата работы модуля**

![Image alt](https://github.com/IlyaDer17/Synthetic_Patient_Generator/blob/master/Data_exsample.png)

Далее через веб-интерфейс пользователь может задать параметры генерации синтетических пациентов.

**Веб-интерфейс** ![Image alt](https://github.com/IlyaDer17/Synthetic_Patient_Generator/blob/master/Web_interface.png)

Далее создается файл с синтетическими пациентами, пример такого файла https://github.com/IlyaDer17/Synthetic_Patient_Generator/blob/master/Пример_файл_15_синтетических_пациентов.xls



**Подготовка.**

Если база данных принимает запросы на языке Cache Object Script необходимо вручную скомпилировать class(ExtendsPersistent.DataDownload) в Cache Studio перед запуском скрипта * 

Необходимо указать параметры доступа к БД в config_main.txt. LocationDB – путь до базы данных, при условии что БД находится на вашем ПК, FeaturesTable - Directory.txt по умолчанию, TypeDB – тип БД, Cache, SQL, другой, Catalog – адрес каталога в сети, CatalogMyPC – адрес каталога для данных пользователя **

Необходимо заполнить ConfigCache ***

**Запуск.**

Модуль запускается через python main.py. Для работы модуля необходим интерпретатор python не ниже 3.6. Далее необходимо следовать указаниям выводимым скриптом в командную строку.

**Результат.**

Если модуль отработал без ошибок, файл с данными будет лежать в указанной вами директории.

**Примечания.**

1 Для работы с БД ц. Алмазово нужно пропустить этот шаг

2 Для работы с БД ц. Алмазово Catalog и CatalogMyPC – один и тот же каталог

3 Для работы с БД ц. Алмазово нужно пропустить этот шаг

