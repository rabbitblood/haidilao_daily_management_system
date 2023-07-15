import json

from flask import Blueprint, render_template, request, session, redirect, send_file
from website import data_handler
from website.data_handler import get_letters_data, get_daily_data, get_translation_data, get_employee_data, \
    get_current_employee_data, save_letters_data_as_json, save_daily_data_as_json, is_float, auth_verify
from website import daily_close_handler

manage_section = Blueprint("manage_section", __name__)


@manage_section.route("/manage/manage_appetizer_daily_work_info", methods=['GET', 'POST'])
def manage_appetizer_daily_work_info():
    route_path = "/manage/manage_appetizer_daily_work_info"
    tempate_path = "manage/manage_appetizer.html"
    department_json_data_name = "appetizer_work_hour"
    if request.method == "POST":
        work_time_data = dict(eval(request.form.get("department_work_time_data")))
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if "" in work_time_data:
            work_time_data.pop("")
        copy_work_time_data = work_time_data.copy()
        for key in copy_work_time_data:
            if copy_work_time_data[key]["worked_hour"] == "":
                work_time_data.pop(key)
        try:
            for key in work_time_data:
                if not key.split(" ")[0].isdigit() or not is_float(work_time_data[key]["worked_hour"]):
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(date=current_view_and_edit_date),
                                           date=current_view_and_edit_date,
                                           error="wrong_format",
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path)
        except Exception as e:
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   error="wrong format",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name] = work_time_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url=route_path,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_cleaner_daily_work_info", methods=['GET', 'POST'])
def manage_cleaner_daily_work_info():
    route_path = "/manage/manage_cleaner_daily_work_info"
    tempate_path = "manage/manage_cleaner.html"
    department_json_data_name = "cleaner_work_hour"
    if request.method == "POST":
        work_time_data = dict(eval(request.form.get("department_work_time_data")))
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        if "" in work_time_data:
            work_time_data.pop("")
        copy_work_time_data = work_time_data.copy()
        for key in copy_work_time_data:
            if copy_work_time_data[key] == "":
                work_time_data.pop(key)
        try:
            for key in work_time_data:
                if not key.split(" ")[0].isdigit() or not is_float(work_time_data[key]):
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(date=current_view_and_edit_date),
                                           date=current_view_and_edit_date,
                                           error="wrong_format",
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path)
        except Exception as e:
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   error="wrong format",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name] = work_time_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        print(get_daily_data(date=current_view_and_edit_date))
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url=route_path,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_dish_prepare_daily_work_info", methods=['GET', 'POST'])
def manage_dish_prepare_daily_work_info():
    route_path = "/manage/manage_dish_prepare_daily_work_info"
    tempate_path = "manage/manage_dish_prepare.html"
    department_json_data_name = "dish_prepare_work_hour"
    if request.method == "POST":
        work_time_data = request.form.to_dict()
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        try:
            for item in work_time_data:
                if not "work_hour" in item:
                    if work_time_data[item] == "":
                        work_time_data[item + "_work_hour"] = ""
                    else:
                        int(work_time_data[item].split(" ")[0])
                    if work_time_data[item + "_work_hour"] == "":
                        work_time_data[item] = ""
        except Exception as e:
            print(e.args[0])
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date, error="wrong format",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name] = work_time_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               success_info="submit_success",
                               department_json_data_name=department_json_data_name,
                               post_url=route_path)
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_noodle_dance_daily_work_info", methods=['GET', 'POST'])
def manage_noodle_dance_daily_work_info():
    route_path = "/manage/manage_noodle_dance_daily_work_info"
    tempate_path = "manage/manage_noodle_dance.html"
    department_json_data_name = "noodle_dance_work_hour"
    if request.method == "POST":
        work_time_data = dict(eval(request.form.get("department_work_time_data")))
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        if "" in work_time_data:
            work_time_data.pop("")
        copy_work_time_data = work_time_data.copy()
        for key in copy_work_time_data:
            if copy_work_time_data[key] == "":
                work_time_data.pop(key)
        try:
            for key in work_time_data:
                if not key.split(" ")[0].isdigit() or not is_float(work_time_data[key]):
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(date=current_view_and_edit_date),
                                           date=current_view_and_edit_date,
                                           error="wrong_format",
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path)
        except Exception as e:
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   error="wrong format",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name] = work_time_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        print(get_daily_data(date=current_view_and_edit_date))
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url=route_path,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_host_daily_work_info", methods=['GET', 'POST'])
def manage_host_daily_work_info():
    route_path = "/manage/manage_host_daily_work_info"
    tempate_path = "manage/manage_host.html"
    department_json_data_name = "host_work_hour"
    if request.method == "POST":
        work_time_data = dict(eval(request.form.get("department_work_time_data")))
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        if "" in work_time_data:
            work_time_data.pop("")
        copy_work_time_data = work_time_data.copy()
        for key in copy_work_time_data:
            if copy_work_time_data[key]["worked_hour"] == "":
                work_time_data.pop(key)
        try:
            for key in work_time_data:
                if not key.split(" ")[0].isdigit() or not is_float(work_time_data[key]["worked_hour"]):
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(date=current_view_and_edit_date),
                                           date=current_view_and_edit_date,
                                           error="wrong_format",
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path)
        except Exception as e:
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   error="wrong format",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name] = work_time_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        print(get_daily_data(date=current_view_and_edit_date))
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url=route_path,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_dish_runner_daily_work_info", methods=['GET', 'POST'])
def manage_dish_runner_daily_work_info():
    route_path = "/manage/manage_dish_runner_daily_work_info"
    tempate_path = "manage/manage_dish_runner.html"
    department_json_data_name = "dish_runner_work_hour"
    if request.method == "POST":
        work_time_data = dict(eval(request.form.get("department_work_time_data")))
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        if "" in work_time_data:
            work_time_data.pop("")
        copy_work_time_data = work_time_data.copy()
        for key in copy_work_time_data:
            if (copy_work_time_data[key]["evening_worked_hour"] == "" or copy_work_time_data[key][
                "evening_worked_hour"] == "0") \
                    and (copy_work_time_data[key]["morning_worked_hour"] == "" or copy_work_time_data[key][
                "morning_worked_hour"] == "0"):
                work_time_data.pop(key)
            else:
                if copy_work_time_data[key]["evening_worked_hour"] == "":
                    copy_work_time_data[key]["evening_worked_hour"] = "0"
                if copy_work_time_data[key]["morning_worked_hour"] == "":
                    copy_work_time_data[key]["morning_worked_hour"] = "0"
        try:
            for key in work_time_data:
                if not key.split(" ")[0].isdigit() \
                        or not is_float(work_time_data[key]["morning_worked_hour"]) \
                        or not is_float(work_time_data[key]["evening_worked_hour"]):
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(date=current_view_and_edit_date),
                                           date=current_view_and_edit_date,
                                           error="wrong format",
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path)
        except Exception as e:
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   error="wrong format",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name] = work_time_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url=route_path,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_server_daily_work_info", methods=['GET', 'POST'])
def manage_server_daily_work_info():
    route_path = "/manage/manage_server_daily_work_info"
    tempate_path = "manage/manage_server.html"
    department_json_data_name = "server_group_info"
    if request.method == "POST":
        form_data = request.form.to_dict()
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        if form_data.get("delete_group"):
            daily_data = get_daily_data(date=current_view_and_edit_date)
            daily_data[department_json_data_name].pop(form_data["delete_group"])
            save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=data_handler.get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path,
                                   str=str)
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path,
                                       str=str)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_server_daily_work_info/add_group", methods=['GET', 'POST'])
