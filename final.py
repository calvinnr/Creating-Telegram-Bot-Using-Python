import telebot
import string
from tarfile import RECORDSIZE
from datetime import date, datetime
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    port='33060',
    user='root',
    passwd='',
    db='feederbogor_bot')

sql = mydb.cursor()

api = '5379965024:AAEgtlAbCAnVf5uDDGSFUIfqg02ezZFQ_P8'
bot = telebot.TeleBot(api)

user = ''

@bot.message_handler(commands=['start'])
def action_start(message):
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
    /start -> Untuk memulai Bot Feeder Bogor
    /id -> Untuk melihat ID kamu
    /help -> Untuk melihat list command Bot Feeder Bogor
    /masukan -> Untuk memasukan data feeder (Format: [STO] [Nama Feeder] [Nomor Feeder] [Panel] [Core Digunakan] [Tanggal YYYY-MM-DD])
    /update -> Untuk memperbarui data feeder yang telah dimasukan (Format: [Nomor] [Core terbaru]
    /hasil -> Untuk melihat data feeder yang telah dimasukan dengan urutan hasil berikut -> Nomor - STO - Nama Feeder - Nomor Feeder - Panel - Core Digunakan - Tanggal (Format Input: [STO] [Nomor Feeder])
    '''.format(nama))

@bot.message_handler(commands=['hasil'])
def hasil(message):
    texts = message.text.split(' ')
    sto = texts[1]
    nomor_feeder = texts[2]
    
    sql.execute("select nomor, sto, nama_feeder, nomor_feeder, panel, core_digunakan from feeder_cigudeg where nomor_feeder='{}'".format(nomor_feeder))
    hasil_sql = sql.fetchmany(288)

    pesan_balasan = ''
    for x in hasil_sql:
        pesan_balasan = pesan_balasan + str(x) + '\n'
        

        pesan_balasan = pesan_balasan.replace("'","")
        pesan_balasan = pesan_balasan.replace("(","")
        pesan_balasan = pesan_balasan.replace(")","")
        pesan_balasan = pesan_balasan.replace(",","")

    bot.reply_to(message, pesan_balasan)

@bot.message_handler(commands=['masukan'])
def masukan(message):
    texts = message.text.split(' ')
    sto = texts[1]
    nama_feeder = texts[2]
    nomor_feeder = texts[3]
    panel = texts[4]
    core_digunakan = texts[5]
    tanggal = texts[6]

    insert = 'insert into feeder_cigudeg (sto, nama_feeder, nomor_feeder, panel, core_digunakan, tanggal) values (%s,%s,%s,%s,%s,%s)'
    val = (sto, nama_feeder, nomor_feeder, panel, core_digunakan, tanggal)
    sql.execute(insert, val)
    mydb.commit()
    bot.reply_to(message, 'Data Berhasil di Input')

@bot.message_handler(commands=['update'])
def update(message):
    texts = message.text.split(' ')
    nomor = texts[1]
    core_digunakan = texts[2]

    update = 'update feeder_cigudeg set core_digunakan=%s where nomor=%s'
    val = (nomor, core_digunakan)
    sql.execute(update, val)
    mydb.commit()
    bot.reply_to(message, 'Data Berhasil di Update')

print('bot start running')
bot.infinity_polling()