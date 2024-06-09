import pyrogram
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import requests
import random
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from config import *

app = pyrogram.Client("myboost", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)



def check_hentai(text,threshold=50):
    matches = process.extract(text, trigger, scorer=fuzz.ratio)
    filtered_matches = [match for match in matches if match[1] >= threshold]
    if filtered_matches:
        print(filtered_matches)
        return True
    else:
        return False
    
def rand_emoji():
    reactions = [ "👍", "👎", "😂", "😍", "😢", "😮", "😡", "😆", "🎉", "❤️", "😜", "🤔", "👏", "💯", "🔥", "🙌", "😎", "🥳", "🤯", "🙈", "💔", "🤗", "🤩", "😷", "😴", "😋", "😒", "😏", "🙄", "😓", "😱", "😰", "😳", "😵", "🤤", "😈", "👻", "🤪", "🤨", "🤮", "😇", "🤬", "🥺", "🥵", "🥶", "😠", "💩", "👀", "🙏", "💪", "✨", "🎶", "🌟", "👋", "😝", "🤝", "✌️", "🤞", "👌" ]
    reaction = random.choice(reactions)
    return reaction

@app.on_message(pyrogram.filters.command("start"))
async def start_command(client, message):
    buttons = [
        [
            InlineKeyboardButton("ToonMixIndia", url=main),
            InlineKeyboardButton("HentaiXplay", url=henati_domain)
        ]
    ]
    
    await client.send_message(
        chat_id=message.chat.id,
        text=txt.Start,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(pyrogram.filters.command("help"))
async def help_command(client, message):
    await client.send_message(
            chat_id=message.chat.id,
            text=txt.Help
        )
    

@app.on_message(pyrogram.filters.command("rules"))
async def rules_command(client, message):
    await client.send_message(
            chat_id=message.chat.id,
            text=txt.Rules
        )
    
@app.on_message(pyrogram.filters.text)
async def handle_message(client, message):
    # React to user's message
    text = message.text
    user = message.from_user.id
    if check_hentai(text):
        q = text.replace("hentai","")
        search_results = requests.get("https://hai-back-5313083442a1.herokuapp.com/hanime/search?search="+q).json()
        if search_results:
            buttons = [[InlineKeyboardButton("Watch Hentai✨",url=hentai)],[InlineKeyboardButton("📲 Join Channel",url=channelurl),InlineKeyboardButton("🌐 Visit Web",url=main)]]
            for result in search_results:
                button = InlineKeyboardButton(result["title"], url=henati_domain+result["url"])
                buttons.append([button])
            buttons.append([InlineKeyboardButton(
            " ❌ ", callback_data=f"del||{user}"
        )])
            await message.reply_text(
                    text="Here are the search results ",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            await message.react(rand_emoji())
    else:
        search_results = requests.get("https://toonmixindia.in/apix5/findseries.php?api_key=HackerKi_Ma_ki_chut_bytmi&search="+text+"&per_page=100").json()
        if search_results:
            buttons =         buttons = [[InlineKeyboardButton("Watch Hentai✨",url=hentai)],[InlineKeyboardButton("📲 Join Channel",url=channelurl),InlineKeyboardButton("🌐 Visit Web",url=main)]]
            for result in search_results:
                button = InlineKeyboardButton(result["title"], url=result["url"])
                buttons.append([button])
            buttons.append([InlineKeyboardButton(
            " ❌ ", callback_data=f"del||{user}"
        )])
            await message.reply_text(
                    text="Here are the search results ",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            await message.react(rand_emoji())
    

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


if __name__ == "__main__":
    app.run()