def manage_server_daily_work_info_add_group():
    route_path = "/manage/manage_server_daily_work_info/add_group"
    tempate_path = "manage/manage_server_add_group.html"
    department_json_data_name = "server_group_info"
    if request.method == "POST":
        server_group_data = request.form.to_dict()
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        team_members_not_empty = False
        transfer_members_not_empty = False
        try:
            print(str(server_group_data))
            print(server_group_data["group_name"])
            if server_group_data["group_name"] == "":
                raise Exception("shift empty")
            for item in server_group_data:
                if "team_member" in item and "work_hour" not in item:
                    if server_group_data[item] != "":
                        if server_group_data[item + "_work_hour"] == "":
                            server_group_data[item + "_work_hour"] = "8"
                        int(server_group_data[item].split(" ")[0])
                        team_members_not_empty = True
            for item in server_group_data:
                if "transfer_member" in item and "work_hour" not in item:
                    if server_group_data[item] != "":
                        if server_group_data[item + "_work_hour"] == "":
                            server_group_data[item + "_work_hour"] = "8"
                        int(server_group_data[item].split(" ")[0])
                        transfer_members_not_empty = True
            if team_members_not_empty is False:
                raise Exception("no team member")
        except Exception as e:
            print(e.args[0])
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date, error="error",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        if transfer_members_not_empty:
            server_group_data["has_transfer_group"] = "True"
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name][
            server_group_data["group_name"]] = server_group_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        return render_template("manage/manage_server.html",
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=data_handler.get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url="/manage/manage_server_daily_work_info",
                               str=str,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("current_view_and_edit_date") and request.args["current_view_and_edit_date"] is not None:
                    view_date = str(request.args["current_view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                if request.args.get("edit_group") is not None:
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=daily_data,
                                           date=view_date,
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path,
                                           edit_group=request.args.get("edit_group"),
                                           str=str)
                else:
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=daily_data,
                                           date=view_date,
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path,
                                           edit_group="None",
                                           str=str)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_manager_and_other_daily_work_info", methods=['GET', 'POST'])
def manage_manager_daily_work_info():
    route_path = "/manage/manage_manager_and_other_daily_work_info"
    tempate_path = "manage/manage_manager_and_other.html"
    department_json_data_name = "manager_daily_work_info_info"
    if request.method == "POST":
        form_data = request.form.to_dict()
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        daily_data = get_daily_data(date=current_view_and_edit_date)
        daily_data[department_json_data_name] = form_data
        save_daily_data_as_json(json.dumps(daily_data),date=current_view_and_edit_date)
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=daily_data,
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url=route_path,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/general_setting", methods=['GET', 'POST'])
def general_setting():
    route_path = "/manage/general_setting"
    tempate_path = "manage/general_settings.html"
    department_json_data_name = "general_setting"
    if request.method == "POST":
        form_data = request.form.to_dict()
        data_handler.set_date_today(form_data["date"])
        return redirect("/manage")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=get_daily_data(),
                                       date=data_handler.get_server_date(),
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/general_setting/daily_close_and_get_file", methods=['POST'])
def daily_close_and_get_file():
    route_path = "/manage/general_setting"
    tempate_path = "manage/general_settings.html"
    department_json_data_name = "general_setting"
    if session.get("user"):
        if auth_verify(session["user"], session["password"]):

            if data_handler.check_if_can_daily_close()[0]:
                return send_file(daily_close_handler.daily_close_and_get_file())
            else:
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=get_daily_data(),
                                       date=data_handler.get_server_date(),
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path,
                                       error=data_handler.check_if_can_daily_close()[1])
        else:
            session.clear()
            return render_template("login.html", error="login information changed")
    else:
        return render_template("login.html")


