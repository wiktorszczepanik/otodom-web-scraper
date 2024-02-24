## Web scraper for Otodom.pl
This bot is developed in Python, with the main library used being Selenium. The scraper collects real estate data and stores it in an SQLite database, with database files located in the ***db*** directory. The **.db** file and all its tables are automatically generated based on the selected filters.

![alt text](additional/img/sql_schema01.png?raw=true)
*example database schema*

### Setup
Filters and other key information are implemented through a **.json** file in the "filters" directory. Modifying this file will affect the selected filters on the website page. The ***filters*** directory may also contain additional filter files.

The ***web_od/constants.py*** file contains values that are essential for the scraper's proper functioning. Certain values, such as DRIVER and DB_NAME, must be configured before running the program.

```Python
DRIVER = r";D:\web_driver"  # web driver type
DB_NAME = "apartment_rental_warsaw"  # name of created data base
```
If Otodom blocks the connection or the program stops for any reason, the bot's operations can be restored from the last row in the database by setting the CONTINUE_AFTER_BRAKE value in the **constants.py** file.
```Python
CONTINUE_AFTER_BRAKE = True  # continue web scraping after program brake
```

### Access
An example of simple access to the collected data from the **.db** file can be found in ***additional/full_estate_info.sql***.
