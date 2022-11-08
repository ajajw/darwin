"""
≛ <b>Commands Available</b> ≛

──────────────────────
- <code>/logs</code>: Get Whole logs file.
──────────────────────
- <code>/proxy_on</code>: Turn on Proxy.
──────────────────────
- <code>/proxy_off</code>: Turn off Proxy.
──────────────────────
- <code>/add_chat</code>: Approve chat.
──────────────────────
- <code>/del_chat</code>: Disapprove chat.
──────────────────────
- <code>/lives</code>: Get all live cards.
──────────────────────
- <code>/pvtusers</code>: Get all privatt users.
──────────────────────

©<a href="https://t.me/roldexverse">RoldexVerse</a>
"""


import asyncio
import os,sys
import threading
from mills import LOG_CHAT
from mills.decorators import bot_cmd
from mills.plugins.checkers.utils.gateinfo import get_gate_info
from .._helpers.strings  import get_strings
from mills import client, sdb


@bot_cmd(cmd="proxy_on", admins_only = True)
async def _(m):
    text = m.pattern_match.group(1).strip()
    test = await m.adb.set_key(f'use_proxy', text)
    if test:
        await m.sod("Proxy turned on Successfully", time = 5)
    else:
        await m.sod(f"{str(test)}", time = 5)



@bot_cmd(pattern="proxy_off$", admins_only = True)
async def _(m):
    test = await m.adb.del_key(f'use_proxy')
    if test:
        await m.sod("Proxy turned off Successfully", time = 5)
    else:
        await m.sod(f"{str(test)}", time = 5)




@bot_cmd(cmd="add_chat", admins_only = True, group_only = True)
async def _(m):
    if await m.adb.get_key(f'approved_{str(m.chat_id)}'):
        return m.sod(f"<code>{m.chat_id}</code> already added.")
    test = await m.adb.set_key(f'approved_{str(m.chat_id)}', m.chat_id)
    if test:
        await m.sod("𝗖𝗵𝗮𝘁 𝗔𝗱𝗱𝗲𝗱 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆", time = 5)
    else:
        await m.sod(f"{str(test)}", time = 5)




@bot_cmd(cmd="del_chat", admins_only = True, group_only = True)
async def _(m):
    if not await m.adb.get_key(f'approved_{str(m.chat_id)}'):
        return m.sod(f"<code>{m.chat_id}</code> not added.")
    test = await m.adb.del_key(f'approved_{str(m.chat_id)}')
    if test:
        await m.sod("𝘾𝙝𝙖𝙩 𝙍𝙚𝙢𝙤𝙫𝙚𝙙 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮", time = 5)
    else: await m.sod(f"Chat not authorized may be.", time = 5)



@bot_cmd(pattern="logs$", admins_only = True, is_private = True) #help( (.*)|$)
async def _(m):
    if os.path.exists("millie.log"):
        await m.sod(file = 'millie.log', time = 5)
    else: await m.sod("not found.")


@bot_cmd(pattern="lives$", admins_only = True, is_private = True) 
async def _(m):
    if os.path.exists("lives/lives.txt"):
        await m.sod(file = 'lives/lives.txt', time = 5)
    else: await m.sod("not found.")


@bot_cmd(cmd="broadcast", admins_only = True, is_private = True) 
async def _(m):
    text = m.pattern_match.group(1).strip()
    rm = await m.get_reply_message()
    if rm:
        text = rm.text
    
    users = sdb['users'].find({})
    all_users = []
    for user in users:
        all_users.append(user['_id'])
    mm = await m.sod("found {} users. now i am sending them.".format(len(all_users)))
    for x in all_users:
        try:
            await client.send_message(x, text)
        except:
            pass
        await asyncio.sleep(2)
        if x == all_users[-1]:
            await m.sod("Broadcasted Successfully.")
            await asyncio.sleep(3)
            await mm.delete()
            await asyncio.sleep(3)
            await m.delete()
            return
    

