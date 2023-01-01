from distutils import core
from optparse import Values
from tarfile import RECORDSIZE
from telebot import types
import telebot
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    port='3306',
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
    tanggal = texts[1]
    
    sql.execute("select sto, nama_feeder, nomor_feeder, panel, core_digunakan from feeder_cigudeg where tanggal='{}'".format(tanggal))
    hasil_sql = sql.fetchall()

    #print(hasil_sql)

    pesan_balasan = ''
    for x in hasil_sql:
        pesan_balasan = pesan_balasan + str(x) + '\n' 

        pesan_balasan = pesan_balasan.replace("'","")
        pesan_balasan = pesan_balasan.replace("(","")
        pesan_balasan = pesan_balasan.replace(")","")
        pesan_balasan = pesan_balasan.replace(",","")

    bot.reply_to(message, pesan_balasan)

@bot.message_handler(commands=['input'])
def action_input(message):
    texts = message.text.split(' ')
    sto = texts[0]
    nama_feeder = texts[2]
    nomor_feeder = texts[3]
    panel = texts[4]
    core_digunakan = texts[5]
    tanggal = texts[6]

    insert = 'insert into feeder_cigudeg (sto, nama_feeder, nomor_feeder, panel, core_digunakan, tanggal) values (%s,%s,%s,%s,%s,%s)'
    val = (sto, nama_feeder, nomor_feeder, panel, core_digunakan, tanggal)
    sql.execute(insert,val)
    mydb.commit()
    bot.reply_to(message, 'Data Berhasil di Input')

print('bot start running')
bot.polling()