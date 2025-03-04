import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from telegraph import upload_file
from utils import get_file_id
@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph(bot, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("🙄 ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ᴜɴᴅᴇʀ 5 ᴍʙ")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await message.reply_text("ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ 😑")
        return
    msg = await message.reply_text(text="<code>ᴘʀᴏᴄᴇssɪɴɢ....</code>", disable_web_page_preview=True)   
    media = await message.reply_to_message.download()   
    await msg.edit_text("<code>ᴅᴏɴᴇ :)</code>", disable_web_page_preview=True) 
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await msg.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)  
        await asyncio.sleep(3)
        return await msg.delete()   
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return   
    await msg.delete()
    await message.reply_photo(
        photo=f'https://graph.org{response[0]}',
        caption=f"<b>ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴄᴏᴍᴘʟᴇᴛᴇᴅ 👇</b>\n\n<code>https://graph.org{response[0]}</code>\n\n<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ - @Codexownerr</b>",       
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="💀 ᴏᴘᴇɴ ʟɪɴᴋ 💀", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="🪄 sʜᴀʀᴇ ʟɪɴᴋ", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ],[
            InlineKeyboardButton(text="🍃 ᴄʟᴏsᴇ 🍃", callback_data="close_data")
            ]])
    )
