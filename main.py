import telebot
import requests
import csv


token = "265363679:AAHtdt5ZLGLxxrxZ5PM0AkgOrQvDVtIss3k"

HOST = ""

with open('token.txt') as token_file:
    token = token_file.read()
bot = telebot.TeleBot(token.strip())

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    welcome_string = """Tʜɪs Rᴏʙᴏᴛ ᴄᴀɴ ᴄᴏᴍᴘɪʟᴇ ᴄᴏᴅᴇ ɢɪᴠᴇɴ ᴛᴏ ɪᴛ﹐ ᴜsɪɴɢ ᴘᴀsᴛᴇʙɪɴ
    ᴜʀʟs. Jᴜsᴛ ᴜsᴇ /ᴄᴏᴍᴘɪʟᴇ <ᴘᴀsᴛᴇʙɪɴ_ɪᴅ> <ʟᴀɴɢᴜᴀɢᴇ>
    ᴛᴏ sᴛᴀʀᴛ﹗ Usᴇ /ʟᴀɴɢᴜᴀɢᴇs ᴛᴏ ᴘʀɪɴᴛ ᴀ ʟɪsᴛ
    ᴏғ ᴀʟʟ sᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇs ɪɴ ᴀ ᴛᴀʙʟᴇ﹗
Cʀᴇᴀᴛᴏʀ = @Voldemort ^^"""

    bot.reply_to(message, welcome_string)

@bot.message_handler(commands=['compile'])
def compile_link(message):
    arguments = message.text.split(" ")

    if len(arguments) < 3:
        bot.reply_to(message, "Not enough arguments :c")
        return

    arguments = arguments[1:]

    input_file = csv.DictReader(open("languages.csv"))

    id = -1
    compargs = ""

    for row in input_file:
        if row["name"].lower() == arguments[1].lower():
            id = row["id"]
            compargs = row["compileargs"]

    if id is -1:
        bot.reply_to(message,  "<Language is not supported>")
        return

    code = requests.get('http://pastebin.com/raw.php?i=' + arguments[0])
    if code.status_code != 200 or "Page Is Removed" in code:
        bot.reply_to(message, "Error while getting code")
        return;

    args = {}
    args["LanguageChoiceWrapper"] = id #"Python"#id
    args["Program"] = code
    args["CompilerArgs"] = compargs

    try:
        r = requests.post(HOST, data = args,
                        timeout=10)
    except requests.exceptions.Timeout:
        bot.reply_to(message, "Error: timeout while executing")
        return


    output = r.json()


    response = "Output: \n"
    if "Errors" in output and output["Errors"]:
        response += "An error occured: \n"
        response += output["Errors"]
        bot.reply_to(message, response)
        return

    response +=  output["Result"]+ "\n"
    response += "stats:\n " + output["Stats"] + "\n"
    response += "URL: https://pastebin.com/raw.php?i=" + arguments[0] + "\n"
    bot.reply_to(message, response)


@bot.message_handler(commands=['languages'])
def print_languages(message):
    input_file = csv.DictReader(open("languages.csv"))
    response = "Supported languages:\n"
    for row in input_file:
        response += row["name"].lower()
        response += "\n"

    bot.reply_to(message,response)

if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError:
        pass
