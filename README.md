# Synthetic_Patient_Generator
Генерация синтетических пациентов основанная на реальных данных
https://github.com/IlyaDer17/Synthetic_Patient_Generator/blob/master/README

Руководство для практического использования модуля выгрузки данных из БД Cache

Подготовка. 

1. Если база данных принимает запросы на языке Sache Object System необходимо вручную скомпилировать class(ExtendsPersistent.DataDownload) в Cache Studio перед запуском скрипта (1) 
2. Необходимо указать параметры доступа к БД в config_main.txt. LocationDB – путь до базы данных, при условии что БД находится на вашем ПК, FeaturesTable - Directory.txt по умолчанию, TypeDB – тип БД, Cache, SQL, другой, Catalog – адрес каталога в сети, CatalogMyPC – адрес каталога для данных пользователя (2)
3. Необходимо заполнить ConfigCache (3) 

Запуск.

Модуль запускается через python main.py. Для работы модуля необходим интерпретатор python не ниже 3.6. Далее необходимо следовать указаниям выводимым скриптом в командную строку.
Результат. Если модуль отработал без ошибок, файл с данными будет лежать в указанной вами директории.



(1) Для работы с БД ц. Алмазово нужно пропустить этот шаг
(2) Для работы с БД ц. Алмазово Catalog и CatalogMyPC – один и тот же каталог
(3) Для работы с БД ц. Алмазово нужно пропустить этот шаг
