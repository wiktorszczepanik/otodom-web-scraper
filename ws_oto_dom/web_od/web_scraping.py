import web_od.constans as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import random
import sqlite3
import math
import os
import time
import re


class WebScraping(webdriver.Chrome):
    def __init__(
        self,
        driver_path=const.DRIVER,
        close_option=False,
        add_ex_time=True,
        static_delay=const.STATIC_DELAY,
    ) -> None:
        self.driver_path = driver_path
        self.close_option = close_option
        self.add_ex_time = add_ex_time
        self.static_delay = static_delay
        os.environ["PATH"] += self.driver_path
        web_option = webdriver.ChromeOptions()
        web_option.add_experimental_option("detach", True)
        super(WebScraping, self).__init__(options=web_option)
        self.implicitly_wait(10)
        self.ec_wait_base = WebDriverWait(self, 4)
        self.maximize_window()

    def __exit__(self, *args):
        if self.close_option == True:
            self.quit()

    def main_page(self):
        RunFunctons.static_wait(2, self.static_delay)
        self.get(const.BASE_PATH)
        if self.add_ex_time == True:
            RunFunctons.rand_wait(2)

    def cookie_pass(self):
        try:
            accept_btn = self.ec_wait_base.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button[id="onetrust-accept-btn-handler"]')
                )
            )
            accept_btn.click()
            RunFunctons.rand_wait(1)
        except:
            if self.add_ex_time == True:
                RunFunctons.rand_wait(1)
            else:
                pass

    def append_main_filters(self, filters):
        try:
            RunFunctons.locate_form(self)

            if "estate" in filters:
                estate_val = filters["estate"]
                self.estate_glbl = estate_val
                filters.pop("estate")
                self.find_element_by_css_selector(
                    "div[class$=' css-b62m3t-container']"
                ).click()
                estete_lst = self.find_element_by_id("react-select-estate-listbox")
                estete_lst = (estete_lst.text).split("\n")
                keys_down_num = estete_lst.index(estate_val)
                main_action = ActionChains(self)
                if keys_down_num > 0:
                    for _ in range(keys_down_num):
                        main_action.send_keys(Keys.DOWN)
                    main_action.send_keys(Keys.ENTER)
                    main_action.perform()
                else:
                    pass  # left defult value from web
                RunFunctons.rand_wait(0.5)

            if "location" in filters:
                location_input = filters["location"].strip()
                filters.pop("location")
                self.find_element_by_xpath("//button[@id='location']").click()
                loc_box = self.find_element_by_xpath(
                    "//input[@id='location-picker-input']"
                )
                loc_box = loc_box.send_keys(location_input)
                self.find_elements_by_xpath("//ul[@class='css-vmxvu4 e1notw0g0']")
                # RunFunctons.static_wait(0.2, self.static_delay)
                self.find_element_by_xpath(
                    "//div[@id='__next']//li[1]//label[1]"
                ).click()
                RunFunctons.static_wait(0.5, self.static_delay)

            self.ec_wait_base.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'button[aria-busy="false"]')
                )
            )
        except:
            pass

        RunFunctons.search(self)
        RunFunctons.static_wait(0.5, self.static_delay)
        RunFunctons.rand_wait(3)

    def append_site_filters(self, filters):
        try:
            self.transaction_glbl = filters.get("transaction")
            send_keys_val = ["price_max", "price_min", "area_max", "area_min"]
            react_parts = {}

            # prepare dynamic val
            for key in filters.keys():
                if key not in send_keys_val:
                    json_reference = key
                    if key == "radius":
                        key = "distanceRadius"
                    elif key == "owner_type":
                        key = "ownerTypeSingleSelect"
                    elif key == "availability":
                        key = "freeFrom"
                    react_parts[key] = [f"react-select-{key}-listbox", json_reference]

            dynamic_queue = {
                1: ["transaction", "investment_type"],
                2: ["distanceRadius"],
                3: ["market"],
                4: ["ownerTypeSingleSelect"],
                5: ["freeFrom"],
            }

            all_elements = self.find_elements_by_css_selector(
                "   div[class$=' css-b62m3t-container']"
            )
            dinamic_elements = len(all_elements[1:-1]) + 1
            if self.transaction_glbl == "Na wynajem":
                dinamic_elements = 3

            # dynamic dropdown fields
            for element_id in range(1, dinamic_elements):
                RunFunctons.rand_wait(1)
                element = self.find_elements_by_css_selector(
                    "   div[class$=' css-b62m3t-container']"
                )[element_id]
                element.click()
                try:
                    field = dynamic_queue.get(element_id)
                    ftype = [
                        react_parts.get(i)
                        for i in field
                        if react_parts.get(i) is not None
                    ][0]
                except:
                    pass
                try:
                    child_element_lst = RunFunctons.find_field(self, 3, ftype[0])
                    part_val = filters[ftype[1]]
                    filters.pop(ftype[1])
                    child_lst = (child_element_lst.text).split("\n")
                    keys_down_num = child_lst.index(part_val)
                    main_action = ActionChains(self)
                    if keys_down_num > 0:
                        for _ in range(keys_down_num):
                            main_action.send_keys(Keys.DOWN)
                        main_action.send_keys(Keys.ENTER)
                        main_action.perform()
                    else:
                        main_action.send_keys(Keys.ENTER)
                        main_action.perform()  # left defult value from web
                    RunFunctons.rand_wait(1.5)
                except:
                    pass
        except:
            pass

        # prepare static val
        try:
            static_queue = {
                "price_min": "priceMin",
                "price_max": "priceMax",
                "area_min": "areaMin",
                "area_max": "areaMax",
            }
            run_area = True
            if self.estate_glbl == "Pokoje":
                run_area = False

            # send text to box fields
            for enum, (key, value) in enumerate(static_queue.items()):
                if enum < 2 or run_area == True:
                    filter_txt = str(filters.get(key))
                    filters.pop(key)
                    box = RunFunctons.find_field(self, 4, value)
                    box.send_keys(filter_txt)
                    RunFunctons.rand_wait(0.5)

            # static dropdown fields
            permission_people_run = False
            people_count = filters.get("people_per_room")
            if people_count != 0:
                permission_people_run = True
            if "people_per_room" in filters and permission_people_run == True:
                filters.pop("people_per_room")
                self.find_element_by_xpath("//div[@role='combobox']").click()
                pp_room_path = f"(//li[@role='menuitem'])[{people_count}]"
                people_box = self.find_element_by_xpath(pp_room_path)
                people_box.click()
        except:
            pass

        RunFunctons.static_wait(3, self.static_delay)
        RunFunctons.search(self)
        RunFunctons.rand_wait(3)

    def offers_by_page(self, filters):
        # dynamic count page select
        permission_page_run = str(filters.get("estates_on_page"))
        self.offers_count = permission_page_run
        if "estates_on_page" in filters and int(permission_page_run) != 36:
            self.execute_script("window.scrollTo(0, 9000);")
            RunFunctons.rand_wait(1.5)
            page_element = self.find_elements_by_css_selector(
                "div[class$='css-b62m3t-container']"
            )[-1]
            page_element.click()
            RunFunctons.rand_wait(1)
            el_lst = page_element.text
            elements_lst = el_lst.split("\n")[2:]
            element = elements_lst.index(permission_page_run)
            main_action = ActionChains(self)
            if element == 2:
                # main_action.send_keys(Keys.DOWN) --
                main_action = RunFunctons.offer_count(main_action, element)
            elif element == 3:
                main_action = RunFunctons.offer_count(main_action, element)
            else:
                main_action.send_keys(Keys.ENTER)
            main_action.perform()
            RunFunctons.rand_wait(1.5)
            self.execute_script("return document.body.scrollHeight")

        filters.pop("estates_on_page")
        RunFunctons.static_wait(3, self.static_delay)
        RunFunctons.search(self)
        RunFunctons.rand_wait(3)

    def page_parameters(self, page_limit=0, items_limit=0):
        # get items and pages number
        if items_limit > 0:
            all_items = int(items_limit)
        else:
            all_items = int(
                self.find_element_by_xpath("//span[@class='css-19fwpg e17mqyjp2']").text
            )
        if page_limit > 0:
            all_pages = page_limit
        else:
            all_pages = math.ceil(all_items / int(self.offers_count))

        self.url = self.current_url  # get current url
        self.all_items = all_items + all_pages
        self.all_pages = all_pages
        RunFunctons.rand_wait(1)

    def collect_base(self, id_set, item_id, page_id):
        nav_info = []
        # uuid and table_extend
        for id_element in id_set:
            nav_info.append(id_element)
        nav_info.append(item_id)  # id
        # date and time
        current_day = datetime.now().strftime("%d/%m/%Y")
        current_time = datetime.now().strftime("%H:%M:%S")
        nav_info.extend([current_day, current_time])
        nav_info.append(page_id)  # page
        # url
        if page_id == 1:
            base_url = self.url
        else:
            base_url = self.url + f"&page={page_id}"
        nav_info.append(base_url)
        self.nav_info = nav_info

    def scrape_base(self, item_nr):
        self.drop_item = False
        try:
            RunFunctons.rand_wait(0.5)
            li_selector = (
                f"div[data-cy='search.listing.organic'] li:nth-child({item_nr})"
            )
            main_li = self.find_elements_by_css_selector(li_selector)
            for element in main_li:
                el_txt = element.text.split("\n")
            base_info = RunFunctons.drop_unnecessary_base(el_txt)
            self.base_scrape = RunFunctons.base_clean(base_info)
            self.drop_item = True if len(self.base_scrape) <= 1 else False
            if self.drop_item == False:
                RunFunctons.rand_wait(4)
        except:
            self.drop_item = True

    def move_in(self, item_nr):
        go_to = f"div[data-cy='search.listing.organic'] li:nth-child({item_nr})"
        move_inner = self.find_element_by_css_selector(go_to)
        move_inner.click()

    def scrape_extend(self):
        RunFunctons.rand_wait(0.5)
        extend_scrape, css_selectors, page_lst = [], [], []
        specific_goto = "div[data-testid='ad.top-information.table']"
        additional_goto = "div[data-testid='ad.additional-information.table']"
        page_goto = "div[class='css-m97llu e16xl7020']"
        css_selectors.extend([specific_goto, additional_goto])

        # collect estate info
        for css in css_selectors:
            extend_selector = self.find_elements_by_css_selector(css)
            for s_element in extend_selector:
                extend_all = s_element.text.split("\n")
            extend_all = extend_all[1:]
            extend_clean = RunFunctons.extend_clean(extend_all)
            extend_drop = RunFunctons.extend_drop(extend_clean)
            extend_scrape.append(extend_drop)
            RunFunctons.rand_wait(0.5)
        self.specific_scrape = extend_scrape[0]
        self.additional_scrape = extend_scrape[1]

        page_info_selector = self.find_elements_by_css_selector(page_goto)
        for info in page_info_selector:
            page_lst = info.text.split("\n")
        if len(page_lst) == 3:
            page_lst.insert(-2, None)
        self.page_info_scrape = RunFunctons.page_info_clean(page_lst)

        self.back()  # back to main page
        RunFunctons.rand_wait(2)

    def to_db(self, item_nr):
        conn = sqlite3.connect(const.DB_PATH + const.DB_NAME + ".db")
        cursor = conn.cursor()

        # base
        base_values = []
        base_values.extend(
            [self.nav_info, self.estate_glbl, self.transaction_glbl, self.base_scrape]
        )
        base_values = RunFunctons.clean_nested(base_values)
        base_query = RunFunctons.insert_query("base_info", 16)
        cursor.execute(base_query, base_values)

        # specific and additional
        extend_info, counter = ["specific_info", "additional_info"], 0
        extend_scrape = [self.specific_scrape, self.additional_scrape]
        for scrape in extend_scrape:
            extend_values = []
            extend_values.extend([self.nav_info[0], item_nr, scrape])
            extend_values = RunFunctons.clean_nested(extend_values)
            extend_table_name = extend_info[counter] + self.nav_info[1]
            paragma_query = f"pragma table_info({extend_table_name});"
            cursor.execute(paragma_query)
            table_info_spec = cursor.fetchall()[-1][0] + 1
            extend_query = RunFunctons.insert_query(extend_table_name, table_info_spec)
            cursor.execute(extend_query, extend_values)
            counter += 1

        # page
        page_values = []
        page_values.extend([self.nav_info[0], self.page_info_scrape])
        page_values = RunFunctons.clean_nested(page_values)
        page_query = RunFunctons.insert_query("page_info", 5)
        cursor.execute(page_query, page_values)

        conn.commit()
        conn.close()
        RunFunctons.rand_wait(1.5)

    def next_page(self):
        go_to = "button[aria-label='następna strona']"
        move_next_page = self.find_element_by_css_selector(go_to)
        move_next_page.click()
        RunFunctons.rand_wait(3.5)

    def comm_to_start(self, id_set):
        conn = sqlite3.connect(const.DB_PATH + const.DB_NAME + ".db")
        cursor = conn.cursor()
        local_uuid = id_set[0]
        page_query = f"""SELECT page FROM base_info WHERE uuid = "{local_uuid}" ORDER BY rowid DESC LIMIT 1;"""
        cursor.execute(page_query)
        self.start_page = cursor.fetchone()[0]
        item_query = f"""SELECT id FROM base_info WHERE uuid = "{local_uuid}" ORDER BY rowid DESC LIMIT 1;"""
        cursor.execute(item_query)
        self.start_item = cursor.fetchone()[0]
        print(self.start_item)


