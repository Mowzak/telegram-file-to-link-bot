import logging
import os, string
import uvloop
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message,User,InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,KeyboardButton,ReplyKeyboardMarkup
import random , json
from jason import add_user,isfirsttime,ispremium,add_post
# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# proxy = {
#      "scheme": "http",  # "socks4", "socks5" and "http" are supported
#      "hostname": "127.0.0.1",
#      "port": 10809,
#  }

# Define constants  1010954503
#get these in my.elegram
API_ID = ''
API_HASH = ''
BOT_TOKEN = ""
DOWNLOAD_DIR = 'download/'
PREMIUM_DIR = 'download/premium/'

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
if not os.path.exists(PREMIUM_DIR):
    os.makedirs(PREMIUM_DIR)


uvloop.install()
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


user_states = {}
downloading_tasks = {}
UPLOADFILE = "آپلود فایل📁"
HELP = "پشتیبانی🔰"
US="درباره ما📝"
ACC = "🧑‍💻 حساب کاربری"
MYFILE = "📁 فایل‌های من"
PREMIUM = "🌟 حساب ویژه"

button1 = KeyboardButton(UPLOADFILE)
button2 = KeyboardButton(HELP)
button3 = KeyboardButton(US)
button4 = KeyboardButton(ACC)
button5 = KeyboardButton(MYFILE)
button6 = KeyboardButton(PREMIUM)
# Create a custom keyboard
keyboard = ReplyKeyboardMarkup(
    [
        [button1],  # First row
        [button5,button6],  # First row
        [button2,button3,button4],  # second row
    ],
    resize_keyboard=True  # Make the keyboard smaller
)
#enter your number id
ADMIN_ID = 0
ASK_FILENAME, RECEIVE_FILE, DOWNLOADING = range(3)
#############################################################################

async def prog(c,total,t,client,user_id):                                   
    #this function show the progress of downlaoing
    #to prevent error of fast editing i made random system to update the progres                                                                            
    try:                                                                    
        alf = random.randint(1,100)                                         
        # print(alf)                                                      
        if alf==50:                                                         
                                                                            
            await client.edit_message_text(                                 
            chat_id=t.chat.id,                                                          
            message_id=t.id,
                 reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cancel", callback_data=f"cancel_{user_id}")]]
        ),
            text=f"در حال دانلود {(c*100)/total:.1f}%"
        )
    except Exception as e:
        print(e)
        pass
    

async def download_file(client: Client, message: Message, file_path: str,t,isp=False):
    #this funtion download the file and return download link
    ttime = 3
    try:
        
        await message.download(file_path,progress=prog,progress_args= (t,client,message.from_user.id))
        if isp:
            ttime = 12
        await client.edit_message_text(
    chat_id=t.chat.id,
    message_id=t.id,
    # text=f"Your file has been downloaded: {file_path}"
        text = f"""این لینک برای {ttime} ساعت فعال است.
                                                                            
   bananauploader.ir/{file_path}                                            
                """,        )                                                
                                                                            
        add_post(message.from_user.id,file_path.split("/")[-1])                
        print(file_path.split("/"))
    except asyncio.CancelledError:  #===> cancel button                                         
        await message.reply("با موفقیت کنسل شد.")                         
        if os.path.exists(file_path):                                       
            os.remove(file_path)                                            
    finally:                                                                
        user_id = message.from_user.id                                      
        user_states.pop(user_id, None)                                         
        downloading_tasks.pop(user_id, None)                                
#############################################################################

@app.on_message(filters.command("forward") & filters.user(ADMIN_ID))
async def start_forwarding(client: Client, message: Message):
    #this command is only for admin to brodcast a message to all user
    #admin should reply the post with /forward to send it to all users
    if message.reply_to_message:
        msg = message.reply_to_message
    else:
        message.reply_text("پیامی که میخوای به همه فرستاده بشه رو بفرست.")
        return

    # Broadcast the message to all users
    f = json.load(open("database.json",'r'))
    for user_id in f["users"]:
        try:
            
            if msg.text:
                await client.send_message(user_id, msg.text)
            elif msg.photo:
                await client.send_photo(user_id, msg.photo.file_id, caption=msg.caption)
            elif msg.video:
                await client.send_video(user_id, msg.video.file_id, caption=msg.caption)
            elif msg.audio:
                await client.send_audio(user_id, msg.audio.file_id, caption=msg.caption)
            elif msg.document:
                await client.send_document(user_id, msg.document.file_id, caption=msg.caption)
            # Add more media types as needed
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    message.reply_text("Message broadcasted to all users.")
    
@app.on_message(filters.command("users") & filters.user(ADMIN_ID))
async def usersinfo(client: Client, message: Message):
    #this command show the users and post count to admin
    f = json.load(open("database.json",'r'))
    user = 0
    posts = 0
    for i in f["users"]:
        user+=1
        posts+=len(f["users"][i]["posts"])
        
    await message.reply_text(f"number of users: {user}\n number of posts: {posts}")

#############################################################################
#############################################################################
#these commands are buttons
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    
    txt = """سلام، به ربات موز آپلودر خوش اومدی."""
    # print(message)
    user_id = str(message.from_user.id)
    add_user(user_id)
    await message.reply_text(txt,reply_markup=keyboard
                             )
    
####
@app.on_message(filters.command("help") | filters.regex(HELP)) 
async def help(client: Client, message: Message):
    txt = """
    برای ارتباط با پشتیبانی به آیدی زیر پیام دهید.\n@Banana_supporter
    """
    await message.reply(txt)
