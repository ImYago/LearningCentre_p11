from colorama import Fore
import filer


class LearningCentre:
    def __init__(self):
        self.current_user = 0
        self.current_grade = ''

    def register(self):
        name = input(Fore.LIGHTGREEN_EX + 'Enter name: ')
        username = input(Fore.LIGHTGREEN_EX + 'Enter username: ')
        phone = input(Fore.LIGHTGREEN_EX + 'Enter phone: ')
        password = input(Fore.LIGHTGREEN_EX + 'Enter password: ')
        is_student = input(Fore.LIGHTGREEN_EX + 'Are you student !? [y/N]: ')

        while filer.checkusername(username):
            username = input(Fore.LIGHTYELLOW_EX + 'this username has been occupied \n'
                                                   'Enter another username {0} for exit: ')
            if username == '0':
                return False
        if username.strip() == "" or password.strip() == "" or name.strip() == "" or username == '0':
            print(Fore.LIGHTYELLOW_EX + 'invalid username or password!')
            return False
        else:
            if is_student.lower() in ['y', 'yes', 'yeah', 'yep', '1', 'sure', 's', 'student']:
                is_student = True
            elif is_student.lower() in ['n', 'no', 'nope', 'nah', '2', 'm', 'mentor']:
                is_student = False
            filer.add_user(name, username, phone, password, is_student)
            self.current_user = filer.get_id(username)
            self.current_grade = filer.get_grade(filer.get_grade(username))
            print(Fore.LIGHTBLUE_EX + "Success!")
            return True

    def login(self):
        username = input(Fore.GREEN + 'Enter username: ')
        password = input(Fore.GREEN + 'Enter password: ')

        while not filer.check(username, password) and username != 0:  # block username: 0
            print(Fore.RED + 'Username not found or password incorrect! try again or {0} for exit')
            username = input(Fore.YELLOW + 'Enter username: ')
            if username == '0':
                return False
            password = input(Fore.YELLOW + 'Enter password: ')
        if filer.check(username, password):
            print(Fore.GREEN + 'success!')
            self.current_user = filer.get_id(username)
            self.current_grade = filer.get_grade(filer.get_id(username))
            return True

    def enterance(self):
        filer.file_create()
        et = '''
        1. Login
        2. Register
        3. exit
        $ '''
        s = input(Fore.LIGHTCYAN_EX + et)
        if s == '1':
            if self.login():
                if not self.main_page():
                    self.enterance()
            else:
                self.enterance()
        elif s == '2':
            if self.register():
                if not self.main_page():
                    self.enterance()
            else:
                self.enterance()
        elif s == '3':
            print(Fore.LIGHTGREEN_EX + 'see you soon ')
            exit()
        else:
            print(Fore.LIGHTYELLOW_EX + 'selection not found!')
            self.enterance()

    def main_page(self):
        if self.current_grade == 'student':
            st = '''
        STUDENT

        1. kursga qoshilish
        2. kursdan chiqish
        3. kusrlarni korish
        4. exit
        $ '''
            s = input(Fore.LIGHTCYAN_EX + st)
            if s.isdigit():
                if s == "1":
                    filer.print_courses()
                    filer.join_course(self.current_user)
                    self.main_page()
                elif s == "2":
                    filer.get_courses(self.current_user)
                    s = int(input(Fore.LIGHTCYAN_EX + 'select course id: '))
                    filer.exit_course(self.current_user, s)
                    self.main_page()
                elif s == "3":
                    filer.print_courses()
                    self.main_page()
                elif s == "4":
                    return False

        elif self.current_grade == 'mentor':
            st = '''
            MENTOR

            1. kurs qoshish
            2. kursni olib tashash
            3. ozi qoshgan kurslarni korish
            4. exit
            $ '''
            s = input(Fore.LIGHTMAGENTA_EX + st)

            if s.isdigit():
                if s == "1":
                    filer.add_course(self.current_user)
                    self.main_page()
                elif s == "2":
                    filer.del_course()
                    self.main_page()
                elif s == "3":
                    filer.get_courses(self.current_user)
                    self.main_page()
                elif s == "4":
                    return False
        else:
            return False


a = LearningCentre()
a.enterance()
