import datetime
import json
import os
import time

file_path = os.path.dirname(__file__)
daily_data_folder_path = file_path + '/data/daily_data/'
employee_data_path = file_path + '/data/employee_data.json'
translation_data_path = file_path + "/data/translation_data.json"
letters_data_path = file_path + "/data/letters_data.json"
server_data_path = file_path + "/data/server_data.json"
monthly_data_path = file_path + "/data/monthly_data.json"
waste_food_category_path = file_path + "/data/waste_food_category.json"


def get_employee_total_work_hours(department, start_date, end_date):
    output_data_list = {}
    converted_start_date = datetime.date(int(start_date[0:4]), int(start_date[5:7]),
                                         int(start_date[8:10]))
    converted_end_date = datetime.date(int(end_date[0:4]), int(end_date[5:7]),
                                       int(end_date[8:10])) + datetime.timedelta(days=1)

    if department == "dish_runner":
        while str(converted_start_date).replace("-", "") != str(converted_end_date).replace("-", ""):
            current_date = str(converted_start_date).replace("-", "")
            daily_data = get_daily_data(current_date)
            if not daily_data.get("dish_runner_work_hour"):
                converted_start_date += datetime.timedelta(days=1)
                continue
            for item in daily_data["dish_runner_work_hour"]:
                employee_total_work_hour_today = float(daily_data["dish_runner_work_hour"][item]["morning_worked_hour"]) + float(daily_data["dish_runner_work_hour"][item]["evening_worked_hour"])
                employee_name = item
                if not output_data_list.get(employee_name):
                    output_data_list[employee_name] = 0
                output_data_list[employee_name] += employee_total_work_hour_today

            converted_start_date += datetime.timedelta(days=1)

    return output_data_list


def export_employee_data_as_csv():
    temp_csv_file_path = file_path + "/temp_file/data_csv.csv"
    employee_data = get_employee_data()
    header = "employee_number," \
             "legal_name," \
             "prefer_name," \
             "server_tips_ratio," \
             "dish_prepare_tips_ratio," \
             "dish_runner_tips_ratio," \
             "appetizer_tips_ratio," \
             "cleaner_tips_ratio," \
             "host_tips_ratios," \
             "noodle_dance_tips_ratios," \
             "dish_prepare_work_count_ratio," \
             "dish_runner_work_count_ratio," \
             "appetizer_work_count_ratio\n"

    csv_output = header

    for employee in employee_data:
        csv_record = ""
        if employee_data[employee].get("employee_number"):
            csv_record += employee_data[employee]["employee_number"]
        csv_record += ","
        if employee_data[employee].get("legal_name"):
            csv_record += employee_data[employee]["legal_name"].replace(",", " ")
        csv_record += ","
        if employee_data[employee].get("prefer_name"):
            csv_record += employee_data[employee]["prefer_name"].replace(",", " ")
        csv_record += ","
        if employee_data[employee].get("server_tips_ratio"):
            csv_record += employee_data[employee]["server_tips_ratio"]
        csv_record += ","
        if employee_data[employee].get("dish_prepare_tips_ratio"):
            csv_record += employee_data[employee]["dish_prepare_tips_ratio"]
        csv_record += ","
        if employee_data[employee].get("dish_runner_tips_ratio"):
            csv_record += employee_data[employee]["dish_runner_tips_ratio"]
        csv_record += ","
        if employee_data[employee].get("appetizer_tips_ratio"):
            csv_record += employee_data[employee]["appetizer_tips_ratio"]
        csv_record += ","
        if employee_data[employee].get("cleaner_tips_ratio"):
            csv_record += employee_data[employee]["cleaner_tips_ratio"]
        csv_record += ","
        if employee_data[employee].get("host_tips_ratios"):
            csv_record += employee_data[employee]["host_tips_ratios"]
        csv_record += ","
        if employee_data[employee].get("noodle_dance_tips_ratios"):
            csv_record += employee_data[employee]["noodle_dance_tips_ratios"]
        csv_record += ","
        if employee_data[employee].get("dish_prepare_work_count_ratio"):
            csv_record += employee_data[employee]["dish_prepare_work_count_ratio"]
        csv_record += ","
        if employee_data[employee].get("dish_runner_work_count_ratio"):
            csv_record += employee_data[employee]["dish_runner_work_count_ratio"]
        csv_record += ","
        if employee_data[employee].get("appetizer_work_count_ratio"):
            csv_record += employee_data[employee]["appetizer_work_count_ratio"]
        csv_output += csv_record+"\n"

    csv_file = open(temp_csv_file_path, "w", encoding='utf-8')
    csv_file.truncate()
    csv_file.write(csv_output)
    csv_file.close()
    time.sleep(1)

    return temp_csv_file_path


