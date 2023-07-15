import json
import random
import string
import openpyxl


employees = {}
employee_data_file_path = "other/employee_data_sheet.xlsx"
data_sheet_wb = openpyxl.load_workbook(employee_data_file_path)
data_sheet_ws = data_sheet_wb.active

for row in range(1, data_sheet_ws.max_row+1):
    try:
        int(data_sheet_ws[f"B{row}"].value)
        current_employee = {"employee_number": str(data_sheet_ws[f"B{row}"].value),
                            "legal_name": str(data_sheet_ws[f"D{row}"].value),
                            "prefer_name": str(data_sheet_ws[f"C{row}"].value),
                            "server_tips_ratio": str(data_sheet_ws[f"E{row}"].value),
                            "dish_prepare_tips_ratio": str(data_sheet_ws[f"F{row}"].value),
                            "dish_runner_tips_ratio": str(data_sheet_ws[f"G{row}"].value),
                            "appetizer_tips_ratio": str(data_sheet_ws[f"H{row}"].value),
                            "cleaner_tips_ratio": str(data_sheet_ws[f"I{row}"].value),
                            "host_tips_ratios": str(data_sheet_ws[f"J{row}"].value),
                            "noodle_dance_tips_ratios": str(data_sheet_ws[f"K{row}"].value),
                            "dish_prepare_work_count_ratio": str(data_sheet_ws[f"F{row}"].value),
                            "dish_runner_work_count_ratio": str(data_sheet_ws[f"G{row}"].value),
                            "appetizer_work_count_ratio": str(data_sheet_ws[f"H{row}"].value),
                            "password": f"{random.randint(1,999)}{random.choice(string.ascii_letters)}{random.randint(1,999)}",
                            "manage_appetizer": False,
                            "manage_cleaner": False,
                            "manage_dish_prepare": False,
                            "manage_dish_runner": False,
                            "manage_server": False,
                            "manage_noodle_dance": False,
                            "manage_host": False,
                            "manage_managers": False,
                            "super_manager": False,
                            }
        employees[current_employee["employee_number"]] = current_employee

    except Exception as e:
        pass

file = open('website/data/employee_data.json', "w")
file.truncate()
file.write(json.dumps(employees))
file.close()
