from colorama import Fore



import json
import os
import bcrypt


def file_create():
    if (not os.path.exists('users.json')) or os.path.isdir('users.json'):
        with open('users.json', 'w') as s:
            s.write('[]')
    if (not os.path.exists('courses.json')) or os.path.isdir('courses.json'):
        with open('courses.json', 'w') as s:
            s.write('[]')


def check(username, password):
    password = password.encode()
    with open('users.json', 'r') as u:
        users = json.load(u)

    for i in users:
        hashed_password = i["password"].encode()
        if bcrypt.checkpw(password, hashed_password):
            return True
    return False


def checkusername(username):
    with open('users.json', 'r') as u:
        users = json.load(u)
    for i in users:
        if i["username"] == username:
            return True
    return False


def get_grade(a):
    with open('users.json', 'r') as u:
        users = json.load(u)

        for i in users:
            if i["id"] == a:
                return 'student' if i["is_student"] else 'mentor'


def get_id(a):
    with open('users.json', 'r') as u:
        users = json.load(u)

    for i in users:
        if i["username"] == a:
            return i["id"]


# encrypt
def encrypt(password):
    salt = bcrypt.gensalt()  # Generate a salt value
    hashed_password = bcrypt.hashpw(password.encode(), salt)  # Hash the password using bcrypt
    return hashed_password


def add_user(name, username, phone, password, is_student):
    with open('users.json', 'r') as u:
        users = json.load(u)

    password = encrypt(password)

    student = {
        "id": len(users) + 1,
        "username": username,
        "name": name,
        "phone": phone,
        "password": password.decode(),
        "courses": [],
        "is_student": is_student
    }

    users.append(student)

    with open('users.json', 'w') as nu:
        json.dump(users, nu, indent=2)


def add_to_history(id_, a):
    with open('users.json', 'r') as u:
        users = json.load(u)

    for i in users:
        if i["id"] == id_:
            i["courses"].append(a)

    with open('users.json', 'w') as nu:
        json.dump(users, nu, indent=2)


def check_course(cname):
    with open('courses.json', 'r') as c:
        courses = json.load(c)

    for i in courses:
        if i["name"].strip().lower() == cname.strip().lower():
            print(Fore.LIGHTYELLOW_EX + "This course exited!")
            print(Fore.LIGHTYELLOW_EX + f"id: {i['id']}. name: {i['name']} price: {i['price']}")
            return True
    return False


def add_course(mid_):
    with open('courses.json', 'r') as c:
        courses = json.load(c)

        name = input('Enter course name: ')
        price = input('Enter course price: ')

        id_ = len(courses) + 1

        course = {
            "id": id_,
            "name": name,
            "price": price,
            "students": []
        }

        h = [id_, name, price]
        if not check_course(name):
            add_to_history(mid_, h)

            courses.append(course)

            with open("courses.json", "w") as nc:
                json.dump(courses, nc, indent=2)
                print(Fore.LIGHTGREEN_EX + 'success!')


def join_course(sid):
    course_id = input(Fore.LIGHTCYAN_EX + 'Enter course id: ')
    with open("courses.json", "r") as c:
        courses = json.load(c)
    for i in courses:
        if i["id"] == course_id:
            add_to_history(sid, [i["id"], i["name"], i["price"]])


def exit_course(sid, cid):
    with open("users.json", "w") as u:
        users = json.load(u)
    for i in users:
        if i["id"] == sid:
            for c in i["courses"]:
                if c[0] == cid:
                    i["courses"].pop(c)


def print_courses():
    with open('courses.json', 'r') as c:
        courses = json.load(c)
    if len(courses) >= 1:
        for i in courses:
            print(Fore.LIGHTMAGENTA_EX + f'{i["id"]}. {i["name"]} {i["price"]}| peoples: {len(i["students"])} ')
    else:
        print(Fore.LIGHTGREEN_EX + 'courses not exist!\nwait for the mentors to add the course')


def get_courses(id_):
    with open('users.json', 'r') as u:
        users = json.load(u)

    for i in users:
        if i["id"] == id_:
            for b in i["courses"]:
                print(f"{b[0]} {b[1].title()}  price: {b[2]} ")

            return True
    return False


def del_course():
    with open('courses.json', 'r') as c:
        courses = json.load(c)

    for i in courses:
        print(Fore.RED + f'{i["id"]}. {i["name"]}')

    s = input('Enter course id: ')
    if s.isdigit():
        c = 0
        for course in courses:
            if course["id"] == s:
                courses.pop(c)

        with open("users.json", "r") as u:
            users = json.load(u)

            for user in users:
                v = 0
                for j in user["courses"]:
                    if j[0] == s:
                        user["courses"].pop(v)
                        v += 1
        with open("users.json", "w") as f:
            json.dump(users, f, indent=2)

        with open('courses.json', 'w') as nc:
            json.dump(courses, nc, indent=2)
            return True
    return False
