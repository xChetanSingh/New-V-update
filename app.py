import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import requests


#Configssss -- Edit Alll
API_ID = 6459362
API_HASH = 'd7877fa235f24635921e287aaa800507'
BOT_TOKEN = '5618692983:AAEs3d0f_W-MbrOzsLpVjvaN4j0Rki3dMBk'
TDMB_API = "b93049a713559ad90b95537da68308fe"
web_domain = "https://www.xdubteam.in/"
howtodownload = "https://youtu.be/-_WfkuVyJL4"
channelurl = "https://t.me/toonmix_india"


# Random Texts :

rulesss = ''' ⁣<b>How To Use Me 📣</b> 

Jab bhi aap bot se search 🔎 karwaaye toh first of all aapko yaad rakhna hai "Series name" + Season + (Number) agar koi movie hai toh movie name only 

Example: Dr. stone Season 3

Movie name example: Doraemon Stand By Me 2

⁣<b>English</b>: Whenever U want to Search With Text Here. So You Need To Know First OF All "Series name" + Season + (Number) If U Want To Seach a Movie Then There Will be Need Just a Movie Name

Example: Dr. stone Season 3

Movie name example: Doraemon Stand By Me 2'''

app = pyrogram.Client("myboost", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(pyrogram.filters.text)
def handle_new_message(client , message):
    search_query = message.text
    if "/start" in search_query :
        message.reply(rulesss)
    if len(search_query) < 150 :
        user = message.from_user.id
        posts = fetch_wordpress_posts(search_query)
        start = 0
        end = 5
        data = f'''<b>Results for : {message.text} </b> \nRequested By : “<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>”
        \nUse 𝘽𝙍𝘼𝙑𝙀 𝘽𝙍𝙊𝙒𝙎𝙀𝙍 🌐 App for Blocking Annoyings Ads!'''
        reply,m = show_results(posts, start, end ,data)
        if reply == 0 :
            pass
        elif m == 0 :
            pass
        else :
            m2 = get_keyboard(posts, start, end,user)
            mak = InlineKeyboardMarkup(m+m2)
            message.reply(reply, reply_markup=mak)
@app.on_callback_query()
def handle_callback_query(client ,callback_query):
    _ = callback_query.data.split("||")
    data = _[0]
    if _[1] != str(callback_query.from_user.id):
        callback_query.answer(
            "😁 User Beta Masti Nhi...
            Please Create Your Own Requests",
            show_alert=True
        )
        return
    if data == "del" :
        callback_query.message.delete()
    else :
        start, end = map(int, data.split(','))
        xx = callback_query.message.reply_to_message.text
        xx2 = callback_query.message.text
        posts = fetch_wordpress_posts(xx)
        reply,m = show_results(posts, start, end ,xx2)
        m2 = get_keyboard(posts, start, end, _[1])
        mak = InlineKeyboardMarkup(m+m2 )
        callback_query.message.edit(reply, reply_markup=mak)


def show_results(posts, start, end , sss):
    results = posts[start:end]
    if results == []:
        return 0 , 0
    else :
        reply = sss
        buttons = [[InlineKeyboardButton("How To Watch/Download❓",url=howtodownload)],[InlineKeyboardButton("📲 Join Channel",url=channelurl),InlineKeyboardButton("🌐 Visit Web",url=web_domain)]]
        for result in results:
            x = [InlineKeyboardButton(result['title'],url=result['url'])]
            buttons.append(x)
        return reply , buttons

def get_keyboard(posts, start, end , user):
    keyboard = []
    keyboard.append([InlineKeyboardButton(
            "⏮️ PREV.", callback_data=f"{start-5},{end-5}||{user}"),InlineKeyboardButton(
            " ❌ ", callback_data=f"del||{user}"
        ),InlineKeyboardButton(
            "NEXT ⏭️", callback_data=f"{start+5},{end+5}||{user}"
        )] )
    return keyboard

def fetch_wordpress_posts(search_query):
    response = requests.get(f"{web_domain}/wp-json/wp/v2/search?search={search_query}&per_page=100")
    if response.status_code == 200:
        return response.json()
    else:
        return []

def delete_message_after_timeout(message, timeout):
    time.sleep(timeout)
    message.delete()

app.run()