@manage_section.route("/manage/daily_close_infos", methods=['GET', 'POST'])
def daily_close_infos():
    tempate_path = "manage/daily_close_infos.html"
    if not session.get("user"):
        return render_template("login.html")
    if not auth_verify(session["user"], session["password"]):
        session.clear()
        return render_template("login.html", error="login information changed")

    if request.method == "GET":
        if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
            view_date = str(request.args["view_and_edit_date"]).replace("-", "")
        else:
            view_date = data_handler.get_server_date()
        daily_data = get_daily_data(view_date)
        return render_template(tempate_path,
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=daily_data,
                               date=view_date)
    elif request.method == "POST":
        form_data = dict(eval(str(request.form.get("general_data"))))
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get("general_data"):
            daily_data["general_data"] = {}
        daily_data["general_data"]['morning_table_count'] = form_data['morning_table_count']
        if daily_data["general_data"]['morning_table_count'] == "":
            daily_data["general_data"]['morning_table_count'] = 0
        daily_data["general_data"]['evening_table_count'] = form_data['evening_table_count']
        if daily_data["general_data"]['evening_table_count'] == "":
            daily_data["general_data"]['evening_table_count'] = 0
        daily_data["general_data"]['take_out_count'] = form_data['take_out_count']
        if daily_data["general_data"]['take_out_count'] == "":
            daily_data["general_data"]['take_out_count'] = 0
        daily_data["general_data"]['morning_busser_help_count'] = form_data['morning_busser_help_count']
        if daily_data["general_data"]['morning_busser_help_count'] == "":
            daily_data["general_data"]['morning_busser_help_count'] = 0
        daily_data["general_data"]['evening_busser_help_count'] = form_data['evening_busser_help_count']
        if daily_data["general_data"]['evening_busser_help_count'] == "":
            daily_data["general_data"]['evening_busser_help_count'] = 0
        daily_data["general_data"]["tips_give_out_from_department"] = form_data['tips_give_out_from_department']
        copy_of_tips_give_out_from_department = dict(daily_data["general_data"]["tips_give_out_from_department"]).copy()
        for item in copy_of_tips_give_out_from_department:
            if copy_of_tips_give_out_from_department[item]["employee_name"] == "":
                daily_data["general_data"]["tips_give_out_from_department"].pop(item)
            elif copy_of_tips_give_out_from_department[item]["amount"] == "":
                daily_data["general_data"]["tips_give_out_from_department"].pop(item)

        daily_data["general_data"]["tips_adjustment"] = form_data['tips_adjustment']
        copy_of_tips_adjustment = dict(daily_data["general_data"]["tips_adjustment"]).copy()
        for item in copy_of_tips_adjustment:
            if copy_of_tips_adjustment[item]["employee_name"] == "":
                daily_data["general_data"]["tips_adjustment"].pop(item)
            elif copy_of_tips_adjustment[item]["amount"] == "":
                daily_data["general_data"]["tips_adjustment"].pop(item)
        data_handler.save_daily_data_as_json(json.dumps(daily_data),
                                             date=current_view_and_edit_date)
        return redirect("/manage")


