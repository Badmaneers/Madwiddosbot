import telebot
import subprocess

# Replace 'YOUR_API_KEY' with your actual bot token
API_TOKEN = '7129718094:AAGAX62hkUEwAhbS9O3vm9HJmAOSwap6kQY'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Start.py Bot! Use /run to execute a command or /help to get help information.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    try:
        # Execute the command `python start.py help`
        process = subprocess.Popen(['python', 'start.py', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

@bot.message_handler(commands=['run'])
def handle_run(message):
    msg = bot.reply_to(message, "Please provide the inputs separated by spaces in the following order:\n1. Method\n2. IP:Port\n3. Thread\n4. Time")
    bot.register_next_step_handler(msg, process_inputs)

def process_inputs(message):
    try:
        inputs = message.text.split()
        if len(inputs) != 4:
            raise ValueError("Invalid number of inputs.")

        method = inputs[0]
        ip_port = inputs[1]
        thread = inputs[2]
        time = inputs[3]

        # Example command execution, adjust as necessary
        command = f"python start.py {method} {ip_port} {thread} {time}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")
    except Exception as e:
        bot.reply_to(message, f"Error processing inputs: {str(e)}")

bot.polling()
