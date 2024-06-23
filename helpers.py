app_screen="""
#:import MDActionBottomAppBarButton kivymd.uix.appbar.MDActionBottomAppBarButton
#:import MDFabBottomAppBarButton kivymd.uix.appbar.MDFabBottomAppBarButton
ScreenManager:
    HomeScreen:
    AddTopicScreen:
    ChatScreen:
    GenImageScreen:
    UpdateScreen:

<HomeScreen>:
    id: home
    name: "home"
    md_bg_color: app.theme_cls.backgroundColor
    MDTopAppBar:
        id: home_top_bar
        size_hint: 1,0.1
        type: "small"
        pos_hint: {"top":1}
        
        MDTopAppBarTitle:
            text: "Topics"
            role: "medium"
            font_size: "14sp"
        
        MDTopAppBarTrailingButtonContainer:
            MDActionTopAppBarButton:
                icon: "cancel"
            MDActionTopAppBarButton:
                icon : "dots-vertical"
    
    MDBoxLayout:
        adaptive_height: False
        # md_bg_color: [1,1,1,1]
        size_hint: 1,0.8
        pos_hint: {"center_y": 0.5}
        MDScrollView:
            id: scroll_view_home
            MDList:
                id: home_list
                spacing: "15dp"
                padding: "10dp"
                
    MDBoxLayout:
        size_hint: 1,0.1
        MDBottomAppBar:
            scroll_cls: scroll_view_home
            allow_hidden: True
            valign: "bottom"
            action_items:
                [
                MDActionBottomAppBarButton(icon="image-auto-adjust"),
                MDActionBottomAppBarButton(icon="face-woman-shimmer"),
                MDActionBottomAppBarButton(icon="image")
                
                ]
            
            MDFabBottomAppBarButton:
                icon: "plus"
                on_release: home.to_add_topic()
                 
                    
<AddTopicScreen>:
    id: topic
    name: 'topic'
    md_bg_color: app.theme_cls.backgroundColor
    MDTopAppBar:
        id: topic_top_bar
        size_hint: 1,0.1
        type: "small"
        pos_hint: {"top":1}
        
        MDTopAppBarLeadingButtonContainer:
            MDActionTopAppBarButton:
                icon: "less-than"
                on_release: topic.to_home()
    MDGridLayout:
        padding: "20sp"
        size_hint: 1,0.9
        cols: 1
        # md_bg_color: [1,1,1,1]
        spacing: "40dp"
                
        MDTextField:
            id: topic_field
            pos_hint: {"center_x":0.5}
            size_hint_x: 0.8
            mode: "filled"
            MDTextFieldMaxLengthText:
                max_text_length: 50
            MDTextFieldHelperText:
                text: "Leave blank for casual chat. Unchangeable."
                font_style: "Label"
                role:"small"
            MDTextFieldHintText:
                text: "Topic of this chat."
                role: "small"
                font_style: "Label"      
          
        MDTextField:
            id: name_field
            pos_hint: {"center_x":0.5}
            size_hint_x: 0.8
            required: True
            MDTextFieldMaxLengthText:
                max_text_length: 20
            MDTextFieldHelperText:
                text: "You CANNOT change it later."
                font_style: "Label"
                role:"small"
            MDTextFieldHintText:
                text: "Nickname in this chat."
                role: "medium"
                font_style: "Label"
        
        MDTextField:
            id: desc_field
            pos_hint: {"center_x":0.5}
            size_hint: 0.8,None
            max_height: "200dp"
            multiline: True
            MDTextFieldMaxLengthText:
                max_text_length: 200
            MDTextFieldHelperText:
                text: "Likes, hates, gender, occupation, etc."
                font_style: "Label"
                role:"small"
            MDTextFieldHintText:
                text: "Your characteristic description."
                role: "medium"
                font_style: "Label"
    MDExtendedFabButton:
        pos_hint: {"center_x":0.5,"center_y":0.1}
        size_hint: 0.5,None
        on_release: topic.to_chat(topic_field.text, name_field.text, desc_field.text)
        MDExtendedFabButtonText:
            text: "Start Conversation"
    
<ChatScreen>:
    id: chat
    name: 'chat'
    md_bg_color: app.theme_cls.backgroundColor
    MDTopAppBar:
        id: chat_top_bar
        size_hint: 1,0.1
        type: "small"
        pos_hint: {"top":1}
        
        MDTopAppBarLeadingButtonContainer:
            MDActionTopAppBarButton:
                icon: "less-than"
                on_release: chat.to_home()
        
        MDTopAppBarTitle:
            id: top_bar_title
            text: ""
            role: "medium"
            font_size: "14sp"
        
        MDTopAppBarTrailingButtonContainer:
            MDActionTopAppBarButton:
                icon: "cancel"
            MDActionTopAppBarButton:
                icon : "dots-vertical"
    
    MDScrollView:
        size_hint: 1,0.75
        pos_hint: {"top":0.9}
        do_scroll_x: False
        MDList:
            id: chat_box
            spacing: "20dp"
            padding: "10dp"
    
    MDTextField:
        id: text_field
        mode: "outlined"
        size_hint: 0.6,None
        height:"20dp"
        width: "200dp"
        font_size: 18
        spacing: "10dp"
        max_height: "150dp"
        pos_hint: {"center_y":0.08, "center_x": 0.35}
        radius: "30dp"


    MDIconButton:
        icon: "attachment"
        pos_hint: {"center_y" : 0.08, "center_x":0.75}
    MDIconButton:
        icon: "send"
        pos_hint: {"center_y" : 0.08, "center_x":0.9}
        on_release: chat.send_text(text_field.text)
    
<GenImageScreen>:
    name: 'gen_image'
    md_bg_color: app.theme_cls.backgroundColor

<UpdateScreen>:
    name: 'update_settings'
    md_bg_color: app.theme_cls.backgroundColor
    
<ChatBubble>:
    id: chat_bubble
    md_bg_color: [0,0,0,0]
    size_hint_y: None
    height: 60
    width: root.width
    padding: [10,0,10,0]
    orientation: 'vertical'
    adaptive_height: True
    # adaptive_size: True
    
    MDBoxLayout:
        height: msg_content.height +10
        width: msg_content.width + 10
        size_hint: None, None
        pos_hint: {'right':1} if chat_bubble._is_user == True else {'left':1}
        radius: [10,10,-5,10] if chat_bubble._is_user == True else [10,10,10,-5]
        md_bg_color: [85/255, 110/255, 83/255,1] if chat_bubble._is_user == True else [21/255, 42/255, 56/255,1]
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: None, None
            height: msg_content.height + 10
            width: msg_content.width
            
            MDLabel:
                id: msg_content
                text: chat_bubble.msg
                width: 48 if self.texture_size[0] < 48 else self.texture_size[0]
                height: self.texture_size[1]
                size_hint_y: None
                # role: 'small'
                font_style: 'Label'
                text_size: chat_bubble.width*0.8 if self.width >= chat_bubble.width*0.8 else None, None
                halign: 'left'
                color: app.theme_cls.secondaryColor
                padding: "10sp"

<Spacer@Widget>:
    id: wid
    width: 5
    size_hint: None, None
                
"""

temp="""
        MDTopAppBarLeadingButtonContainer:
            MDActionTopAppBarButton:
                icon: "account"
"""