@manage_section.route("/manage/employee_data_view_and_edit", methods=['GET'])
def employee_data_view_and_edit():
    tempate_path = "manage/employee_data_view_and_edit.html"
    if session.get("user"):
        if auth_verify(session["user"], session["password"]):
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(),
                                   date=data_handler.get_server_date())
        else:
            session.clear()
            return render_template("login.html", error="login information changed")
    else:
        return render_template("login.html")


@manage_section.route("/manage/employee_data_view_and_edit/edit_employee", methods=['GET', 'POST'])
def employee_data_view_and_edit_edit_employee():
    tempate_path = "manage/employee_data_view_and_edit_edit_employee.html"
    if request.method == "POST":
        form_data = request.form.to_dict()
        employee_data = data_handler.get_employee_data()

        if not employee_data.get(form_data["employee_number"]):
            employee_data[form_data["employee_number"]] = {}

        employee_data[form_data["employee_number"]]["employee_number"] = form_data["employee_number"]
        employee_data[form_data["employee_number"]]["legal_name"] = form_data["legal_name"]
        employee_data[form_data["employee_number"]]["prefer_name"] = form_data["prefer_name"]
        employee_data[form_data["employee_number"]]["server_tips_ratio"] = form_data["server_tips_ratio"]
        employee_data[form_data["employee_number"]]["dish_prepare_tips_ratio"] = form_data[
            "dish_prepare_tips_ratio"]
        employee_data[form_data["employee_number"]]["dish_runner_tips_ratio"] = form_data["dish_runner_tips_ratio"]
        employee_data[form_data["employee_number"]]["appetizer_tips_ratio"] = form_data["appetizer_tips_ratio"]
        employee_data[form_data["employee_number"]]["cleaner_tips_ratio"] = form_data["cleaner_tips_ratio"]
        employee_data[form_data["employee_number"]]["host_tips_ratios"] = form_data["host_tips_ratios"]
        employee_data[form_data["employee_number"]]["noodle_dance_tips_ratios"] = form_data[
            "noodle_dance_tips_ratios"]
        employee_data[form_data["employee_number"]]["dish_prepare_work_count_ratio"] = form_data[
            "dish_prepare_work_count_ratio"]
        employee_data[form_data["employee_number"]]["dish_runner_work_count_ratio"] = form_data[
            "dish_runner_work_count_ratio"]
        employee_data[form_data["employee_number"]]["appetizer_work_count_ratio"] = form_data[
            "appetizer_work_count_ratio"]
        employee_data[form_data["employee_number"]]["main_department"] = form_data[
            "main_department"]
        if form_data["can_work_days_in_a_week"] != "":
            employee_data[form_data["employee_number"]]["can_work_days_in_a_week"] = form_data[
                "can_work_days_in_a_week"]
        else:
            employee_data[form_data["employee_number"]]["can_work_days_in_a_week"] = 0
        employee_data[form_data["employee_number"]]["available_working_time"] = {}

        for item in form_data:
            if 'can_work' in item:
                employee_data[form_data["employee_number"]]["available_working_time"][item] = form_data[item]

        if form_data.get("change_employee"):
            if form_data["employee_number"] != form_data["change_employee"]:
                employee_data.pop(form_data["change_employee"])

        data_handler.save_employee_data_as_json(json.dumps(employee_data))
        return redirect("/manage/employee_data_view_and_edit")
    elif request.method == "GET":
        change_employee = request.args["change_employee"]
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if change_employee == "add_new_employee":
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(),
                                           date=data_handler.get_server_date(),
                                           employee_data=data_handler.get_employee_data())
                else:
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=get_daily_data(),
                                           date=data_handler.get_server_date(),
                                           change_employee=change_employee,
                                           employee_data=data_handler.get_employee_data())
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/employee_data_view_and_edit/get_employee_data_csv", methods=['POST'])
def get_employee_data_csv():
    if request.method == "POST":
        output_file_path = data_handler.export_employee_data_as_csv()
        return send_file(output_file_path)


