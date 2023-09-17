# otodom-web-scraper
## Web scraper for Otodom.pl
Bot is written in Python. The main library used in this project is Sellenium. Scraper collects estates data to SQLite database. Database files are located in db directory.

![alt text](additional/img/sql_schema01.png?raw=true)
*database schema*

### Setup
Filters and other key information’s are implemented by **.json** file in the filters directory. Modifying this file will affect selected filters on the website page. Filters directory may also contain more filter files.

The ***web_od/constans.py*** file contains main values that are important for the scraper to work properly. Some values must be set before running the program - such as DRIVER and DB_NAME.
```Python
DRIVER = r";D:\web_driver"  # web driver type
DB_NAME = "apartment_rental_warsaw"  # name of created data base
```
If otodom blocks the connection or program will stop running for any other reason – it is possible to restore bot operations from last row in database by setting in file **constans.py** CONTINUE_AFTER_BRAKE value.
```Python
CONTINUE_AFTER_BRAKE = True  # continue web scraping after program brake
```

### Access
An example of simple access to collected data from **.db** file can be found in ***additional/full_estate_info.sql***.
