import web_od.constans as const
from os import listdir
import sqlite3
import json
from datetime import datetime
import uuid


class DbManagement:
    def __init__(self, name=const.DB_NAME, path=const.DB_PATH, close=False) -> None:
        self.name = name
        self.path = path
        self.db_path = self.path + self.name
        self.close = close

    def db_structure(self, filters):
        # all db types in one layer dict
        self.db_types = {}

        estate = filters.get("estate")
        estate_constr = estate[:3].lower()
        second_lvl: str = ""
        if estate == "Inwestycje":
            second_lvl = "investment_type"
        else:
            second_lvl = "transaction"
        transaction = filters.get(second_lvl)
        transaction_constr = transaction[3:6]
        name_dict = {"Na sprzedaż": "sell", "Na wynajem": "rent"}
        name_lst = list(name_dict.keys())
        if transaction == name_lst[0]:
            transaction = name_dict["Na sprzedaż"]
        elif transaction == name_lst[1]:
            transaction = name_dict["Na wynajem"]
        else:
            transaction = "all"

        # imprt json database structure
        db_structure_location = "web_od/db_structure.json"
        db_structure = open(db_structure_location, encoding="UTF-8")
        db_structure = json.load(db_structure)

        self.db_types["filters"] = db_structure.get("form")
        self.db_types["base"] = db_structure.get("lvl-0")
        top_layer = db_structure.get(estate)

        for top_key, child_element in top_layer.items():
            structure_elements = child_element.get(transaction)
            found_element = True if (transaction and structure_elements) else False
            if found_element == True:
                self.db_types[top_key] = structure_elements

        self.db_types["page"] = db_structure.get("lvl-3")

        # create name extend
        self.name_extend = "_" + estate_constr + transaction_constr

    def db_setup(self, filters):
        try:
            conn = sqlite3.connect(self.db_path + ".db")

            # add "approach_id" table + values
            cursor = conn.cursor()
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS approach_id (uu_id INTEGER, uu_date TEXT, uu_time TEXT);"""
            )
            if const.CONTINUE_AFTER_BRAKE == False:
                self.uu_id = str(uuid.uuid4())
            else:
                cursor.execute(
                    "SELECT uu_id FROM approach_id ORDER BY rowid DESC LIMIT 1"
                )
                self.uu_id = cursor.fetchone()[0]
            current_day = datetime.now().strftime("%d/%m/%Y")
            current_time = datetime.now().strftime("%H:%M:%S")
            date_time = [self.uu_id, current_day, current_time]
            cursor.execute("INSERT INTO approach_id VALUES (?,?,?);", date_time)

            # add "filters_record" table + values
            form_elements = self.db_types["filters"]
            filter_types = [i.split("|") for i in form_elements]
            ct_name = "filters_record"
            ct_filters = DbStatic.ct_list(ct_name, filter_types)
            cursor.execute(ct_filters)
            filters_val = [["uuid", self.uu_id]]
            else_filters_val = [list(val) for val in filters.items()]
            filters_val.extend(else_filters_val)
            for look in filters_val:
                if look[0] == "transaction":
                    look[0] = "transaction_type"
            ir_insert, ir_values = DbStatic.ir_tuple(ct_name, filters_val, filter_types)
            cursor.execute(ir_insert, ir_values)

            # add "base_info", "specific_info", "additional_info" tables
            info_tables, position = ["base", "specific", "additional", "page"], 0
            tables = ["base_info", "specific_info", "additional_info", "page_info"]
            tables_names = [
                table + self.name_extend
                if table != "base_info" and table != "page_info"
                else table
                for table in tables
            ]
            for table in info_tables:
                elements = self.db_types[table]
                types = [i.split("|") for i in elements]
                name = tables_names[position]
                create_table = DbStatic.ct_list(name, types)
                position += 1
                cursor.execute(create_table)

            conn.commit()

        finally:
            if conn:
                conn.close()

    def old_uuid(self):
        pass


class DbStatic:
    @staticmethod
    def ct_list(name, lst):
        ct_start = "CREATE TABLE IF NOT EXISTS " + name + " ("
        ct_end = ");"
        ct_core = ""
        for pair in lst:
            queue = ", " + pair[0] + " " + pair[1]
            ct_core += queue
        ct_core = ct_core[2:]
        create_table = ct_start + ct_core + ct_end
        return create_table

    @staticmethod
    def ir_tuple(name, tpl_val, lst_col):
        all_values = []
        ir_start = f"INSERT INTO {name} VALUES ("
        ir_end = ");"
        ir_core = ""
        for t in range(0, 15):
            ir_core += ", ?"
        ir_core = ir_core[2:]

        for pair in lst_col:
            found = False
            for val in tpl_val:
                if pair[0] == val[0]:
                    all_values.append([pair[0], val[1]])
                    found = True
                    break
            if found == False:
                all_values.append([pair[0], None])
            else:
                pass

        all_values = tuple(i[1] for i in all_values)
        insert_values = ir_start + ir_core + ir_end
        return insert_values, all_values