@manage_section.route("/manage/employee_data_view_and_edit/delete_employee", methods=['POST'])
def employee_data_view_and_edit_edit_employee_delete_employee():
    if auth_verify(session["user"], session["password"]):
        delte_employee = request.form['delete_employee']
        print(delte_employee)
        employee_data = data_handler.get_employee_data()
        employee_data.pop(delte_employee)
        data_handler.save_employee_data_as_json(json.dumps(employee_data))
        return redirect("/manage/employee_data_view_and_edit")
    else:
        session.clear()
        return render_template("login.html", error="login information changed")


@manage_section.route("/manage/view_secret_letters", methods=['GET'])
def view_secret_letters():
    tempate_path = "manage/view_secret_letter.html"
    if session.get("user"):
        if auth_verify(session["user"], session["password"]):
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(),
                                   date=data_handler.get_server_date(),
                                   secret_letter_data=data_handler.get_letters_data())
        else:
            session.clear()
            return render_template("login.html", error="login information changed")
    else:
        return render_template("login.html")


@manage_section.route("/manage/delete_secret_letters", methods=['POST'])
def delete_secret_letters():
    letter_to_delete = request.form.get("delete_letter")
    letter_data = data_handler.get_letters_data()
    letter_data.pop(letter_to_delete)
    data_handler.save_letters_data_as_json(json.dumps(letter_data))
    return redirect("/manage/view_secret_letters")


