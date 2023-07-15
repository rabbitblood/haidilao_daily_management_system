import json
import random

from flask import Blueprint, render_template, request, session, redirect, send_file
from website import data_handler
from website.data_handler import get_letters_data, get_daily_data, get_translation_data, get_employee_data, \
    get_current_employee_data, save_letters_data_as_json, save_daily_data_as_json, is_float, auth_verify
from website import daily_close_handler

work_schedule_section = Blueprint("work_schedule_section", __name__)


@work_schedule_section.route("/work_schedule/edit_server_available_work_time", methods=['GET', 'POST'])
def edit_server_available_work_time():
    route_path = "/work_schedule/edit_server_available_work_time"
    template_path = "work_schedule/edit_server_available_work_time.html"

    # 验证用户
    if not session.get("user"):
        return render_template("login.html")
    if not auth_verify(session["user"], session["password"]):
        session.clear()
        return render_template("login.html", error="login information changed")

    # web respond
    if request.method == "POST":
        form_data = request.form.to_dict()
        employee_data = data_handler.get_employee_data()
        employee_data[form_data['employee_number']]['available_working_time'] = form_data
        data_handler.save_employee_data_as_json(json.dumps(employee_data))
        return render_template(template_path,
                               success_info="submit_success",
                               userinfo=get_current_employee_data(session['user']),
                               posturl=route_path,
                               employee_data=data_handler.get_employee_data())
    elif request.method == "GET":
        return render_template(template_path,
                               userinfo=get_current_employee_data(session['user']),
                               employee_data=data_handler.get_employee_data(),
                               posturl=route_path)


