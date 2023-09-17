from difflib import SequenceMatcher
import json
import csv
import re


class WebSetup:
    def __init__(self) -> None:
        self.filters_values_dict = {}

    def load_filters_values(self, json_config=True, file_json="", custom_lst=[]):
        if json_config == True and file_json != "":
            try:
                # imprt json config files
                filters_location = "web_od/filters_options.json"
                js_options = open(filters_location, encoding="UTF-8")
                js_filters = open(file_json, encoding="UTF-8")
                filters, options = json.load(js_filters), json.load(js_options)

                # set filters
                raw_str_js = [
                    "estate",
                    "transaction",
                    "investment_type",
                    "market",
                    "owner_type",
                    "availability",
                ]
                for attr in raw_str_js:
                    filter_form = filters.get(attr)
                    match_str = HelpFunctons.str_match(filter_form, options[attr])
                    self.filters_values_dict[attr] = match_str

                manual_js = [
                    "radius",
                    "location",
                    "price",
                    "area",
                    "people_per_room",
                    "estates_on_page",
                ]
                radius_opt_js = [0, 5, 10, 15, 25, 50, 75]
                radius = filters.get(manual_js[0])
                if radius == None:
                    radius = ""
                elif isinstance(radius, str) == True:
                    radius_inp = re.split("[ \s+ | km ]", radius)[0]
                    radius = HelpFunctons.close_num(
                        radius_inp, radius_opt_js, radius=True
                    )
                else:
                    radius = HelpFunctons.close_num(radius, radius_opt_js, radius=True)
                self.filters_values_dict[manual_js[0]] = radius

                self.filters_values_dict[manual_js[1]] = filters.get(manual_js[1])

                send_js = ["price_min", "price_max", "area_min", "area_max"]
                try:
                    for send_k in send_js:
                        if send_k[:5] == manual_js[2]:
                            filter_val = filters.get(manual_js[2], {}).get(send_k)
                        else:
                            filter_val = filters.get(manual_js[3], {}).get(send_k)
                        filter_clean = HelpFunctons.min_add(filter_val)
                        self.filters_values_dict[send_k] = filter_clean
                except:
                    pass
                try:
                    people_lst, on_page_lst = range(0, 4), [24, 36, 48, 72]
                    people_per_room = HelpFunctons.close_num(
                        filters.get(manual_js[4]), people_lst
                    )
                    self.filters_values_dict[manual_js[4]] = people_per_room
                except:
                    pass
                estates_on_page = HelpFunctons.close_num(
                    filters.get(manual_js[5]), on_page_lst
                )
                self.filters_values_dict[manual_js[5]] = estates_on_page

            except:
                pass
        else:
            self.filters_values_dict = custom_lst

    def clean_filters_values(self):
        filter_lst = list(self.filters_values_dict.keys())
        char_code = (self.filters_values_dict["estate"][0]).lower()
        with open("web_od/filters_chain.csv", "r") as chains:
            reader = csv.reader(chains, delimiter=";")
            for ch in reader:
                if char_code == ch[0]:
                    chain_lst = ch[1:]
                    break

        for bridge_key in filter_lst:
            if bridge_key not in chain_lst:
                self.filters_values_dict.pop(bridge_key)


class HelpFunctons:
    @staticmethod
    def str_match(txt, options):
        if txt != "" and txt != None:
            scores = []
            for opt in options:
                score = SequenceMatcher(None, txt, opt).ratio()
                scores.append(score)
            match_opt = max(scores)
            high_score_idx = scores.index(match_opt)
            return options[high_score_idx]
        else:
            return ""

    @staticmethod
    def close_num(txt, lst, radius=False):
        to_num = float(txt)
        num = min(lst, key=lambda x: abs(x - to_num))
        if radius == True:
            num = str(num) + " km"
        return num

    @staticmethod
    def min_add(txt):
        txt = round(float(txt))
        if txt < 0 or txt == None:
            txt = 0
        return txt
