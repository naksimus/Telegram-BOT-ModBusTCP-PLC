import telebot
import time
import threading
import logging

bot = telebot.TeleBot("1414457957:AAFDmhfa8amUVRICFYrCMkC1nN8Yp0YsZ5Y")
from telebot import types



def sleeper():
	i = 1
	error = []
	while True:
		while 1==1:
			regs_r = []
			with open('listfile.txt', 'r') as filehandle:
				for line in filehandle:
					regs0 = line[:-1] # удаляем разрыв строки, который является последним символом строки
					regs_r.append(regs0) # добовляем елемент в список
			i += 1
			if i == 11:
				break
		with open('readerror.txt', 'r') as filehandle:
			for line in filehandle:
				error0 = line[:-1] # удаляем разрыв строки, который является последним символом строки
				error.append(error0) # добовляем елемент в список
		regs = regs_r + error
		time.sleep(1)
		return regs
t = threading.Thread(target=sleeper)
t.start()

def sleeper1():
	while True:
		joinedFile = open("user.txt", "r")
		joinedUsers = set()
		for line in joinedFile:
			joinedUsers.add(line.strip())
		joinedFile.close()	
		return joinedUsers
time.sleep(5)
t = threading.Thread(target=sleeper1)
t.start()



def sleeper2():
	TrueM = ["Соединение с ПЛК ОК!", "Задание системы: ПУСК", "Система включена", "Засор фильтра!", "Фиксация аварий:"]
	FalseM = ["Нет связи с ПЛК!", "Задание системы: СТОП", "Система отключена", "Фильтр чист", "Аварии устранены"]

	alarmstart = 3
	alarmtest = 0
	regs = []
	alarm = ['alarm']
	prevVal = [None, None, None, None, None]
	while True:

		regs = sleeper()
		r2b11 = int(regs[5]) & 2048 !=0 #есть авария? 
		alarm = int(r2b11)
		error = int(regs[10]) & 1 != 0
		on_off = int(regs[3]) & 16 !=0 #текущее заданее
		system = int(regs[3]) & 8 !=0 # текущее состояние системы
		Filter = int(regs[5]) & 8192 !=0 # Засор приточного фильтр
		
		Val = [error, on_off, system, Filter, alarm]

		AutoMessage(TrueM, FalseM, Val, prevVal, 4)

		prevVal = Val
t = threading.Thread(target=sleeper2)
t.start()

def AutoMessage(TrueM, FalseM, Val, prevVal, SendAlarm):
		joinedUsers = sleeper1()
		regs = []
		regs = sleeper()
		i = 0
		maxlen = int(len(TrueM))
		while i != maxlen:
			if prevVal[i] is not None:
				if Val[i] != prevVal[i]:
					if Val[i]:
						info = TrueM[i]
						for user in joinedUsers:
							bot.send_message(user, info)
							if SendAlarm == i:
								messages = prepareMessage('alarm', regs)
								for objMessage in messages:
									bot.send_message(user, objMessage.text)
					else:
						info = FalseM[i]
						for user in joinedUsers:
							bot.send_message(user, info)
			i = i + 1
	
	


time.sleep(2)


with open("password.txt", "r") as readpassword:
	password = readpassword.read()


@bot.message_handler(commands=['add_me_' + str(password)])
def addme(message):
	user1 = str(message.chat.id)
	joinedFile = open("user.txt", "r")
	joinedUsers = set()
	for line in joinedFile:
		joinedUsers.add(line.strip())
	joinedFile.close()
	for user1 in joinedUsers:
		send = "Ваш ID уже добавлен к боту"
		pass

	if not str(message.chat.id) in joinedUsers:
		joinedFile = open("user.txt", "a")
		joinedFile.write(str(message.chat.id) + "\n")
		joinedUsers.add(message.chat.id)
		send = "Ваш ID добавлен к боту. Рекомендуем удалить сообщение с паролем"
	bot.send_message(message.chat.id, send)


@bot.message_handler(commands=['start'])
def start(message):
	#keyboard
	markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

	markup.row("Состояние системы")
	markup.row("Температуры", "Заслонки")

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот создан чтобы отслеживать данные с ПЛК по протоколу ModBusTCP.".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)

	user2 = str(message.chat.id)
	joinedFile = open("user.txt", "r")
	joinedUsers = set()
	for line in joinedFile:
		joinedUsers.add(line.strip())
	joinedFile.close()
	for user2 in joinedUsers:
		send = "Оповещения активированны, ID в базе данных"
		pass

	if not str(message.chat.id) in joinedUsers:
		send = "Оповещения для ващего ID не активированны"
	bot.send_message(message.chat.id, send)


