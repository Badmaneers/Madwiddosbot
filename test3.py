import telebot
import subprocess

# Replace 'YOUR_API_KEY' with your actual bot token
API_TOKEN = '7129718094:AAGAX62hkUEwAhbS9O3vm9HJmAOSwap6kQY'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Command Runner Bot! Use /run to start the process.")

@bot.message_handler(commands=['run'])
def handle_run(message):
    msg = bot.reply_to(message, "Please provide the following inputs separated by a space:\n1. Method\n2. Domain")
    bot.register_next_step_handler(msg, process_inputs)

def process_inputs(message):
    try:
        inputs = message.text.split()
        if len(inputs) != 2:
            raise ValueError("Invalid number of inputs. Please provide exactly 2 inputs.")

        method = inputs[0]
        domain = inputs[1]

        # Construct and execute the command
        command = f"python setup.py '{method}' '{domain}' 1000 120"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")

    except Exception as e:
        bot.reply_to(message, f"Error processing inputs: {str(e)}")        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
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

@bot.message_handler(commands=['help'])
def handle_help(message):
    try:
        # Execute the command `python setup.py help`
        process = subprocess.Popen(['python', 'setup.py', 'help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            bot.reply_to(message, f"Command executed successfully:\n{output.decode('utf-8')}")
        else:
            bot.reply_to(message, f"Error executing command:\n{error.decode('utf-8')}")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
        

bot.polling()