@manage_section.route("/manage/view_data", methods=['GET'])
def view_data():
    tempate_path = "manage/view_data.html"
    if request.method == "GET":
        data = request.args.to_dict()
        if data:
            output_data = data_handler.get_view_data(data["data_type"], data["start_date"], data["end_date"])
            data_range = output_data[0]
            counted_dates = output_data[1]
            return render_template(tempate_path,
                                   data_range=data_range,
                                   all_employee_info=get_employee_data(),
                                   counted_dates=counted_dates,
                                   data=data)
        else:
            return render_template(tempate_path)


@manage_section.route("/manage/view_data/download_report_as_csv", methods=['POST'])
def view_data_download_csv():
    if request.method == "POST":
        data = eval(request.form.get("data"))
        output_file_path = data_handler.view_data_to_csv(data)
        return send_file(output_file_path)


@manage_section.route("/manage/manage_take_out_data", methods=['GET', 'POST'])
def manage_take_out_data():
    tempate_path = "manage/manage_take_out.html"
    route_path = "/manage/manage_take_out_data"
    department_json_data_name = "take_out_data"
    if request.method == "POST":
        form_data = request.form.to_dict()
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        if form_data.get("delete_group"):
            daily_data = get_daily_data(date=current_view_and_edit_date)
            daily_data[department_json_data_name].pop(form_data["delete_group"])
            save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=data_handler.get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date,
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path,
                                   str=str)
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("view_and_edit_date") and request.args["view_and_edit_date"] is not None:
                    view_date = str(request.args["view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                return render_template(tempate_path,
                                       userinfo=get_current_employee_data(session['user']),
                                       all_employee_info=get_employee_data(),
                                       daily_data=daily_data,
                                       date=view_date,
                                       department_json_data_name=department_json_data_name,
                                       post_url=route_path,
                                       str=str)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/manage_take_out_data/add_group", methods=['GET', 'POST'])
def manage_take_out_data_add_group():
    route_path = "/manage/manage_take_out_data/add_group"
    tempate_path = "manage/manage_take_out_add_group.html"
    department_json_data_name = "take_out_data"
    if request.method == "POST":
        server_group_data = request.form.to_dict()
        current_view_and_edit_date = request.form.get("current_view_and_edit_date")
        if current_view_and_edit_date is None:
            current_view_and_edit_date = data_handler.get_server_date()
        team_members_not_empty = False
        try:
            for item in server_group_data:
                if "team_member" in item and "work_hour" not in item:
                    if server_group_data[item] != "":
                        if server_group_data[item + "_work_hour"] == "":
                            server_group_data[item + "_work_hour"] = "8"
                        int(server_group_data[item].split(" ")[0])
                        team_members_not_empty = True
            if team_members_not_empty is False:
                raise Exception("no team member")
        except Exception as e:
            print(e.args[0])
            return render_template(tempate_path,
                                   userinfo=get_current_employee_data(session['user']),
                                   all_employee_info=get_employee_data(),
                                   daily_data=get_daily_data(date=current_view_and_edit_date),
                                   date=current_view_and_edit_date, error="error",
                                   department_json_data_name=department_json_data_name,
                                   post_url=route_path)
        daily_data = get_daily_data(date=current_view_and_edit_date)
        if not daily_data.get(department_json_data_name):
            daily_data[department_json_data_name] = {}
        daily_data[department_json_data_name][server_group_data["shift"]] = server_group_data
        save_daily_data_as_json(json.dumps(daily_data), date=current_view_and_edit_date)
        return render_template("manage/manage_take_out.html",
                               userinfo=get_current_employee_data(session['user']),
                               all_employee_info=get_employee_data(),
                               daily_data=data_handler.get_daily_data(date=current_view_and_edit_date),
                               date=current_view_and_edit_date,
                               department_json_data_name=department_json_data_name,
                               post_url="/manage/manage_take_out_data",
                               str=str,
                               success_info="submit_success")
    elif request.method == "GET":
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                if request.args.get("current_view_and_edit_date") and request.args["current_view_and_edit_date"] is not None:
                    view_date = str(request.args["current_view_and_edit_date"]).replace("-", "")
                else:
                    view_date = data_handler.get_server_date()
                daily_data = get_daily_data(view_date)
                if request.args.get("edit_group") is not None:
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=daily_data,
                                           date=view_date,
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path,
                                           edit_group=request.args.get("edit_group"),
                                           str=str)
                else:
                    return render_template(tempate_path,
                                           userinfo=get_current_employee_data(session['user']),
                                           all_employee_info=get_employee_data(),
                                           daily_data=daily_data,
                                           date=view_date,
                                           department_json_data_name=department_json_data_name,
                                           post_url=route_path,
                                           edit_group="None",
                                           str=str)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")


