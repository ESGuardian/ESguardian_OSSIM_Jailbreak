# README #

Это мой набор плагинов, отчетов, файлов конфигурации и модификации OSSIM.
01.09.2015
Многое поменял с момента первой публикации. 
В отчеты IDS и OTX вставил данные геолокации. 
Навел порядок с кодировками символов. 
Убрал в отдельный модуль "helper" функцию запроса данных геолокации. С базой geoip2 работать надо осторожно.
вызов методов объекта reader может привести к фатальной ошибке, например, если случайно попадется локальный адрес ip.
Кроме того в базе могут оказаться данные в не пойми какой кодировке, типа, на языке оригинала.
Текущая версия отчетов 1.0.3