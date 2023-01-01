import string
from tarfile import RECORDSIZE
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
    nomor = texts[1]
    
    sql.execute("select sto, nama_feeder, nomor_feeder, panel, core_digunakan from feeder_cigudeg where nomor='{}'".format(nomor))
    hasil_sql = sql.fetchone()

    #print(hasil_sql)

    pesan_balasan = ''
    for x in hasil_sql:
        pesan_balasan = pesan_balasan + str(x) + '\n'
        

        pesan_balasan = pesan_balasan.replace("'","")
        pesan_balasan = pesan_balasan.replace("(","")
        pesan_balasan = pesan_balasan.replace(")","")
        pesan_balasan = pesan_balasan.replace(",","")

    bot.reply_to(message, pesan_balasan)

@bot.message_handler(commands=['masuk'])
def masuk(message):
    string1 = (input("STO: "))
    string2 = (input('Nama Feeder: '))
    string3 = (input('Nomor Feeder: '))
    string4 = (input('Panel: '))
    string5 = (input('Core: '))
    string6 = (input('Tanggal: '))

    insert_query = 'insert into feeder_cigudeg (sto, nama_feeder, nomor_feeder, panel, core_digunakan, tanggal) values (%s,%s,%s,%s,%s,%s)'
    #val = (sto, nama_feeder, nomor_feeder, panel, core_digunakan, tanggal)
    sql.execute(insert_query, (string1,string2,string3,string4,string5,string6), multi=True)
    mydb.commit()
    bot.reply_to(message, 'Data Berhasil di Input')

@bot.message_handler(commands=['update'])
def update(message):
    texts = message.text.split(' ')
    sto = texts[1]
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