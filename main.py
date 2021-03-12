from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.scrollview import ScrollView
import json, glob
from datetime import datetime
from pathlib import Path
import random

Builder.load_file('design.kv')

#classes need to have same nane -- Same string--- as design.kv file
class LoginScreen(Screen):
    """
    Login screen for application. If new user, will redirect to signup
    screen. If current user, will check for user name and password match
    """

    def sign_up(self):
        self.manager.current="sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password']==pword:
            self.manager.current= 'login_screen_success'
        else:
            self.ids.login_wrong.text = "Wrong username or password!"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    """
    Renders screen for signup. Will input signup information into
    json file, which is used to verify login information. If email is in use, not valid
    or the password does not match the user name, sign up screen success
    will not load.
    """

    def add_user(self, uname,pword):
        with open("users.json") as file:
            users=json.load(file)

        users[uname] = {'username': uname, 'password': pword,
        'created': datetime.now().strftime("%Y--%m-%d  %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_screen_success"

class SignUpScreenSuccess(Screen):
        """
        Redirects user to login screen after successful signup
        """

        def back_to_login(self):
            self.manager.transition.direction ="right"
            self.manager.current="login_screen"

class LoginScreenSuccess(Screen):
        """
        Once logged in, home page will load for application. Screen will feature logout button,
        button to retrieve quote and display on application.
        """
        def log_out(self):
            self.manager.transition.direction ="right"
            self.manager.current = "login_screen"

        def get_quote(self, feel):
            feel = feel.lower()

            available_feelings = glob.glob("quotes/*txt")

            available_feelings = [Path(filename).stem for filename in
            available_feelings]

            if feel in available_feelings:
                with open(f"quotes/{feel}.txt", 'r', encoding="utf8", errors='ignore') as f:
                    lines = f.readlines()

                self.ids.quote.text = random.choice(lines)
            else:
                self.ids.quote.text ="Choose another feelings"

class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