def get_date_next_day(date):
    date_next_day = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8])) + datetime.timedelta(days=1)
    converted_date_next_day = str(date_next_day).replace("-", "")
    return converted_date_next_day


def get_waste_food_category():
    try:
        data_file = open(waste_food_category_path, "r", encoding="utf8")
        data_json = json.load(data_file)
        data = eval(str(data_json))
        data_file.close()
    except:
        data = {}
    return data


def change_waste_food_category(method: str,
                               change_type: str,
                               change_name: str,
                               foods_data: dict = None,
                               name_before_change: str = None):
    """
    :param foods_data: only needed if you are adding food, the data for food as dict
                        {"main_categories": "string", "secondary_categories": "string"}
    :param method: string "add", "change", or "delete" to add, change, or delete a value
    :param change_type: string of "main_categories" or "secondary_categories" or "foods"
    :param change_name: string of the change_type display name
    :param name_before_change: string of the name before change if the method is change
    """
    waste_food_category = get_waste_food_category()
    if method != "add" and method != "delete" and method != "change":
        print(1)
        return
    if change_type != "main_categories" and change_type != "secondary_categories" and change_type != "foods":
        print(2)
        return
    if change_name == "" or change_name is None:
        print(3)
        return
    if foods_data:
        foods_data["name"] = change_name
    if method == "change" and name_before_change is None:
        return

    if change_type == "main_categories":
        if method == "add":
            if change_name not in waste_food_category["main_categories"]:
                waste_food_category["main_categories"].append(change_name)
        elif method == "delete":
            if change_name in waste_food_category["main_categories"]:
                waste_food_category["main_categories"].remove(change_name)
                for food in waste_food_category["foods"]:
                    if waste_food_category["foods"][food]["main_categories"] == change_name:
                        waste_food_category["foods"][food]["main_categories"] = "None"
        elif method == "change":
            if change_name in waste_food_category["main_categories"]:
                waste_food_category["main_categories"].remove(name_before_change)
                waste_food_category["main_categories"].append(change_name)
                for food in waste_food_category["foods"]:
                    if waste_food_category["foods"][food]["main_categories"] == name_before_change:
                        waste_food_category["foods"][food]["main_categories"] = change_name
    elif change_type == "secondary_categories":
        if method == "add":
            if change_name not in waste_food_category["secondary_categories"]:
                waste_food_category["secondary_categories"].append(change_name)
        elif method == "delete":
            if change_name in waste_food_category["secondary_categories"]:
                waste_food_category["secondary_categories"].remove(change_name)
                for food in waste_food_category["foods"]:
                    if waste_food_category["foods"][food]["secondary_categories"] == change_name:
                        waste_food_category["foods"][food]["secondary_categories"] = "None"
        elif method == "change":
            if name_before_change in waste_food_category["secondary_categories"]:
                waste_food_category["secondary_categories"].remove(name_before_change)
                waste_food_category["secondary_categories"].append(change_name)
                for food in waste_food_category["foods"]:
                    if waste_food_category["foods"][food]["secondary_categories"] == name_before_change:
                        waste_food_category["foods"][food]["secondary_categories"] = change_name
    elif change_type == "foods":
        if method == "add":
            if not waste_food_category["foods"].get(change_name):
                waste_food_category["foods"][change_name] = foods_data
        elif method == "delete":
            if waste_food_category["foods"].get(change_name):
                waste_food_category["foods"].pop(change_name)
        elif method == "change":
            if waste_food_category["foods"].get(name_before_change):
                waste_food_category["foods"].pop(name_before_change)
                waste_food_category["foods"][change_name] = foods_data

    print(waste_food_category)
    file = open(waste_food_category_path, "w")
    file.truncate()
    file.write(json.dumps(waste_food_category))
    file.close()


