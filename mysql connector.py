import string
from tarfile import RECORDSIZE
from datetime import date, datetime
import telebot
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

@bot.message_handler(commands=['hasil'])
def hasil(message):
    texts = message.text.split(' ')

    # print(texts)
    sto = texts[1]
    nomor_feeder = texts[2]
    
    sql.execute("select nomor, sto, nama_feeder, nomor_feeder, panel, core_digunakan from feeder_cigudeg where nomor_feeder='{}'".format(nomor_feeder))
    hasil_sql = sql.fetchmany(288)

    #print(hasil_sql)

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
    bot.reply_to(message,'Data Berhasil di Input')

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
bot.polling()