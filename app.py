import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import requests


#Configssss -- Edit Alll
API_ID = 6459362
API_HASH = 'd7877fa235f24635921e287aaa800507'
BOT_TOKEN = '5618692983:AAFi_Mfg1Xv4_0Gp0HaJlNLtKbz1U0g8uO8'
TDMB_API = "b93049a713559ad90b95537da68308fe"
web_domain = "https://www.xdubteam.in/"
howtodownload = "https://youtu.be/jmRfdHcoSJY"
channelurl = "https://t.me/toonmix_india"


# Random Texts :

rulesss = ''' ⁣<b>How To Use Me 📣</b> 

Jab bhi aap bot se search 🔎 karwaaye toh first of all aapko yaad rakhna hai "Series name" + Season + (Number) agar koi movie hai toh movie name only 

Example: Dr. stone Season 3

Movie name example: Doraemon Stand By Me 2

⁣<b>English</b>: Whenever U want to Search With Text Here. So You Need To Know First OF All "Series name" + Season + (Number) If U Want To Seach a Movie Then There Will be Need Just a Movie Name

Example: Dr. stone Season 3

Movie name example: Doraemon Stand By Me 2'''



# Initialize the client
app = pyrogram.Client("myboost", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# Define a handler for the messages in the group
@app.on_message(pyrogram.filters.text)
def handle_new_message(client , message):
    # Get the search query from the message text
    search_query = message.text
    if "/start" in search_query :
        message.reply(rulesss)
        
    if len(search_query) < 150 :
        # print(message)
        # Fetch the WordPress posts for the given search query
        # This is just an example and you need to replace it with your own implementation
        # to fetch the WordPress posts based on the search query
        posts = fetch_wordpress_posts(search_query)

        
        # Show the first 5 results along with the buttons
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
            m2 = get_keyboard(posts, start, end)
            mak = InlineKeyboardMarkup(m+m2)
            # Send the results to the group
            # x = message.reply(reply,reply_markup=mak)
            # message.reply_photo(photo=image_url, caption=reply, reply_markup=mak)
            message.reply(reply, reply_markup=mak)


# Define a handler for callback queries
@app.on_callback_query()
def handle_callback_query(client ,callback_query):
    # Get the data from the callback query
    data = callback_query.data
    if data == "del" :
        callback_query.message.delete()
    else :
        start, end = map(int, data.split(','))
        # print(callback_query)
        # Show the results based on the action
        xx = callback_query.message.reply_to_message.text
        xx2 = callback_query.message.text
        posts = fetch_wordpress_posts(xx)
        reply,m = show_results(posts, start, end ,xx2)
        
        # Edit the original message with the new results
        # callback_query.message.edit(reply, reply_markup=get_keyboard(posts, start, end))
        m2 = get_keyboard(posts, start, end)
        mak = InlineKeyboardMarkup(m+m2 )
        callback_query.message.edit(reply, reply_markup=mak)


def show_results(posts, start, end , sss):
    results = posts[start:end]
    if results == []:
        return 0 , 0
    else :
        reply = sss
        buttons = [[InlineKeyboardButton("How To Watch/Download❓",url=howtodownload)],[InlineKeyboardButton("📲 Join Channel",url=channelurl),InlineKeyboardButton("🌐 Visit Web",url=web_domain)]]
        # print(posts)
        for result in results:
            x = [InlineKeyboardButton(result['title'],url=result['url'])]
            buttons.append(x)
        return reply , buttons

def get_keyboard(posts, start, end):
    keyboard = []
    keyboard.append([InlineKeyboardButton(
            "⏮️ PREV.", callback_data=f"{start-5},{end-5}"),InlineKeyboardButton(
            " ❌ ", callback_data=f"del"
        ),InlineKeyboardButton(
            "NEXT ⏭️", callback_data=f"{start+5},{end+5}"
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
     

# def tmdbinfo(q):
#     try :
#         response = requests.get(f"https://api.themoviedb.org/3/search/multi?api_key={TDMB_API}&query={q}")
#         data = response.json()
#         result = data["results"][1]
#         poster_path = result["poster_path"]

#         if poster_path :
#             poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
#             return poster_url
#         else :
#             poster_url = "https://i.ibb.co/rsmv4n1/photo-2022-02-18-16-38-12-2.jpg"
#             return poster_url
#     except :
#         return "https://i.ibb.co/rsmv4n1/photo-2022-02-18-16-38-12-2.jpg"
app.run()
