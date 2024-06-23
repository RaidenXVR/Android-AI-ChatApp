import asynckivy
from kivy.graphics import Color
from kivy.graphics.svg import Svg
from kivy.lang import Builder
from kivy.properties import DictProperty, StringProperty, OptionProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivymd.material_resources import dp
from kivymd.theming import ThemableBehavior
from kivymd.uix import MDAdaptiveWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar, MDListItemLeadingIcon, MDListItemHeadlineText, \
    MDListItemSupportingText, MDListItemTertiaryText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField, MDTextFieldLeadingIcon
from helpers import app_screen
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle, RoundedRectangle

from functions import *


class ChatbotApp(MDApp):
    def build(self):
        screen = Builder.load_string(app_screen)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        return screen

    def toggle_nav(self):
        pass


class HomeScreen(Screen):

    def to_add_topic(self):
        self.manager.current = "topic"

    def to_chat(self, topic: str):
        self.manager.current = "chat"
        self.manager.current_screen.set_topic(topic)

    def add_topic_list(self, topic, name):
        self.ids.home_list.add_widget(HomeListItem(topic=topic, name=name))

    def set_last_message(self, topic, last_message):
        pass

    def get_topic_list(self):
        return self.ids.home_list.children


class AddTopicScreen(Screen):
    def to_chat(self, topic: str, nickname: str, desc: str):
        chat_screen: ChatScreen = [obj for obj in self.manager.screens if obj.name == "chat"][0]
        home_screen: HomeScreen = [obj for obj in self.manager.screens if obj.name == "home"][0]

        if topic == "" or topic is None or topic == "Casual":

            topic_list = [obj for obj in self.manager.screens if obj.name == "home"][0].get_topic_list()
            casual_list = [topic for topic in topic_list if topic.topic_[:6] == "Casual"]
            if len(casual_list) > 0:
                topic = "Casual" + str(len(casual_list))
            else:
                topic = "Casual"

        home_screen.add_topic_list(topic, nickname)
        chat_screen.set_topic(topic)
        self.manager.current = "chat"

    def to_home(self):
        self.manager.current = "home"


class ChatScreen(Screen):
    _topic: str = ""

    def send_text(self, text):
        async def _send_text(_text):
            if text == "" or text is None:
                return
            bubble = ChatBubble(text=_text)
            self.ids.chat_box.add_widget(bubble)
            loading = ChatBubbleLoading()
            self.ids.chat_box.add_widget(loading)
            response = await get_response(chat_str=_text)
            self.ids.chat_box.remove_widget(loading)
            bubble2 = ChatBubble(text=response, is_user=False)
            self.ids.chat_box.add_widget(bubble2)

        asynckivy.start(_send_text(text))


    def set_topic(self, topic: str):

        self._topic = topic

        if len(topic) >= 12:
            topic = topic[:8] + "..."
        self.ids.top_bar_title.text = topic

    def to_home(self):
        self.manager.current = "home"


class GenImageScreen(Screen):
    pass


class UpdateScreen(Screen):
    pass


class HomeListItem(MDListItem):
    topic_: str = ""

    def __init__(self, topic: str, name: str, image=None, last_text: str = None):
        super().__init__()
        self.topic_ = topic
        avatar = MDListItemLeadingAvatar(source=image) if image else MDListItemLeadingIcon(icon="account")
        title = MDListItemHeadlineText(text=topic)
        # title.padding = [0,"0dp",0,0]
        nickname = MDListItemSupportingText(text=name)
        last_text = MDListItemTertiaryText(text=last_text if last_text else "   ")

        self.add_widget(avatar)
        self.add_widget(title)
        self.add_widget(nickname)
        self.add_widget(last_text)
        self.bind(on_release=lambda x: self.to_chat(topic=topic))

    def to_chat(self, topic):
        self.parent.parent.parent.parent.to_chat(topic=topic)


class ChatBubble(MDBoxLayout):
    msg = StringProperty()
    time = StringProperty()
    _is_user = BooleanProperty()

    def __init__(self, text: str, is_user: bool = True):
        super().__init__()
        self._is_user = is_user
        self.msg = text

class ChatBubbleLoading(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.size_hint = [None,None]
        self.size = ["48dp", "48dp"]

        self.add_widget(MDCircularProgressIndicator(size=self.size,
                                                    size_hint=(None,None),
                                                    pos_hint={"center_x":0.5, "center_y":0.5}))

if __name__ == "__main__":
    # Window.size = (9 * 40, 16 * 40)
    Window.size = (320, 600)
    sm = ScreenManager()
    sm.add_widget(HomeScreen(name="home"))
    sm.add_widget(AddTopicScreen(name="topic"))
    sm.add_widget(ChatScreen(name="chat"))
    sm.add_widget(GenImageScreen(name="gen_image"))
    sm.add_widget(UpdateScreen(name="update_settings"))

    ChatbotApp().run()
