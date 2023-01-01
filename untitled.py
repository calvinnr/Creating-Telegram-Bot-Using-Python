import telebot

api = '5379965024:AAEgtlAbCAnVf5uDDGSFUIfqg02ezZFQ_P8'
bot = telebot.TeleBot(api)

user = ''

@bot.message_handler(commands=['start'])
def action_start(message):
    # print(message.from_user.id)
    nama = message.chat.first_name
    bot.reply_to(message,'Semangat Pagi {} !'.format(nama))

@bot.message_handler(commands=['id'])
def action_id(message):  
    nama = message.from_user.first_name
    id_telegram = message.chat.id
    bot.reply_to(message,'''
    Hai, ID Kamu
    Nama = {}
    ID = {}
            '''.format(nama,id_telegram))    

@bot.message_handler(commands=['help'])
def action_help(message):
    nama = message.chat.first_name
    bot.reply_to(message, '''
    Hi {}, Berikut list command pada BOT
    /start -> Salam Pertama pada Bot
    /id -> Pengecekan ID
    /help -> List Command BOT
    /masukan ->
    '''.format(nama))
 
print('bot start running')
bot.polling()