class RunFunctons:
    @staticmethod
    def offer_count(action, rule_id):
        for next_element in range(0, rule_id):
            action.send_keys(Keys.DOWN)
        action.send_keys(Keys.ENTER)
        return action

    @staticmethod
    def find_field(driver, delay, field_id):
        find = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    field_id,
                )
            )
        )
        return find

    @staticmethod
    def search(driver):
        driver.ec_wait_base.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='search-form-submit']"))
        ).click()

    @staticmethod
    def locate_form(driver):
        driver.ec_wait_base.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "form[name='adsSearchHome']")
            )
        )

    @staticmethod
    def static_wait(delay, static_delay):
        if static_delay == True:
            time.sleep(delay)
        else:
            pass

    @staticmethod
    def rand_wait(long_wait):
        how_long = round(random.random(), 1) + long_wait
        time.sleep(how_long)

    @staticmethod
    def drop_unnecessary_base(items):
        regex_check = ["Dodane ", "Podbite", "+ czynsz: "]
        out_lst = []
        for element in items:
            case_mach = True
            for catchword in regex_check:
                if catchword in element:
                    case_mach = False
            if case_mach == True:
                out_lst.append(element)
        return out_lst

    @staticmethod
    def base_clean(items):
        db_base = []
        # pictures count cleaning
        pictures = (items[0].split("/"))[-1]
        db_base.append(int(pictures))
        # title + location cleaning
        title, loc = items[1], items[2]
        db_base.extend([title, loc])
        # price cleaning
        if re.search("Zapytaj o cenę", items[3]):
            price_zl = 0
        else:
            price_zl = (items[3].split(" zł"))[0]
        db_base.append(int(price_zl))
        # area cleaning
        area_inp = (items[3].split(" "))[-2]
        area_m2 = re.sub(r"[^0-9.]", "", area_inp)
        db_base.append(float(area_m2))
        # owner cleaning
        owner_type_inp = items[-1]
        exept_type = "Oferta prywatna"
        if owner_type_inp == exept_type:
            owner = [None, exept_type]
        else:
            owner = items[-2:]
        db_base.extend(owner)

        return db_base

    @staticmethod
    def extend_clean(items):
        cleand_items = []
        group_1 = ["Powierzchnia", "Czynsz", "Kaucja"]  # "79 m²" -> 79
        group_2 = ["Liczba pokoi", "Rok budowy"]  # "3" -> 3
        group_3 = ["elevator"]  # "tak" -> 0
        length = len(items)
        for couple in range(0, length, 2):
            item_key = items[couple]
            item_val = items[couple + 1]
            if item_val == "Zapytaj" or item_val == "brak informacji":
                item_val = None
            elif item_key in group_1:
                # delete spaces between numbers in string
                item_val = re.sub(r"(\d)\s+(\d)", r"\1\2", item_val)
                # selecct first number in string
                item_val = int(re.findall(r"\d+", item_val)[0])
            elif item_key in group_2:
                item_val = int(item_val)
            elif item_key in group_3:
                0 if item_val == "tak" else 1
            else:  # reserved for text
                pass
            cleand_items.extend([item_key, item_val])
        return cleand_items

    @staticmethod
    def extend_drop(items):
        even_items = []
        for count, disr in enumerate(items):
            if count % 2 != 0:
                even_items.append(disr)
        return even_items

    @staticmethod
    def page_info_clean(items):
        match_val, exit_lst = [
            "Nr oferty w Otodom:",
            "Nr oferty w biurze nieruchomości",
            "Data dodania:",
            "Data aktualizacji:",
        ], []
        for element in items:
            if element == None:
                exit_lst.append(None)
            elif match_val[1] in element:
                proc_el = element.split(" ")[-1]
                exit_lst.append(proc_el)
            else:
                proc_el = (element.split(":")[-1]).strip()
                if match_val[0] in element:
                    exit_lst.append(int(proc_el))
                else:
                    exit_lst.append(proc_el)
        return exit_lst

    @staticmethod
    def insert_query(name, length):
        question_marks = ""
        for mark in range(0, length):
            question_marks += "?, "
        question_marks = question_marks[0:-2]
        main_query = f"INSERT INTO {name} VALUES ({question_marks});"
        return main_query

    @staticmethod
    def clean_nested(lst):
        exit_lst = []

        def remove_nested(req):
            for part in req:
                if type(part) == list:
                    remove_nested(part)
                else:
                    exit_lst.append(part)

        remove_nested(lst)
        return exit_lst
