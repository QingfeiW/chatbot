#!/usr/bin/env python
# coding: utf-8

# In[1]:


# css = '''
# <style>
# .chat-message {
#     padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
# }
# .chat-message.user {
#     background-color: #ff4d4d
# }
# .chat-message.bot {
#     background-color: #475063
# }

# .chat-message .message {
#   color: #fff;
#   align-items: center;
#   justify-content: center;
# }
# '''

css='''
<style>

.chat-bubble {
    font-family: "Source Sans Pro", sans-serif, "Segoe UI", "Roboto", sans-serif;
    border: 1px solid transparent;
    padding: 5px 10px;
    margin: 2px 7px;
    max-width: 70%;
}

.chat-bubble.bot {
    background: #FFE4E1;
    border-radius: 10px;
    float: left;
}

.chat-bubble.user {
    background: #C0C0C0; 
    border-radius: 20px;
    float: right;
}

.chat-bubble .message {
   color: #000000;
   align-items: center;
   justify-content: center;
}

.chat-bubble .avatar {
  width: 20%;
}
'''

bot_template = '''
<div class="chat-bubble bot">
    <div class="avatar">
        <img src="https://png.pngtree.com/png-vector/20220611/ourmid/pngtree-chatbot-icon-chat-bot-robot-png-image_4841963.png" 
        style="max-height: 32px; max-width: 32px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-bubble user">
    <div class="avatar">
        <img src="https://static.vecteezy.com/system/resources/thumbnails/005/545/335/small/user-sign-icon-person-symbol-human-avatar-isolated-on-white-backogrund-vector.jpg"
        style="max-height: 35px; max-width: 35px; border-radius: 50%; object-fit: cover;">
    </div>   
    <div class="message">{{MSG}}</div>
</div>
'''
#style="max-height: 35px; max-width: 35px; border-radius: 50%; object-fit: cover;"

