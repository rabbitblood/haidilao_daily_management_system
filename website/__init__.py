import json
import random
import os

from flask import Flask, render_template, url_for, session, request, redirect, send_file
from website import data_handler
from website.data_handler import get_letters_data, get_daily_data, get_translation_data, get_employee_data, \
    get_current_employee_data, save_letters_data_as_json, save_daily_data_as_json, is_float, auth_verify, get_server_date
from website import manage_section
from website import work_schedule_section


def init_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.secret_key = f'1'
    app.secret_key = f'1'

    app.register_blueprint(manage_section.manage_section)
    app.register_blueprint(work_schedule_section.work_schedule_section)

    @app.context_processor
    def load_translate_languages():
        return {"translate_data": get_translation_data()}

    @app.context_processor
    def load_str():
        return str()

    @app.context_processor
    def load_current_language():
        if session.get("language"):
            return {"language": session["language"]}
        else:
            session["language"] = "en"
            return {"language": "en"}

    @app.route("/language", methods=['GET', 'POST'])
    def language():
        if request.method == "POST":
            if session.get("language"):
                if session["language"] == "en":
                    session["language"] = "cn"
                else:
                    session["language"] = "en"
            else:
                session["language"] = "en"
            return redirect(request.referrer)
        else:
            if session.get("language"):
                return session["language"]
            else:
                session["language"] = "en"
                return "en"

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            user = request.form.get("user")
            password = request.form.get("password")
            employees = get_employee_data()
            for employee in employees:
                if employees[employee]['employee_number'] == user:
                    if employees[employee]['password'] == password:
                        session["user"] = user
                        session["password"] = password
                        session["legal_name"] = employees[employee]['legal_name']
                        return redirect("/my_account")
                    else:
                        return render_template("login.html", error="wrong username or password")
            return render_template("login.html", error="wrong username or password")
        elif request.method == "GET":
            return render_template("login.html")

    @app.route("/my_account")
    def my_account():
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                return render_template("my_account.html", userinfo=get_current_employee_data(session['user']))
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")

    @app.route("/work_schedule")
    def work_schedule():
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                return render_template("work_schedule.html",
                                       userinfo=get_current_employee_data(session['user']),
                                       employee_data=get_employee_data(),
                                       float=float)
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")

    @app.route("/manage")
    def manage():
        if session.get("user"):
            if auth_verify(session["user"], session["password"]):
                return render_template("manage.html", userinfo=get_current_employee_data(session['user']))
            else:
                session.clear()
                return render_template("login.html", error="login information changed")
        else:
            return render_template("login.html")

    @app.route("/secret_letters", methods=['GET', 'POST'])
    def secret_letters():
        route_path = "/secret_letters"
        tempate_path = "secret_letters.html"
        if request.method == "POST":
            form_data = request.form.to_dict()
            letter_data = get_letters_data()
            letter_data[str(letter_data["current_letter_count"])] = form_data
            letter_data["current_letter_count"] += 1
            save_letters_data_as_json(json.dumps(letter_data))
            return render_template(tempate_path,
                                   error=get_translation_data()["submit_success"][session["language"]],
                                   date=get_server_date(),
                                   post_url=route_path)
        elif request.method == "GET":
            return render_template(tempate_path,
                                   date=get_server_date(),
                                   post_url=route_path)

    @app.route("/logout")
    def logout():
        session.pop("user")
        session.pop("password")
        return render_template("edit_server_available_work_time.html")

    @app.route("/get_daily_data_from_server")
    def get_daily_data_from_server():
        return get_daily_data()

    @app.route("/get_employee_data_from_server")
    def get_get_employee_data_from_server_data_from_server():
        return get_employee_data()

    return app


app = init_app()


if __name__ == '__main__':
    app.run(host="", port=8894, debug=True)