def get_view_data(data_type, start_date, end_date):
    output_data_list = {}
    counted_dates = []
    converted_start_date = datetime.date(int(start_date[0:4]), int(start_date[5:7]),
                                         int(start_date[8:10]))
    converted_end_date = datetime.date(int(end_date[0:4]), int(end_date[5:7]),
                                       int(end_date[8:10])) + datetime.timedelta(days=1)

    print(converted_start_date)
    print(converted_end_date)

    while str(converted_start_date).replace("-", "") != str(converted_end_date).replace("-", ""):
        current_date = str(converted_start_date).replace("-", "")
        daily_data = get_daily_data(current_date)
        target_data_type = None
        try:
            if data_type == "tips_data":
                target_data_type = daily_data["close_data"]["daily_tips_count"]
            elif data_type == "busser_work_count_data":
                target_data_type = daily_data["close_data"]["daily_busser_work_count"]
            elif data_type == "kitchen_work_count_data":
                target_data_type = daily_data["close_data"]["daily_kitchen_work_count"]
            elif data_type == "take_out_work_count_data":
                target_data_type = daily_data["close_data"]["daily_take_out_bonus_data"]
            elif data_type == "wasted_food_data":
                target_data_type = daily_data["wasted_food_data"]
            else:
                raise Exception("Unknown Data Type or no such day")

            for item in target_data_type:
                if not output_data_list.get(item):
                    output_data_list[item] = {}
                output_data_list[item][current_date] = target_data_type[item]
        except Exception as e:
            print(e)
        converted_start_date += datetime.timedelta(days=1)
        counted_dates.append(current_date)

    return output_data_list, counted_dates


def view_data_to_csv(view_data, data_target="employee"):
    temp_csv_file_path = file_path + "/temp_file/data_csv.csv"
    if not os.path.exists(temp_csv_file_path):
        open(temp_csv_file_path, "a").close()
    output_data = get_view_data(view_data["data_type"], view_data["start_date"], view_data["end_date"])
    view_data_list = output_data[0]
    counted_dates = output_data[1]
    csv_file_body = None

    if data_target == "employee":
        employee_data = get_employee_data()
        header = "employee_id, prefer_name, legal_name"
        for day in counted_dates:
            header += f",{day}"

        csv_file_body = header+"\n"
        for employee in view_data_list:
            try:
                current_file_line = ""
                current_file_line += f"{str(employee_data[employee]['employee_number']).replace(',', ' ')},"
                current_file_line += f"{str(employee_data[employee]['prefer_name']).replace(',', ' ')},"
                current_file_line += f"{str(employee_data[employee]['legal_name']).replace(',', ' ')},"
                for day in counted_dates:
                    if view_data_list[employee].get(day):
                        current_file_line += f"{view_data_list[employee][day]},"
                    else:
                        current_file_line += f"0,"
                current_file_line += "\n"
                csv_file_body += current_file_line
            except Exception as e:
                print(e)
                continue
    elif data_target == "wasted_food":
        waste_food_data = get_waste_food_category()
        header = "name, main_categories, secondary_categories"
        for day in counted_dates:
            header += f",{day}"

        csv_file_body = header + "\n"
        for item in view_data_list:
            current_file_line = ""
            current_file_line += f"{str(waste_food_data['foods'][item]['name']).replace(',', ' ')},"
            current_file_line += f"{str(waste_food_data['foods'][item]['main_categories']).replace(',', ' ')},"
            current_file_line += f"{str(waste_food_data['foods'][item]['secondary_categories']).replace(',', ' ')},"
            for day in counted_dates:
                if view_data_list[item].get(day):
                    current_file_line += f"{view_data_list[item][day]},"
                else:
                    current_file_line += f"0,"
            current_file_line += "\n"
            csv_file_body += current_file_line

    csv_file = open(temp_csv_file_path, "w", encoding='utf-8')
    csv_file.truncate()
    csv_file.write(csv_file_body)
    csv_file.close()
    time.sleep(1)

    return temp_csv_file_path


def monthly_data_ymd_update(year, month, day):
    # not using
    monthly_data = get_monthly_data()

    if not monthly_data.get(year):
        monthly_data[year] = {}
    if not monthly_data[year].get(month):
        monthly_data[year][month] = {}
    if not monthly_data[year][month].get(day):
        monthly_data[year][month][day] = {}

    save_monthly_data(json.dumps(monthly_data))


def get_monthly_data():
    # not using
    data_file = open(monthly_data_path, "r", encoding="utf8")
    data_json = json.load(data_file)
    data = eval(str(data_json))
    data_file.close()
    return data


def save_monthly_data(overwrite_data):
    # not using
    file = open(monthly_data_path, "w")
    file.truncate()
    file.write(overwrite_data)
    file.close()


def get_server_data():
    data_file = open(server_data_path, "r", encoding="utf8")
    data_json = json.load(data_file)
    data = eval(str(data_json))
    data_file.close()
    return data


def save_server_data(overwrite_data):
    file = open(server_data_path, "w")
    file.truncate()
    file.write(overwrite_data)
    file.close()


