import os.path
import asynckivy
from PIL import Image as PImage
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image as KImage
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogContentContainer, MDDialogButtonContainer, MDDialogHeadlineText
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.fitimage import FitImage
from kivymd.uix.list import MDListItem, MDListItemLeadingAvatar, MDListItemLeadingIcon, MDListItemHeadlineText, \
    MDListItemSupportingText, MDListItemTertiaryText
from kivymd.uix.progressindicator import MDCircularProgressIndicator
from kivymd.uix.screen import Screen

from functions import *
from helpers import app_screen


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
            if response["type"] == "text":
                bubble2 = ChatBubble(text=response["message"], is_user=False)
                self.ids.chat_box.add_widget(bubble2)
            elif response["type"] == "image":
                img_bubble = ChatBubbleImage(image_data=response["image"], is_user=False)
                bubble2 = ChatBubble(text=response["message"], is_user=False)
                self.ids.chat_box.add_widget(img_bubble)
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

class Gallery(Screen):
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

    def __init__(self, text: str = "", is_user: bool = True):
        super().__init__()
        self._is_user = is_user
        self.msg = text


class ChatBubbleImage(MDBoxLayout):
    image_data = None
    ori_image = None
    _is_user = BooleanProperty(False)
    _path = ""

    def __init__(self, **kwargs):
        super().__init__()
        self.image_data = kwargs.pop('image_data')
        self._is_user = kwargs.pop('is_user')
        self.ori_image = self.image_data
        img = PImage.open(BytesIO(self.image_data))
        self.image_width, self.image_height = img.size

        if self.image_width > 0.8 * self.width:
            ratio = 0.8 * Window.size[0] / self.image_width

            self.image_width = ratio * self.image_width
            self.image_height = ratio * self.image_height

            resized = img.resize((int(self.image_width), int(self.image_height)), PImage.Resampling.LANCZOS)
            bio = BytesIO()
            resized.save(bio, format='PNG')
            self.image_data = bio.getvalue()

        self.md_bg_color = [0, 0, 0, 0]
        self.size_hint_y = None
        self.height = 60
        self.padding = [10, 0, 10, 0]
        self.orientation = 'vertical'
        self.adaptive_height = True

        cb_box = MDBoxLayout(size_hint=(None, None),
                             height=self.image_height + 10,
                             width=self.image_width + 10,
                             pos_hint={'right': 1} if self._is_user else {'left': 1},
                             radius=[10, 10, -5, 10] if self._is_user else [10, 10, 10, -5],
                             md_bg_color=[85 / 255, 110 / 255, 83 / 255, 1] if self._is_user else [21 / 255, 42 / 255,
                                                                                                   56 / 255, 1],
                             )
        lcon_box = MDBoxLayout(orientation='vertical',
                               size_hint=(None, None),
                               height=self.image_height + 10,
                               width=self.image_width + 10)

        label = ImageButton(texture=CoreImage(BytesIO(self.image_data), ext='png').texture)
        label.bind(on_press=lambda x: self.touched(x, ori_image=self.ori_image, ori_size=img.size))
        label.bind(on_long_press=self.long_pressed)

        cb_box.add_widget(lcon_box)
        lcon_box.add_widget(label)
        self.add_widget(cb_box)

    def touched(self, *args, **kwargs):
        print(args)
        butt = MDButton(MDButtonIcon(icon="close"))
        img_con = MDBoxLayout(size_hint=(None, None),
                              orientation='vertical',
                              width=self.parent.size[0] * 0.85,
                              height=self.parent.size[1])
        # ['scale-down', 'fill', 'contain', 'cover']
        img_con.add_widget(
            FitImage(texture=CoreImage(BytesIO(kwargs["ori_image"]), ext='png').texture, fit_mode="contain"))
        dia = MDDialog(MDDialogContentContainer(
            img_con
        ),
            MDDialogButtonContainer(butt))

        butt.bind(on_release=dia.dismiss)
        dia.open()

    def long_pressed(self, *args):
        save_button = MDButton(MDButtonText(text="Save"), style="text")
        save_button.bind(on_release=lambda x: self.save_image(x, image_bytes=self.ori_image, dialog=dia))
        cancel_button = MDButton(MDButtonText(text="Cancel"), style="text")
        dia = MDDialog(MDDialogHeadlineText(text="Save Image?"),
                       MDDialogButtonContainer(
                           Widget(),
                           cancel_button,
                           save_button,
                           spacing="8dp"
                       ))
        dia.open()

    def save_image(self, *args, **kwargs):
        image_bytes = kwargs.get("image_bytes")
        dia = kwargs.get("dialog")
        dia.dismiss()

        def close_file(*arguments):
            file_manager.close()
            return

        def select_path(path: str):
            file_manager.exit_manager()
            img.save(os.path.join(path, "test.png"))

        img = PImage.open(BytesIO(image_bytes))

        file_manager = MDFileManager(exit_manager=close_file, select_path=select_path)
        file_manager.show(os.path.expanduser("~"))
        print(self._path)


class ImageButton(ButtonBehavior, KImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_time = None
        self._is_long_press = False
        self.register_event_type('on_long_press')

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._is_long_press = False
            self._touch_time = Clock.schedule_once(self._do_long_press, 1)  # 1 second for long press
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self._touch_time is not None:
                self._touch_time.cancel()
                if not self._is_long_press:
                    self._do_short_press()
            return True
        return super().on_touch_up(touch)

    def _do_short_press(self):
        # Execute short press action
        self.dispatch('on_press')

    def _do_long_press(self, dt):
        # Execute long press action
        self._is_long_press = True
        self.dispatch('on_long_press')

    def on_press(self):
        pass

    def on_long_press(self):
        pass


class ChatBubbleLoading(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.size_hint = [None, None]
        self.size = ["48dp", "48dp"]

        self.add_widget(MDCircularProgressIndicator(size=self.size,
                                                    size_hint=(None, None),
                                                    pos_hint={"center_x": 0.5, "center_y": 0.5}))


if __name__ == "__main__":
    # Window.size = (9 * 40, 16 * 40)
    Window.size = (320, 600)
    sm = ScreenManager()
    sm.add_widget(HomeScreen(name="home"))
    sm.add_widget(AddTopicScreen(name="topic"))
    sm.add_widget(ChatScreen(name="chat"))
    sm.add_widget(GenImageScreen(name="gen_image"))
    sm.add_widget(Gallery(name='gallery'))
    sm.add_widget(UpdateScreen(name="update_settings"))
    ChatbotApp().run()
