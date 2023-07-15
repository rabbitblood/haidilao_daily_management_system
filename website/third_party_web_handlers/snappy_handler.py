import json
import requests

S_TABLES = {6, 8, 10, 11, 12, 15, 16, 18, 19, 21, 22, 23, 25, 26, 28, 29, 20, 80, 69, 81, 68, 66, 65, 36, 32, 31, 30,
            35, 33, 38, 51, 50, 39, 55, 53, 52, 56, 58, 59, 61, 60, 622, 63, 85, 83, 82}


# since snappy monday is day 2, sunday is day 1, saturday is day 7, I wrote this method to help
def get_snappy_day(input_day):
    snappy_day = 0
    if input_day < 7:
        snappy_day = input_day + 1
    else:
        snappy_day = 1
    return snappy_day


def change_able_to_reservation_time(days: [], modify_time: [], modify_method: str):
    s = requests.Session()
    s.headers.update({"storeid": "4933"})
    username = "manager"
    password = "Qz059522778157"

    # login in to snappy account
    pos_res_info = s.post("https://gosnappy.io/v1/storestaff/login/4933", auth=(username, password))
    auth = pos_res_info.headers['Authorization']
    s.headers.update({"authorization": auth})

    # change each small table's time
    for table in S_TABLES:
        for day in days:
            day = get_snappy_day(day)
            table_num = table
            pos_res_info = s.get(f"https://gosnappy.io/v1/dt/store/reservation/slots/?day={day}&tableNo={table_num}")
            reservation_time_slots = list(json.loads(pos_res_info.content.decode('utf-8'))[0]['reservationTimeSlots'])

            if modify_method == "delete":
                for time in modify_time:
                    if time in reservation_time_slots:
                        reservation_time_slots.remove(time)
            elif modify_method == "add":
                for time in modify_time:
                    if time not in reservation_time_slots:
                        reservation_time_slots.append(time)

            payload = {
                "day": day,
                "date": None,
                "tableNo": f"{table_num}",
                "allowCpReservation": True,
                "reservationTimeInterval": 15,
                "reservationTimeSlots": reservation_time_slots
            }

            pos_res_info = s.post("https://gosnappy.io/v1/dt/store/reservation/slots/", json=payload)

    s.close()


if __name__ == "__main__":
    # this main is for manual set time and test
    change_able_to_reservation_time([5, 6], [17.5, 17.75, 18], "delete")
