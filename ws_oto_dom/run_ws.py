from web_od.web_scraping import WebScraping
from web_od.web_setup import WebSetup
from web_od.db_setup import DbManagement
from web_od.collect_filters import Filters
import web_od.constans as const
import time


def collect_filters():
    collect_all = Filters()
    collect_all.collect()
    all_filters = getattr(collect_all, "filters_lst")
    return all_filters


def prepare_web(json_filter):
    setup = WebSetup()
    setup.load_filters_values(file_json=json_filter)
    setup.clean_filters_values()
    filters = getattr(setup, "filters_values_dict")
    return filters


def prepare_database(filters):
    setup = DbManagement()
    setup.db_structure(filters)
    setup.db_setup(filters)
    uuid = getattr(setup, "uu_id")
    table_extend = getattr(setup, "name_extend")
    id_set = [uuid, table_extend]
    return id_set


def run_web(filters, id_set):
    with WebScraping() as bot:
        bot.main_page()
        bot.cookie_pass()
        bot.append_main_filters(filters=filters)
        bot.append_site_filters(filters=filters)
        bot.offers_by_page(filters=filters)
        bot.page_parameters()
        max_pages = getattr(bot, "all_pages")
        all_items = getattr(bot, "all_items")
        offer_per_page = int(getattr(bot, "offers_count"))
        brake_page, brake_item = 0, 0
        if const.CONTINUE_AFTER_BRAKE == True:
            bot.comm_to_start(id_set)
            brake_page = int(getattr(bot, "start_page"))
            brake_item = int(getattr(bot, "start_item"))
        page: int = 1
        item: int = 1
        loops_out = False
        try:
            while page <= max_pages:
                if loops_out == True:
                    break
                local_item = 1
                while local_item <= offer_per_page + 1:
                    if page >= brake_page and item > brake_item:
                        bot.collect_base(id_set, item, page)
                        bot.scrape_base(local_item)
                        to_drop = getattr(bot, "drop_item")
                        if to_drop == True:
                            local_item += 1
                            item += 1
                            continue
                        bot.move_in(local_item)
                        bot.scrape_extend()
                        bot.to_db(local_item)
                        if item == all_items:
                            loops_out = True
                            break
                    local_item += 1
                    item += 1
                bot.next_page()
                page += 1
        except:
            print("Program completed: " + str(item) + "/" + str(all_items))
            print("For restrore set CONTINUE_AFTER_BRAKE to True")


if __name__ == "__main__":
    filters_lst = collect_filters()
    for filter_file in filters_lst:
        otd_filters = prepare_web(filter_file)
        id_set = prepare_database(otd_filters)
        run_web(otd_filters, id_set)