@work_schedule_section.route("/work_schedule/generate_work_time_sheet", methods=['GET', 'POST'])
def generate_work_time_sheet():
    route_path = "/work_schedule/generate_work_time_sheet"
    template_path = "work_schedule/generate_new_work_time_sheet.html"

    # 验证用户
    if not session.get("user"):
        return render_template("login.html")
    if not auth_verify(session["user"], session["password"]):
        session.clear()
        return render_template("login.html", error="login information changed")

    # web respond
    if request.method == "POST":
        form_data = request.form.to_dict()
        employee_data = data_handler.get_employee_data()
        work_schedule_data = form_data
        employee_available_work_times = {
            "monday_morning": [],
            "monday_evening": [],
            "tuesday_morning": [],
            "tuesday_evening": [],
            "wednesday_morning": [],
            "wednesday_evening": [],
            "thursday_morning": [],
            "thursday_evening": [],
            "friday_morning": [],
            "friday_evening": [],
            "saturday_morning": [],
            "saturday_evening": [],
            "sunday_morning": [],
            "sunday_evening": []
        }
        generated_schedule = {
            "sunday": {
                "sunday_morning": [],
                "sunday_evening": []
            },
            "monday": {
                "monday_morning": [],
                "monday_evening": []
            },
            "tuesday": {
                "tuesday_morning": [],
                "tuesday_evening": []
            },
            "wednesday": {
                "wednesday_morning": [],
                "wednesday_evening": []
            },
            "thursday": {
                "thursday_morning": [],
                "thursday_evening": []
            },
            "friday": {
                "friday_morning": [],
                "friday_evening": []
            },
            "saturday": {
                "saturday_morning": [],
                "saturday_evening": []
            }
        }
        day_info = {
            "monday_morning": {
                "shift": "monday_morning",
                "week_or_weekend_max": "week_day_morning_max",
                "ok_check": False,
                'senior_needed': 1,
                'same_day_shift': 'monday_evening',
                'day': 'monday'
            },
            "monday_evening": {
                "shift": "monday_evening",
                "week_or_weekend_max": "week_day_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'monday_morning',
                'day': 'monday'
            },
            "tuesday_morning": {
                "shift": "tuesday_morning",
                "week_or_weekend_max": "week_day_morning_max",
                "ok_check": False,
                'senior_needed': 1,
                'same_day_shift': 'tuesday_evening',
                'day': 'tuesday'
            },
            "tuesday_evening": {
                "shift": "tuesday_evening",
                "week_or_weekend_max": "week_day_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'tuesday_morning',
                'day': 'tuesday'
            },
            "wednesday_morning": {
                "shift": "wednesday_morning",
                "week_or_weekend_max": "week_day_morning_max",
                "ok_check": False,
                'senior_needed': 1,
                'same_day_shift': 'wednesday_evening',
                'day': 'wednesday'
            },
            "wednesday_evening": {
                "shift": "wednesday_evening",
                "week_or_weekend_max": "week_day_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'wednesday_morning',
                'day': 'wednesday'
            },
            "thursday_morning": {
                "shift": "thursday_morning",
                "week_or_weekend_max": "week_day_morning_max",
                "ok_check": False,
                'senior_needed': 1,
                'same_day_shift': 'thursday_evening',
                'day': 'thursday'
            },
            "thursday_evening": {
                "shift": "thursday_evening",
                "week_or_weekend_max": "week_day_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'thursday_morning',
                'day': 'thursday'
            },
            "friday_morning": {
                "shift": "friday_morning",
                "week_or_weekend_max": "weekend_morning_max",
                "ok_check": False,
                'senior_needed': 1,
                'same_day_shift': 'friday_evening',
                'day': 'friday'
            },
            "friday_evening": {
                "shift": "friday_evening",
                "week_or_weekend_max": "weekend_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'friday_morning',
                'day': 'friday'
            },
            "saturday_morning": {
                "shift": "saturday_morning",
                "week_or_weekend_max": "weekend_morning_max",
                "ok_check": False,
                'senior_needed': 2,
                'same_day_shift': 'saturday_evening',
                'day': 'saturday'
            },
            "saturday_evening": {
                "shift": "saturday_evening",
                "week_or_weekend_max": "weekend_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'saturday_morning',
                'day': 'saturday'
            },
            "sunday_morning": {
                "shift": "sunday_morning",
                "week_or_weekend_max": "weekend_morning_max",
                "ok_check": False,
                'senior_needed': 2,
                'same_day_shift': 'sunday_evening',
                'day': 'sunday'
            },
            "sunday_evening": {
                "shift": "sunday_evening",
                "week_or_weekend_max": "weekend_evening_max",
                "ok_check": False,
                'senior_needed': 3,
                'same_day_shift': 'sunday_morning',
                'day': 'sunday'
            }
        }
        working_employee = []
        for employee in employee_data:
            if employee_data[employee].get("available_working_time"):
                if employee_data[employee]["available_working_time"].get("monday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["monday_can_work_morning"] == "on":
                    employee_available_work_times["monday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("monday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["monday_can_work_night"] == "on":
                    employee_available_work_times["monday_evening"].append(employee)

                if employee_data[employee]["available_working_time"].get("tuesday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["tuesday_can_work_morning"] == "on":
                    employee_available_work_times["tuesday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("tuesday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["tuesday_can_work_night"] == "on":
                    employee_available_work_times["tuesday_evening"].append(employee)

                if employee_data[employee]["available_working_time"].get("wednesday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["wednesday_can_work_morning"] == "on":
                    employee_available_work_times["wednesday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("wednesday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["wednesday_can_work_night"] == "on":
                    employee_available_work_times["wednesday_evening"].append(employee)

                if employee_data[employee]["available_working_time"].get("thursday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["thursday_can_work_morning"] == "on":
                    employee_available_work_times["thursday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("thursday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["thursday_can_work_night"] == "on":
                    employee_available_work_times["thursday_evening"].append(employee)

                if employee_data[employee]["available_working_time"].get("friday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["friday_can_work_morning"] == "on":
                    employee_available_work_times["friday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("friday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["friday_can_work_night"] == "on":
                    employee_available_work_times["friday_evening"].append(employee)

                if employee_data[employee]["available_working_time"].get("saturday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["saturday_can_work_morning"] == "on":
                    employee_available_work_times["saturday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("saturday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["saturday_can_work_night"] == "on":
                    employee_available_work_times["saturday_evening"].append(employee)

                if employee_data[employee]["available_working_time"].get("sunday_can_work_morning") \
                        and employee_data[employee]["available_working_time"]["sunday_can_work_morning"] == "on":
                    employee_available_work_times["sunday_morning"].append(employee)

                if employee_data[employee]["available_working_time"].get("sunday_can_work_night") \
                        and employee_data[employee]["available_working_time"]["sunday_can_work_night"] == "on":
                    employee_available_work_times["sunday_evening"].append(employee)
        while True:
            for shift in day_info:
                day_info[shift]["ok_check"] = True

            for shift in day_info:
                current_shift = day_info[shift]
                if len(generated_schedule[current_shift['day']][current_shift["shift"]]) \
                        < int(work_schedule_data[current_shift["week_or_weekend_max"]]):
                    current_senior_count = 0
                    for employee in generated_schedule[current_shift['day']][current_shift["shift"]]:
                        if float(employee_data[employee]['server_tips_ratio']) == 6:
                            current_senior_count += 1
                    if current_senior_count < current_shift["senior_needed"]:
                        random.shuffle(employee_available_work_times[current_shift["shift"]])
                        for employee in employee_available_work_times[current_shift["shift"]]:
                            current_employee_working_days = 0
                            for day in generated_schedule:
                                for day_shift in generated_schedule[day]:
                                    if employee in generated_schedule[day][day_shift]:
                                        current_employee_working_days += 1
                            if employee not in generated_schedule[current_shift['day']][current_shift["shift"]] \
                                    and float(employee_data[employee]['server_tips_ratio']) == 6\
                                    and current_employee_working_days < int(employee_data[employee]['can_work_days_in_a_week'])\
                                    and employee not in generated_schedule[current_shift['day']][current_shift['same_day_shift']]:
                                generated_schedule[current_shift['day']][current_shift["shift"]].append(employee)
                                if employee not in working_employee:
                                    working_employee.append(employee)
                                current_shift["ok_check"] = False
                                break
                    if current_shift["ok_check"]:
                        random.shuffle(employee_available_work_times[current_shift["shift"]])
                        for employee in employee_available_work_times[current_shift["shift"]]:
                            current_employee_working_days = 0
                            for day in generated_schedule:
                                for day_shift in generated_schedule[day]:
                                    if employee in generated_schedule[day][day_shift]:
                                        current_employee_working_days += 1
                            if employee not in generated_schedule[current_shift['day']][current_shift["shift"]]\
                                    and current_employee_working_days < int(employee_data[employee]['can_work_days_in_a_week'])\
                                    and employee not in generated_schedule[current_shift['day']][current_shift['same_day_shift']]:
                                generated_schedule[current_shift['day']][current_shift["shift"]].append(employee)
                                if employee not in working_employee:
                                    working_employee.append(employee)
                                current_shift["ok_check"] = False
                                break

            all_ok = True
            for shift in day_info:
                if day_info[shift]["ok_check"] is False:
                    all_ok = False
                    break

            if all_ok:
                break

        # noinspection PyTypeChecker
        work_schedule_data["employee_available_work_times"] = employee_available_work_times
        # noinspection PyTypeChecker
        work_schedule_data["generated_schedule"] = generated_schedule
        # noinspection PyTypeChecker
        work_schedule_data["working_employee"] = working_employee
        # noinspection PyTypeChecker
        work_schedule_data["day_info"] = day_info
        # noinspection PyTypeChecker
        work_schedule_data["work_schedule_data_json"] = json.dumps(work_schedule_data).encode("utf-8")
        print(work_schedule_data)

        return render_template(template_path,
                               employee_data=employee_data,
                               posturl=route_path,
                               work_schedule_data=work_schedule_data)
    elif request.method == "GET":
        return render_template(template_path,
                               employee_data=data_handler.get_employee_data(),
                               posturl=route_path)