####
@app.on_message(filters.command("about") | filters.regex(US)) 
async def about(client: Client, message: Message):
    txt = """درباره ما
    """
    await message.reply(txt)
####
@app.on_message(filters.command("account") | filters.regex(ACC))
async def account(client: Client, message: Message):
    txt = """
    اکانت
    """
    await message.reply(txt)
    
####
@app.on_message(filters.command("myfile") | filters.regex(MYFILE)) 
async def myfile(client: Client, message: Message):
    txt = """
    فایل های شما:
    """
    
    await message.reply(txt)
    
@app.on_message(filters.command("premium") | filters.regex(PREMIUM)) 
async def myfile(client: Client, message: Message):
    txt = """
    حساب ویژه    
    """
    
    await message.reply(txt)
#############################################################################
#############################################################################
@app.on_message(filters.command("upload") | filters.regex(UPLOADFILE)) 
async def upload(client: Client, message: Message):
    #this command ask name that user want to save file with
    user_states[message.from_user.id] = ASK_FILENAME
    await message.reply("اسم فایلت رو برام بفرست.\nدقت کن که اسم باید انگلیسی و بدون فاصله باشه.\nدر غیر این صورت تو دانلود کردن به مشکل میخوری.")
####

@app.on_message(filters.text)
async def ask_filename(client: Client, message: Message):
    #this function get the name that user has sent with /upload
    user_id = message.from_user.id
    if user_states.get(user_id) == ASK_FILENAME:
        filename = message.text
        filename = filename.translate({ord(c): None for c in string.whitespace}) 
        if os.path.exists(filename):
            await message.reply(f"The filename '{filename}' already exists. Please choose a different filename.")
        else:
            user_states[user_id] = RECEIVE_FILE
            user_states[f"{user_id}_filename"] = filename
            txt = f"حالا فایلت رو که میخوای به اسم '{filename}' ذخیره بشه بفرست برام."
            await message.reply(txt)

####
@app.on_message(filters.document | filters.audio|filters.video|filters.photo|filters.voice)
async def handle_file(client, message: Message):
    #this funtion handle the file that user has send
    user_id =str(message.from_user.id)
    
    if bool(message.document):
        file = message.document
        file_name = file.file_name
    elif bool(message.video):
        file = message.video
        file_name = file.file_name
        file_name = 'xx.mp4' if file_name is None else file_name


    elif bool(message.photo):
        file = message.photo
        file_name = file.file_id+".png"
        file_name = 'xx.mp3' if file_name is None else file_name



    elif bool(message.audio):
        file = message.audio
        file_name = file.file_name
    elif bool(message.voice):
        file = message.voice
        file_name = file.file_id+"mp3"
        #بعذاا
        
    file_name = str(random.randint(1000000000,9999999999))+"."+file_name.split(".")[-1]
    if user_states.get(int(user_id)) == RECEIVE_FILE:  #=======> out user name on file
        file_name = user_states.pop(f"{user_id}_filename")+"_"+str(random.randint(1000000000,9999999999))+"."+file_name.split(".")[-1]
        user_states.pop(user_id, None)
    else:
        elsetext = """
شما اسمی برای فایل خودت انتخاب نکردید درنتیجه فایل با اسم پیشفرض به ثبت رسید.
برای انتخاب نام فایل:
/upload
"""

        
        await message.reply(elsetext,
                            reply_markup=keyboard)
        
        

    if ispremium(user_id):
        cancel_keyboard=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cancel", callback_data=f"cancel_{user_id}")]]
        )
        file_path = os.path.join(PREMIUM_DIR, file_name)
        t = await client.send_message(
        chat_id=message.chat.id,   reply_markup=cancel_keyboard,
        text="شروع دانلود..",reply_to_message_id=message.id)
    
        user_states[user_id] = DOWNLOADING
        task = asyncio.create_task(download_file(client, message, file_path,t,True))
        downloading_tasks[user_id] = task
        return

    if (file.file_size/1000000)>5000:
        if isfirsttime(user_id):
            f = json.load(open("database.json"))
            f["users"][user_id]["isf"] -= 1
            with open("database.json","w") as data:
                json.dump(f,data)


        else:
            errortext = """حد مجاز مصرف شما به پایان رسیده."""
            await client.send_message(
                                            chat_id=message.chat.id,
                                            text=errortext
                                            ,reply_to_message_id=message.id
                                        )
            return


    # Download the file
    cancel_keyboard=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cancel", callback_data=f"cancel_{user_id}")]]
        )
    file_path = os.path.join(DOWNLOAD_DIR, file_name)
    t = await client.send_message(
    chat_id=message.chat.id,   reply_markup=cancel_keyboard,
    text="شروع دانلود..",reply_to_message_id=message.id)

    user_states[user_id] = DOWNLOADING
    task = asyncio.create_task(download_file(client, message, file_path,t,False))
    downloading_tasks[user_id] = task



#############################################################################
# Callback query handler for cancel button
@app.on_callback_query(filters.regex(r"cancel_\d+"))
async def cancel_download(client: Client, callback_query):
    #if cancel button pushed
    user_id =  (callback_query.data.split("_")[1])
    if str(user_id) in downloading_tasks:
        downloading_tasks[str(user_id)].cancel()
        await callback_query.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer()
        
#############################################################################
#############################################################################
def main():
    app.run()

if __name__ == '__main__':
    main()