@manage_section.route("/manage/edit_and_view_wasted_food_data", methods=['GET'])
def edit_and_view_wasted_food_data():
    template_path = "manage/edit_and_view_wasted_food_data.html"
    # 验证用户咨询
    if not session.get("user"):
        return render_template("login.html")
    if not auth_verify(session["user"], session["password"]):
        session.clear()
        return render_template("login.html", error="login information changed")

    # return web
    if request.method == "GET":
        data = request.args.to_dict()
        if data:
            output_data = data_handler.get_view_data(data["data_type"], data["start_date"], data["end_date"])
            data_range = output_data[0]
            counted_dates = output_data[1]
            return render_template(template_path,
                                   data_range=data_range,
                                   wasted_food_data=data_handler.get_waste_food_category(),
                                   counted_dates=counted_dates,
                                   data=data)
        else:
            return render_template(template_path,
                                   wasted_food_data=data_handler.get_waste_food_category())


@manage_section.route("/manage/edit_and_view_wasted_food_data/change_food_category", methods=['POST'])
def edit_and_view_wasted_food_data_change_food_category():
    # 验证用户咨询
    if not session.get("user"):
        return render_template("login.html")
    if not auth_verify(session["user"], session["password"]):
        session.clear()
        return render_template("login.html", error="login information changed")

    # return web
    if request.method == "POST":
        data = request.form.to_dict()
        foods_data = None
        change_name = None
        method = None
        change_type = None
        name_before_change = None
        if data.get("change_name"):
            change_name = data["change_name"]
        if data.get("method"):
            method = data["method"]
        if data.get("change_type"):
            change_type = data["change_type"]
        if data.get("name_before_change"):
            name_before_change = data["name_before_change"]
        try:
            if data["method"] == "add":
                foods_data = {"main_categories": data["food_main_categories"],
                              "secondary_categories": data["food_secondary_categories"]}
        except:
            pass
        data_handler.change_waste_food_category(method=method,
                                                change_type=change_type,
                                                change_name=change_name,
                                                foods_data=foods_data,
                                                name_before_change=name_before_change)
        return redirect("/manage/edit_and_view_wasted_food_data")


@manage_section.route("/manage/daily_report_wasted_food_data", methods=['Get', 'POST'])
def daily_report_wasted_food_data():
    template_path = "manage/daily_report_wasted_food_data.html"
    # 验证用户咨询
    if not session.get("user"):
        return render_template("login.html")
    if not auth_verify(session["user"], session["password"]):
        session.clear()
        return render_template("login.html", error="login information changed")

    # return web
    if request.method == "GET":
        daily_data = data_handler.get_daily_data()
        return render_template(template_path,
                               wasted_food_data=data_handler.get_waste_food_category(),
                               daily_data=daily_data)
    elif request.method == "POST":
        data = request.form.to_dict()
        print(data)
        daily_data = get_daily_data()
        if not daily_data.get("wasted_food_data"):
            daily_data["wasted_food_data"] = {}
        daily_data["wasted_food_data"] = data
        data_handler.save_daily_data_as_json(json.dumps(daily_data))
        return render_template(template_path,
                               wasted_food_data=data_handler.get_waste_food_category(),
                               daily_data=daily_data,
                               success_info="submit_success")


@manage_section.route("/manage/edit_and_view_wasted_food_data/download_report_as_csv", methods=['POST'])
def view_wasted_food_data_download_csv():
    if request.method == "POST":
        data = eval(request.form.get("data"))
        output_file_path = data_handler.view_data_to_csv(data, data_target="wasted_food")
        return send_file(output_file_path)