def set_date_today(date):
    server_data = get_server_data()
    server_data["current_server_date"] = date
    save_server_data(json.dumps(server_data))


def get_server_date(part="all"):
    date_today = get_server_data()["current_server_date"]
    if part == "year":
        return date_today[0:4]
    elif part == "month":
        return date_today[4:6]
    elif part == "month":
        return date_today[6:8]
    else:
        return date_today


def get_current_daily_file_path():
    daily_files_path = file_path + f"/daily_files/{get_server_date()}"
    return daily_files_path


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_translation_data():
    data_file = open(translation_data_path, "r", encoding="utf8")
    data_json = json.load(data_file)
    data = eval(str(data_json))
    data_file.close()
    return data


def auth_verify(username: str, password: str):
    employees = get_employee_data()
    for employee in employees:
        if employees[employee]['employee_number'] == username:
            if employees[employee]['password'] == password:
                return True
            else:
                return False
    return False


def get_employee_data() -> dict:
    employees_data_file = open(employee_data_path, "r")
    employees_data_json = json.load(employees_data_file)
    employees = eval(str(employees_data_json))
    employees_data_file.close()
    return employees


def get_current_employee_data(username: str):
    employees = get_employee_data()
    current_employee_data = employees[username]
    return current_employee_data


def get_daily_data(date=None) -> dict:
    if date is None:
        date = get_server_date()
    daily_data_path = daily_data_folder_path + f"{date}.json"
    try:
        file = open(daily_data_path, "r")
        file_json = json.load(file)
        data = eval(str(file_json))
        file.close()
        return data
    except Exception as e:
        print(e.args[0])
        return {}


def save_daily_data_as_json(overwrite_data, date=None):
    if date is None:
        date = get_server_date()
    daily_data_path = daily_data_folder_path + f"{date}.json"
    if not os.path.exists(daily_data_path):
        open(daily_data_path, "a").close()
    file = open(daily_data_path, "w")
    file.truncate()
    file.write(overwrite_data)
    file.close()


def save_employee_data_as_json(overwrite_data):
    file = open(employee_data_path, "w")
    file.truncate()
    file.write(overwrite_data)
    file.close()


def get_letters_data() -> dict:
    try:
        file = open(letters_data_path, "r")
        file_json = json.load(file)
        data = eval(str(file_json))
        file.close()
        return data
    except Exception as e:
        print(e.args[0])
        return {}


def save_letters_data_as_json(overwrite_data):
    file = open(letters_data_path, "w")
    file.truncate()
    file.write(str(overwrite_data))
    file.close()


def check_if_can_daily_close(date=None):
    if date is None:
        date = get_server_date()
    daily_data = get_daily_data(date)

    # 检查小吃工时是否正确
    appetizer_error_text = "appetizer_work_hour_error"
    try:
        if not daily_data["appetizer_work_hour"]:
            raise Exception
        for item in daily_data["appetizer_work_hour"]:
            float(daily_data["appetizer_work_hour"][item]['worked_hour'])
    except Exception as e:
        return False, appetizer_error_text

    # 检查保洁工时是否正确
    cleaner_error_text = "cleaner_work_hour_error"
    try:
        if not daily_data["cleaner_work_hour"]:
            raise Exception
        for item in daily_data["cleaner_work_hour"]:
            float(daily_data["cleaner_work_hour"][item])
    except Exception as e:
        return False, cleaner_error_text

    # 检查上菜口工时是否正确
    dish_prepare_error_text = "dish_prepare_work_hour_error"
    try:
        if not daily_data["dish_prepare_work_hour"]:
            raise Exception
    except Exception as e:
        return False, dish_prepare_error_text

    # 检查传配工时是否正确
    dish_runner_error_text = "dish_runner_hour_error"
    try:
        if not daily_data["dish_runner_work_hour"]:
            raise Exception
    except Exception as e:
        return False, dish_runner_error_text

    # 检查日常数据是否正确
    general_data_error_text = "general_data_error"
    try:
        if not daily_data["general_data"]:
            raise Exception
    except Exception as e:
        return False, general_data_error_text

    # 检查门迎工时是否正确
    host_work_hour_error_text = "host_work_hour_error"
    try:
        if not daily_data["host_work_hour"]:
            raise Exception
    except Exception as e:
        return False, host_work_hour_error_text

    # 检查管理，特岗工时是否正确
    manager_work_hour_error_text = "manager_work_hour_error"
    try:
        if not daily_data["manager_daily_work_info_info"]:
            raise Exception
    except Exception as e:
        return False, manager_work_hour_error_text

    return True, "good"
