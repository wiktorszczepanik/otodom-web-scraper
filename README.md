# otodom-web-scraper
## Web scraper for Otodom.pl
This bot is written in Python and the main library used in this project is Sellenium. Scraper collects real estate data into SQLite database. Database files are located in db directory. The **.db** file and all the tables in it are created automatically based on the selected filters.

![alt text](additional/img/sql_schema01.png?raw=true)
*example database schema*

### Setup
Filters and other key information’s are implemented by **.json** file in the filters directory. Modifying this file will affect selected filters on the website page. The filters directory may also contain more filter files.

The ***web_od/constans.py*** file contains main values that are important for the scraper to work properly. Some values must be set before running the program - such as DRIVER and DB_NAME.
```Python
DRIVER = r";D:\web_driver"  # web driver type
DB_NAME = "apartment_rental_warsaw"  # name of created data base
```
If otodom blocks the connection or program will stop running for any other reason – it is possible to restore bot operations from the last row in database by setting CONTINUE_AFTER_BRAKE value in the **constans.py** file.
```Python
CONTINUE_AFTER_BRAKE = True  # continue web scraping after program brake
```

### Access
An example of simple access to collected data from **.db** file can be found in ***additional/full_estate_info.sql***.