@bot.message_handler(commands=['special'])
def mess(message):
	joinedUsers = sleeper1()
	for user in joinedUsers:
		bot.send_message(user,"Сообщение от: {0.first_name} {0.last_name}\n".format(message.from_user, bot.get_me()), message.text[message.text.find(' '):])
		bot.send_message(user, message.text[message.text.find(' '):])

@bot.message_handler(commands=['special_noname'])
def mess(message):
	joinedUsers = sleeper1()
	for user in joinedUsers:
		bot.send_message(user, message.text[message.text.find(' '):])

@bot.message_handler(content_types=['text'])
def send_echo(message):	
		regs = []
		regs = sleeper()
		error = int(regs[10]) & 1 != 0
		
		if error:
			messages = prepareMessage(message.text, regs)
			for objMessage in messages:
				print(objMessage.reply_markup)
				bot.send_message(message.chat.id, objMessage.text, reply_markup=objMessage.reply_markup)

		else:
			print("Соединение отсутсвтует")
			infsys = "Соединение отсутсвтует"
			bot.send_message(message.chat.id, infsys)

class Message:
	text = ''
	reply_markup = None

	def __init__(self, text, reply_markup=None):
		self.text = text
		self.reply_markup = reply_markup

		
def prepareMessage(messageText, regs):
	messages = []
	regs = []
	regs = sleeper()
	r0b0 = int(regs[3]) & 1 !=0 # season 0-leto/1 -zima
	r0b1 = int(regs[3]) & 2 !=0 # auto season
	r0b2 = int(regs[3]) & 4 !=0 # #местное/дистанционное управление пуском
	r0b3 = int(regs[3]) & 8 !=0 # текущее состояние системы
	r0b4 = int(regs[3]) & 16 !=0 #текущее заданее
	r0b5 = int(regs[3]) & 32 !=0 #задание двигателю П3
	r0b6 = int(regs[3]) & 64 !=0 #задание двигателю П1
	r0b7 = int(regs[3]) & 128 !=0 #задание двигателю П2
	r2b11 = int(regs[5]) & 2048 !=0 #есть авария? 
	r2b0 = int(regs[5]) & 1 !=0 # авария П3
	r2b1 = int(regs[5]) & 2 !=0 # авария П1
	r2b2 = int(regs[5]) & 4 !=0 # авария П2
	r2b3 = int(regs[5]) & 8 !=0 # авария Ав Фильтр
	r2b4 = int(regs[5]) & 16 !=0 #авария Пожар
	r2b5 = int(regs[5]) & 32 !=0 #авария Газ
	r2b6 = int(regs[5]) & 64 !=0 #авария Тнар
	r2b7 = int(regs[5]) & 128 !=0 #авария Тцех
	r2b8 = int(regs[5]) & 256 !=0 #авария Тсмеш
	r2b9 = int(regs[5]) & 512 !=0 #авария ПускГр
	r2b10 = int(regs[5]) & 1024 !=0 #авария СтопГр
	r2b13 = int(regs[5]) & 8192 !=0 # Засор приточного фильтр
	if messageText == 'Состояние системы':

				infsys = "Состояние системы" + "\n\n"
				infsys += "Система: "  #текущее состояние системы
				if r0b3:
					infsys += "включена" + "\n"
				else:
					infsys += "отключена" + "\n"
				infsys += "Текущее задание: "  #текущее заданее
				if r0b4:
					infsys += "пуск" + "\n"
				else:
					infsys += "стоп" + "\n"
				infsys += "Управление: "  #местное/дистанционное управление пуском
				if r0b2:
					infsys += "дистанционное" + "\n"
				else:
					infsys += "местное" + "\n"
				infsys += "Сезон: "  #местное/дистанционное управление пуском
				if r0b0:
					infsys += "зима" + "\n"
				else:
					infsys += "лето" + "\n"
				infsys += "Двигатель П3: "  #текущее заданее
				if r0b5:
					infsys += "пуск" + "\n"
				else:
					infsys += "стоп" + "\n"
				infsys += "Двигатель П1: "  #текущее заданее
				if r0b6:
					infsys += "пуск" + "\n"
				else:
					infsys += "стоп" + "\n"
				infsys += "Двигатель П2: "  #текущее заданее
				if r0b7:
					infsys += "пуск" + "\n"
				else:
					infsys += "стоп" + "\n"
				infsys += "Фильтр: "  #текущее заданее
				if r2b13:
					infsys += "засор" + "\n\n"
				else:
					infsys += "чист" + "\n\n"
				infsys += "Наличие аварии: "  #наличие аварии
				if r2b11:
					infsys += "есть!" + "\n"
				else:
					infsys += "нет" + "\n"
				message = Message(infsys)
				messages.append(message)

				if r2b11:
					markup = types.InlineKeyboardMarkup(row_width = 1)
					item1 = types.InlineKeyboardButton("Просмотр текущих аварий", callback_data='alarm')

					markup.add(item1)
					message = Message('Посмотреть текущие аварии?', markup)
					messages.append(message)

	elif messageText == 'Температуры':

				time_n_int16 = int(regs[0])
				if time_n_int16 > 10000:
					time_n = time_n_int16 - 65535
				else: 
					time_n = time_n_int16

				time_z_int16 = int(regs[1])
				if time_z_int16 > 10000:
					time_z = time_z_int16 - 65535
				else: 
					time_z = time_z_int16

				time_k_int16 = int(regs[2])
				if time_k_int16 > 10000:
					time_k = time_k_int16 - 65535
				else: 
					time_k = time_k_int16					
									
				answer = "Датчики температур" + "\n\n"
				answer += "Улица: " + str(int(time_n * 0.1 * 10) / 10) + " °С" + "\n"
				answer += "В цеху: " + str(int(time_z * 0.1 * 10) / 10) + " °С" + "\n"
				answer += "В камере смешения: " + str(int(time_k * 0.1 * 10) / 10) + " °С"

				message = Message(answer)
				messages.append(message)
			
	elif messageText == 'Заслонки':
				answer = "Текущее положение заслонок" + "\n\n"
				answer += "Приток:  " + str(int(regs[6])) + " %" +  "\n"
				answer += "Камера смешения:  " + str(int(regs[9])) + " %" + "\n"
				answer += "П1:  " + str(int(regs[7])) + " %" 
				answer += "          П2:  " + str(int(regs[8]))  + " %"
				message = Message(answer)
				messages.append(message)

	elif messageText == 'alarm':
				alarm_info = ""	
				if r2b0:
					alarm_info += "Авария П3" + "\n"

				if r2b1:
					alarm_info += "Авария П1" + "\n"

				if r2b2:
					alarm_info += "Авария П2" + "\n"

				if r2b3:
					alarm_info += "Авария Фильтр" + "\n"

				if r2b4:
					alarm_info = "Авария Пожар" + "\n"

				if r2b5:
					alarm_info += "Авария Газ" + "\n"

				if r2b6:
					alarm_info += "Авария Тнар" + "\n"

				if r2b7:
					alarm_info += "Авария Тцех" + "\n"

				if r2b8:
					alarm_info += "Авария Тсмещ" + "\n"

				if r2b9:
					alarm_info += "Авария ПускГрафик" + "\n"

				if r2b10:
					alarm_info += "Авария СтопГрафик" + "\n"
				message = Message(alarm_info)
				messages.append(message)

	else:
				message = Message('Кожаный, я не понимаю что ты от меня хочешь, научи сначала...')
				messages.append(message)

	return messages	
	
@bot.message_handler(content_types=['text'])
def send_echo(message):	
		regs = []
		regs = sleeper()
		error = int(regs[10]) & 1 != 0
		
		if error:
			messages = prepareMessage(message.text, regs)
			for objMessage in messages:
				print(objMessage.text)
				bot.send_message(message.chat.id, objMessage.text, reply_markup=objMessage.reply_markup)

		else:
			print("Соединение отсутсвтует")
			infsys = "Соединение отсутсвтует"
			bot.send_message(message.chat.id, infsys)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			# if call.data == 'alarm':
				regs = []
				regs = sleeper()
			
				messages = prepareMessage(call.data, regs)
				for objMessage in messages:
					bot.send_message(call.message.chat.id, objMessage.text)
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Текущие аварии:", reply_markup=None) 
	except Exception as e:
		print(repr(e))

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

bot.polling( none_stop = True )
