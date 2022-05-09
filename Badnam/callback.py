from XDX.queues import QUEUE
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    OWNER_NAME,
)







@Client.on_callback_query(filters.regex("cbmenu"))
async def cbmenu(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\n» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
          await query.edit_message_text(
              f"⚙️ **settings of** {query.message.chat.title}\n\n°❚❚ : pause stream\n°⇆ : resume stream\n🔇 : mute userbot\n🔊 : unmute userbot\n°↻ : stop stream",
              reply_markup=InlineKeyboardMarkup(
                  [[
                      InlineKeyboardButton("°↻", callback_data="cbstop"),
                      InlineKeyboardButton("°❚❚", callback_data="cbpause"),
                      InlineKeyboardButton("°⇆", callback_data="cbresume"),
                  ],[
                      InlineKeyboardButton("°🔇", callback_data="cbmute"),
                      InlineKeyboardButton("°🔊", callback_data="cbunmute"),
                  ],[
                      InlineKeyboardButton("✒ Cʟᴏꜱᴇ", callback_data="cls")],
                  ]
             ),
         )
    else:
        await query.answer("❌ nothing is currently streaming", show_alert=True)
        
        
#start



@Client.on_callback_query(filters.regex("cb_start"))
async def cb_start(_, query: CallbackQuery):
    await query.edit_message_text(
       f"""ʜᴇʟʟᴏ [✨](https://telegra.ph//file/08f70fa9464a522ef465d.jpg) **ᴡᴇʟᴄᴏᴍᴇ [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
 **────「 [𝐁𝐫𝐮𝐭𝐚𝐥 𝐌𝐮𝐬𝐢𝐜](https://telegra.ph/file/9cc6f3c56940c224cd7bf.jpg) 」────**
 ** ➖➖➖➖➖➖➖➖➖➖➖➖➖ 
 **ɪ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ɢʀᴏᴜᴘ ᴠɪᴅᴇᴏ ᴄᴀʟʟ !!**
 ** ➖➖➖➖➖➖➖➖➖➖➖➖➖
 ‣ Managed By - @Its_Brutal_xD ❥︎
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⛓ Aᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ Gʀᴏᴜᴘ",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton(
                    "°Cᴏᴍᴍᴀɴᴅs", callback_data="cb_cmd"),],
                [
                    InlineKeyboardButton("°Oᴡɴᴇʀ", url=f"https://t.me/{OWNER_NAME}"),
                    InlineKeyboardButton("°Dᴇᴠᴇʟᴏᴘᴇʀ ", url=f"https://Badnam-xd.github.io/"),
                ],
                [
                    InlineKeyboardButton(
                        "• Sᴏᴜʀᴄᴇ •", url="https://t.me/XCodeSupport"
                    )
                ],
            ]
        ),
    )

    
    
    
    #Help command
    
    
@Client.on_callback_query(filters.regex("cb_cmd"))
async def cb_cmd(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Hello !**
» **ғᴏʀ ᴀɴʏ ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅ ᴄʟɪᴄᴋ ʙᴜᴛᴛᴏɴs 🔭 !**
⚡ Powered by [O W N E R](https://t.me/{OWNER_NAME})""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• Mᴜꜱɪᴄ Cᴏᴍᴍᴀɴᴅꜱ", callback_data="cb_basic"),
                    InlineKeyboardButton("°Sᴜᴅᴏ ᴜꜱᴇʀ •", callback_data="cb_advance"),
                ],
                [InlineKeyboardButton("°Sᴇᴍx", callback_data="cb_fun")],
               
                [InlineKeyboardButton("✒ Bᴀᴄᴋ", callback_data="cb_start")],
            ]
        ),
    )
    
@Client.on_callback_query(filters.regex("cb_basic"))
async def cb_basic(_, query: CallbackQuery):
    await query.edit_message_text(  
        f"""𝔖𝔦𝔪𝔭𝔩𝔢...ℭ𝔬𝔪𝔪𝔞𝔫𝔡𝔰..
        
        
•  `/play (song name)` 
•  `/vplay (song name)` 
•  `/vstream (song name)` 
•  `/skip` - skip the current song
•  `/end` - stop music play
•  `/pause` - pause song play
•  `/resume` - resume song play
•  `/mute` - mute assistant in vc
•  `/lyrics (song name)`

⛄ Powered By [O W N E R](https://t.me/{OWNER_NAME}) .""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✒ Bᴀᴄᴋ", callback_data="cb_cmd")]]
        ),
    )
    
    
@Client.on_callback_query(filters.regex("cb_advance"))
async def cb_advance(_, query: CallbackQuery):
    await query.edit_message_text(    
      f"""𝔗𝔵𝔱𝔯𝔞... ℭ𝔬𝔪𝔪𝔞𝔫𝔡𝔰.
• `/ping` pong !!
• `/start` - Alive msg ~group 
• `/id` - Find out your grp and your id // stickers id also
• `/uptime` - 💻
• `/rmd` clean all downloads
• `/clean` - clear storage 

⛄ Powered By [O W N E R](https://t.me/{OWNER_NAME}) .""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✒ Bᴀᴄᴋ", callback_data="cb_cmd")]]
        ),
    )
    
    
@Client.on_callback_query(filters.regex("cb_fun"))
async def cb_fun(_, query: CallbackQuery):
    await query.edit_message_text(  
        f"""𝔖𝔢𝔵.. ℭ𝔬𝔪𝔪𝔞𝔫𝔡..
• `/truth` 🖕
• `/dare` 🖕 
• `/XDX` 🖕   
• `/tpatp` 🖕  
• `/OSM` 🖕  

⛄ Powered By [O W N E R](https://t.me/{OWNER_NAME}) .""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✒ Bᴀᴄᴋ", callback_data="cb_cmd")]]
        ),
    )
        

    
    
    
        


@Client.on_callback_query(filters.regex("cls"))
async def close(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("🤭😅ɴɪᴋᴀʟ ʙsᴅᴋ ᴛᴜ ᴀᴅᴍɪɴ ɴᴀʜɪ ʜᴀɪ ɢʀᴘ ᴋᴀ !", show_alert=True)
    await query.message.delete()
