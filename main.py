from tkinter import *
import libfucntions as fucn

if __name__ == '__main__':
    root = Tk()
    root.title("Аутентификация")
    root.geometry("400x400")
    root.resizable(False, False)
    root.iconbitmap(default="favicon.ico")
    root.configure(bg="blue")

    # fucn.create_database()

    # Фреймы для авторизации и регистрации
    login_frame = Frame(root)
    registration_frame = Frame(root)

    # Отображение окна авторизации по умолчанию
    login_frame.pack()

    name = Label(login_frame, text="Авторизация", font=("Arial", 40), bg="red")

    loginName = Label(login_frame, text="Логин", font=("Arial", 14))
    loginInput = Entry(login_frame, font=("Arial", 14))

    passwordName = Label(login_frame, text="Пароль", font=("Arial", 14))
    passwordInput = Entry(login_frame, font=("Arial", 14), show="*")

    errorLabel = Label(login_frame, font=("Arial", 12))

    loginButton = Button(login_frame, text="Вход", font=("Arial", 14),
                         command=lambda: on_login_click(loginInput.get(), passwordInput.get()), bg="red")
    registrationButton = Button(login_frame, text="Зарегистрироваться", font=("Arial", 14),
                                command=lambda: show_registration_frame(), bg="red")

    help_button = Button(login_frame, text="Справка", font=("Arial", 14), command=lambda: show_help(), bg="red")
    about_button = Button(login_frame, text="О программе", font=("Arial", 14), command=lambda: show_about(), bg="red")

    name.pack()
    loginName.pack()
    loginInput.pack()
    passwordName.pack()
    passwordInput.pack()
    errorLabel.pack()
    loginButton.pack()
    registrationButton.pack()
    about_button.pack()
    help_button.pack()



    def show_help():
        help_window = Toplevel(root)
        help_window.title("Справка")
        help_window.geometry("400x200")

        help_label = Label(help_window, text="**Здесь будет описана справка к программе.**", font=("Arial", 14), wraplength=300)
        help_label.pack(padx=10, pady=10)

        close_button = Button(help_window, text="Закрыть", font=("Arial", 14), command=help_window.destroy)
        close_button.pack(pady=10)

        help_window.deiconify()

    def show_about():
        about_window = Toplevel(root)
        about_window.title("О программе")
        about_window.geometry("450x130")
        root.resizable(False, False)

        # Add program information here, e.g., using labels
        title_label = Label(about_window, text="Программа аутентификации", font=("Arial", 18))
        title_label.pack(pady=10)

        title_label = Label(about_window, text="Сделал: Карпов Максим", font=("Arial", 18))
        title_label.pack(pady=10)

        version_label = Label(about_window, text="Версия 1.0", font=("Arial", 12))
        version_label.pack()

        close_button = Button(about_window, text="Закрыть", font=("Arial", 14), command=about_window.destroy)
        close_button.pack(pady=10)


    # Фрейм регистрации
    name = Label(registration_frame, text="Регистрация", font=("Arial", 40))

    regName = Label(registration_frame, text="Логин", font=("Arial", 14))
    regInput = Entry(registration_frame, font=("Arial", 14))

    regPasswordName = Label(registration_frame, text="Пароль", font=("Arial", 14))
    regPasswordInput = Entry(registration_frame, font=("Arial", 14), show="*")
    regSecondPasswordName = Label(registration_frame, text="Повторите пароль", font=("Arial", 14))
    regSecondPasswordInput = Entry(registration_frame, font=("Arial", 14), show="*")

    regErrorLabel = Label(registration_frame, font=("Arial", 12), wraplength=200)

    registrationButton = Button(registration_frame, text="Зарегистрироваться", font=("Arial", 14),
                                command=lambda: on_registration_click(regInput.get(), regPasswordInput.get(),
                                                                      regSecondPasswordInput.get()))
    backButton = Button(registration_frame, text="Назад", font=("Arial", 14),
                        command=lambda: show_login_frame())

    name.pack()
    regName.pack()
    regInput.pack()
    regPasswordName.pack()
    regPasswordInput.pack()
    regSecondPasswordName.pack()
    regSecondPasswordInput.pack()
    regErrorLabel.pack()
    registrationButton.pack()
    backButton.pack()


    def show_registration_frame():
        login_frame.pack_forget()
        registration_frame.pack()


    def show_login_frame():
        registration_frame.pack_forget()
        login_frame.pack()


    ex = 1


    def on_login_click(username, password):
        global ex
        if fucn.is_blocked(username):
            errorLabel.config(text="Вход заблокирован.")

        if not fucn.is_user_exists(username):
            errorLabel.config(text="Пользователь не найден.")
            return

        if fucn.is_password_restrict(username):
            if not fucn.check_login_and_password(username, password):
                errorLabel.config(text="Неверный логин или пароль.")
                return

        if ex == 3:
            root.destroy()

        if not fucn.is_password_correct(username, password):
            errorLabel.config(text="Неверный пароль.")
            ex += 1
            return

        # Пользователь успешно авторизовался
        is_admin1 = fucn.is_admin(username)

        if not is_admin1:
            open_user_menu(username)
        else:
            open_admin_menu(username)


    def on_registration_click(username, password, secondPassword):
        if fucn.is_user_exists(username):
            regErrorLabel.config(text="Такой пользователь уже существует!")
            return

        if not fucn.check_login_and_password(username, password):
            regErrorLabel.config(text="Пароль должен содержать как минимум одну цифру и один арифметический знак.")
            return

        if password != secondPassword:
            regErrorLabel.config(text="Пароли не совпадают")
            return

        if not fucn.register_user(username, password):
            regErrorLabel.config(text="Регистрация не удалась")
            return
        regErrorLabel.config(text="Регистрация удалась! \n Пожалуйста, вернитесь на окно авторизации")


    def open_admin_menu(username):
        admin_window = Toplevel()
        admin_window.geometry("700x580")
        admin_window.title("Меню администратора")
        root.resizable(False, False)

        adminName = Label(admin_window, text="Админ панель", font=("Arial", 40))
        UserListName = Label(admin_window, text="Список пользователей", font=("Arial", 18))
        users_list = Listbox(admin_window, width=400)
        block_button = Button(admin_window, text="Заблокировать", command=lambda: block_user(users_list.get(ACTIVE)))
        unblock_button = Button(admin_window, text="Разблокировать",
                                command=lambda: unblock_user(users_list.get(ACTIVE)))
        restrictionButtonOn = Button(admin_window, text="Поставить ограничение пароля",
                                     command=lambda: restrictionOn_user(users_list.get(ACTIVE)))
        restrictionButtonOff = Button(admin_window, text="Снять ограничение пароля",
                                      command=lambda: restrictionOff_user(users_list.get(ACTIVE)))
        addUser = Label(admin_window, text="Добавить нового пользователя", font=("Arial", 18))
        addUserInput = Entry(admin_window, font=("Arial", 14))
        addUserButton = Button(admin_window, text="Добавить", command=lambda: add_new_user(addUserInput.get()))
        adminErrorLabel = Label(admin_window, font=("Arial", 12), wraplength=200)
        adminPasswordName = Label(admin_window, text="Пароль", font=("Arial", 14))
        adminPasswordInput = Entry(admin_window, font=("Arial", 14), show="*")
        adminSecondPasswordName = Label(admin_window, text="Повторите пароль", font=("Arial", 14))
        adminSecondPasswordInput = Entry(admin_window, font=("Arial", 14), show="*")

        def add_new_user(userNew):
            if fucn.is_user_exists(userNew):
                adminErrorLabel.config(text="Пользователь уже существует.")
                return
            adminErrorLabel.config(text="")
            fucn.add_new_user(userNew)
            show_users_list(users_list)

        def block_user(username):
            user = username.split()
            fucn.block_user(user)
            show_users_list(users_list)

        def unblock_user(username):
            user = username.split()
            fucn.unblock_user(user)
            show_users_list(users_list)

        def restrictionOn_user(username):
            user = username.split()
            fucn.restrictionOn_user(user)
            show_users_list(users_list)

        def restrictionOff_user(username):
            user = username.split()
            fucn.restrictionOff_user(user)
            show_users_list(users_list)

        adminName.pack()
        UserListName.pack()
        users_list.pack()
        block_button.pack()
        unblock_button.pack()
        restrictionButtonOn.pack()
        restrictionButtonOff.pack()
        addUser.pack()
        addUserInput.pack()
        addUserButton.pack()
        adminErrorLabel.pack()
        adminPasswordName.pack()
        adminPasswordInput.pack()
        adminSecondPasswordName.pack()
        adminSecondPasswordInput.pack()

        def show_users_list(users_list):
            users = fucn.get_users()

            # Очистка списка пользователей
            users_list.delete(0, END)

            # Добавление пользователей в список
            for user in users:
                username, block_user, restrict_password = user
                blocked_str = " (заблокирован)" if block_user else ""
                restrict_password_str = " (ограничения на пароли)" if restrict_password else ""
                users_list.insert(END, f"{username}{blocked_str}{restrict_password_str}")

        show_users_list(users_list)


    def open_user_menu(username):
        user_window = Toplevel()
        user_window.geometry("300x250")
        user_window.title("Окно пользователя")
        root.resizable(False, False)

        # Поля для ввода старого и нового пароля
        old_password_label = Label(user_window, text="Введите старый пароль:")
        old_password_entry = Entry(user_window, show="*")
        new_password_label = Label(user_window, text="Введите новый пароль:")
        new_password_entry = Entry(user_window, show="*")
        new_SecondPassword_label = Label(user_window, text="Подтвердите новый пароль:")
        new_SecondPassword_entry = Entry(user_window, show="*")
        userErrorLabel = Label(user_window, font=("Arial", 10), wraplength=200)

        # Кнопки "Сменить пароль"
        change_password_button = Button(user_window, text="Сменить пароль",
                                        command=lambda: on_change_password_click(username, old_password_entry.get(),
                                                                                 new_password_entry.get(),
                                                                                 new_SecondPassword_entry.get()))

        # Размещение элементов
        old_password_label.pack()
        old_password_entry.pack()
        new_password_label.pack()
        new_password_entry.pack()
        new_SecondPassword_label.pack()
        new_SecondPassword_entry.pack()
        userErrorLabel.pack()
        change_password_button.pack()

        def on_change_password_click(username, oldPassword, newPassword, newSecondPassword):
            if newPassword != newSecondPassword:
                userErrorLabel.config(text="Пароли не совпадают")
                return

            if not fucn.is_password_restrict(username):
                if not fucn.check_login_and_password(username, newPassword):
                    userErrorLabel.config(
                        text="Пароль должен содержать как минимум одну цифру и один арифметический знак.")
                    return

            if not fucn.is_password_correct(username, oldPassword):
                userErrorLabel.config(text="Неверный старый пароль.")
                return
            userErrorLabel.config(text="Пароль изменен")
            fucn.change_password(username, newPassword)

        user_window.mainloop()


    root.mainloop()
