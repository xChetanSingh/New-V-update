import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import requests
import re

#Configssss -- Edit Alll
API_ID = 7999622
API_HASH = '0c6b5e046ae4aff8987e95b93c9ce281'
BOT_TOKEN = '6731569216:AAEIctl1U-Xfn4rEeAPizyb255MEkEbAtGg'
TDMB_API = "b93049a713559ad90b95537da68308fe"
web_domain = "https://www.toonmixindia.in/"
hentai_domain = "https://hentaixplay.com/"
howtodownload = "https://www.toonmixindia.in/how-to-use-me/"
channelurl = "https://t.me/toonmix_india"
botusername = "yukichanptbot"

# Random Texts :

rulesss = ''' ⁣<b>How To Use Me 📣</b> 

Jab bhi aap bot se search 🔎 karwaaye toh first of all aapko yaad rakhna hai "Series name" + Season + (Number) agar koi movie hai toh movie name only 

Example: Dr. stone Season 3

Movie name example: Doraemon Stand By Me 2

⁣<b>English</b>: Whenever U want to Search With Text Here. So You Need To Know First OF All "Series name" + Season + (Number) If U Want To Seach a Movie Then There Will be Need Just a Movie Name

Example: Dr. stone Season 3

Movie name example: Doraemon Stand By Me 2'''

def has_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642" 
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return bool(emoji_pattern.search(text))

def has_common_greeting(text):
    greetings = ["hi","hlo" , "hello", "hey", "gm", "good morning", "good afternoon", "good evening", "ok", "okay", "hi there", "howdy", "greetings","/purge","/start","/settings","/","acha","accha","ok","okay","ji","bikul"]
    normalized_text = text.lower()
    for greeting in greetings:
        if greeting in normalized_text:
            return True
    return False


app = pyrogram.Client("myboost", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(pyrogram.filters.text)
async def handle_new_message(client , message):
    search_query = message.text
    if has_emoji(search_query) :
        pass
    elif has_common_greeting(search_query):
        pass
    else:
        if "/start" in search_query :
            await message.reply(rulesss)
        if len(search_query) < 150 :
            try:
                response = requests.get(f"https://stream.toonmix.site/checkfile.php?search={search_query}")
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = response.json()
                is_success = data.get("success", False)
                if is_success:
                    user = message.from_user.id
                    data = f'''<b>Results for : {message.text} </b> \nRequested By : “<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>” \nUse 𝘽𝙍𝘼𝙑𝙀 𝘽𝙍𝙊𝙒𝙎𝙀𝙍 🌐 App for Blocking Annoyings Ads!'''
                    buttons = [[InlineKeyboardButton("Watch Hentai✨",url=hentai_domain)],[InlineKeyboardButton("📲 Join Channel",url=channelurl),InlineKeyboardButton("🌐 Visit Web",url=web_domain)],[InlineKeyboardButton("🔍 View Search Results 👀", url="https://t.me/"+botusername+"/app?startapp="+search_query)],[InlineKeyboardButton("🔍 View Search Results 👀", url="https://t.me/"+botusername+"/app?startapp="+search_query)],[InlineKeyboardButton("🔍 View Search Results 👀", url="https://t.me/"+botusername+"/app?startapp="+search_query)]]
                    buttons.append([InlineKeyboardButton(
                        " ❌ ", callback_data=f"del||{user}"
                    )])
                    await message.reply(
                                text=data,
                                reply_markup=InlineKeyboardMarkup(buttons)
                            )
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                is_success = False
            except ValueError as e:
                print(f"Invalid JSON response: {e}")
                is_success = False

@app.on_callback_query()
async def handle_callback_query(client ,callback_query):
    _ = callback_query.data.split("||")
    data = _[0]
    if _[1] != str(callback_query.from_user.id):
        await callback_query.answer(
            "😁 User Beta Masti Nahi... \nPlease Create Your Own Requests",
            show_alert=True
        )
        return
    if data == "del":
        await callback_query.message.delete()


def delete_message_after_timeout(message, timeout):
    time.sleep(timeout)
    message.delete()

app.run()
