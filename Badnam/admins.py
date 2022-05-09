from XDX.Cache.admins import admins
from BruTalxD.main import call_py
from pyrogram import Client, filters
from XDX.decorators import authorized_users_only
from XDX.filters import command, other_filters
from XDX.queues import QUEUE, clear_queue
from XDX.utils import skip_current_song, skip_item
from config import BOT_USERNAME, IMG_3
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("✒ Bᴀᴄᴋ", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("♨ Cʟᴏꜱᴇ", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "⚡ Bᴏᴛ **°Rᴇʟᴏᴀᴅᴇᴅ Cᴜʀᴇɴᴛʟʏ !**\n⛄ **°Aᴅᴍɪɴ Lɪꜱᴛ** Hᴀꜱ **Uᴘᴅᴀᴛᴇᴅ !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="°Mᴇɴᴜ", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="°Cʟᴏsᴇ", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ Nᴏ Mᴏʀᴇ Cᴜʀᴇɴᴛʟʏ Pʟᴀʏɪɴɢ")
        elif op == 1:
            await m.reply("🌀 __Qᴜᴇᴜᴇꜱ__ **Iꜱ Eᴍᴘᴛʏ.**\n\n**• Uꜱᴇʀ Bᴏᴛ Lᴇᴀᴠɪɴɢ Tʜɪꜱ Vᴄ**")
        elif op == 2:
            await m.reply("⚡ **Cʟᴇᴀʀɪɴɢ Tʜɪꜱ Qᴜᴇᴜꜱᴇ**\n\n**• Uꜱᴇʀ Bᴏᴛ Lᴇᴀᴠɪɴɢ Tʜɪꜱ Vᴄ**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"⏭ **Sᴋɪᴘᴇᴅ Tᴏ Tʜᴇ Nᴇxᴛ Tʀᴀᴄᴋ.**\n\n🏷 **°Nᴀᴍᴇ:** [{op[0]}]({op[1]})\n💭 **°Cʜᴀᴛ:** `{chat_id}`\n💡 **°Sᴛᴀᴛᴜꜱ:** `Playing`\n🎧 **°RᴇQᴇꜱᴛᴇᴅ Bʏ:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **Rᴇᴍᴏᴠᴇ Sᴏɴɢ Fʀᴏᴍ Qᴜᴇꜱᴇ:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ Tʜᴇ Uꜱᴇʀ Bᴏᴛ Dɪꜱꜱᴄᴏɴᴇᴄᴛᴇᴅ Fʀᴏᴍ Vɪᴅᴇᴏ Cʜᴀᴛ.")
        except Exception as e:
            await m.reply(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "📶 **Pᴀᴜꜱᴇᴅ.**\n\n• **Tᴏ Rᴇꜱᴜᴍᴇ Tʜᴇ Sᴛʀᴇᴀᴍ, Uꜱᴇ Tʜᴇ**\n» /resume Cᴏᴍᴍᴏɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **Rᴇꜱᴜᴍᴇᴅ.**\n\n• **Tᴏ Pᴀᴜꜱᴇᴅ Tʜᴇ Sᴛʀᴇᴀᴍ, Uꜱᴇ Tʜᴇ**\n» /pause Cᴏᴍᴍᴏɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "🔇 **Uꜱᴇʀ Bᴏᴛ Mᴜᴛᴇᴅ.**\n\n• **Tᴏ Uɴᴍᴜᴛᴇ Tʜᴇ Uꜱᴇʀʙᴏᴛ, Uꜱᴇ Tʜᴇ**\n» /unmute Cᴏᴍᴍᴏɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "🔊 **Uꜱᴇʀ Bᴏᴛ Unᴍᴜᴛᴇᴅ.**\n\n• **Tᴏ ᴍᴜᴛᴇ Tʜᴇ Uꜱᴇʀʙᴏᴛ, Uꜱᴇ Tʜᴇ**\n» /mute Cᴏᴍᴍᴏɴᴅ."
            )
        except Exception as e:
            await m.reply(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ Tʜᴇ Sᴛʀᴇᴀᴍ Hᴀꜱ Pᴀᴜꜱᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)
        
        
@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.skip_stream(chat_id)
            await query.edit_message_text(
                "⏸ Tʜᴇ Sᴛʀᴇᴀᴍ Hᴀꜱ Sᴋɪᴘᴘᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ Tʜᴇ Sᴛʀᴇᴀᴍ Hᴀꜱ Rᴇꜱᴜᴍᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **Tʜɪꜱ Sᴛʀᴇᴀᴍɪɴɢ Hᴀꜱ Eɴᴅ**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 Uꜱᴇʀ Bᴏᴛ Mᴜᴛᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 Uꜱᴇʀ Bᴏᴛ Uɴᴍᴜᴛᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **Vᴏʟᴜᴍᴇ Sᴇᴛ Tᴏ** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("❌ **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")

        
@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "💬 Tʜᴇ Sᴛʀɪᴍɪɴɢ Hᴀꜱ Pᴀᴜꜱᴇᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "💬 Tʜᴇ Sᴛʀᴇᴀᴍɪɴɢ Hᴀꜱ Rᴇꜱᴜᴍᴇɴᴅ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("💬 **Tʜɪꜱ Sᴛʀᴇᴀᴍ Hᴀꜱ Eɴᴅᴇᴅ**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"💬 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "💬 Uꜱᴇʀ Bᴏᴛ Mᴜᴛᴇᴅ Sᴜᴄᴄᴇꜱ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("Yᴏᴜ 're Aɴᴏɴɴʏᴍᴏᴜꜱ Aᴅᴍɪɴ !\n\n» Rᴇᴠᴇʀᴛ Bᴀᴄᴋ Tᴏ Yᴏᴜʀ Aᴄᴄᴏᴜɴᴛ Aɴ Aᴅᴍɪɴ Rɪɢʜᴛꜱ.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 Oɴʟʏ Aᴅᴍɪɴꜱ Uꜱᴇ Tʜɪꜱ Bᴜᴛᴛᴏɴ Bꜱᴅᴋ Cᴏʟʟᴇᴄᴛ Aᴅᴍɪɴ Fɪʀꜱᴛ Aɴᴅ Tᴏᴜᴄʜ Tʜɪꜱ Bᴏᴛᴛᴏɴ !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "💬 Uꜱᴇʀ Bᴏᴛ Uɴᴍᴜᴛᴇᴅ Sᴜᴄᴄᴇꜱ", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"💬 **Eʀʀᴏʀ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("💬 Nᴏᴛʜɪɴɢ Iꜱ Cᴜʀᴇɴᴛʟʏ Sᴛʀᴇᴀᴍɪɴɢ", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"💬 **Vᴏʟᴜᴍᴇ Sᴇᴛ Tᴏ** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"💬 **Eʀʀᴏʀ:**\n\n`{e}`")
    else:
        await m.reply("💬 **Nᴏᴛʜɪɴɢ Iꜱ Sᴛʀᴇᴀᴍɪɴɢ**")
        
        
        # whats up  by BADNAM
