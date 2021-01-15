import sched, time
import datetime

from pyModbusTCP.client import ModbusClient

c = ModbusClient()
c.host("192.168.0.31")
c.port(502)
# managing TCP sessions with call to c.open()/c.close()
c.auto_open(True)


s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
	i = 1
	errorlist = 0
	while 1==1:
		regs = c.read_input_registers(0, 10) #температуры
		i += 1
		if i == 2:		
			regs_t = c.read_input_registers(0, 10)
			break		
	regs = c.read_input_registers(0, 10)
	now = datetime.datetime.now()
	if regs:
		if int(len(regs)) == 10:
			error = [1]
			print(now.strftime("%d-%m-%Y %H:%M:%S.%f"))
			print("Запись" + str(regs) + " |плохие запросы: " + str(errorlist))
			with open('listfile.txt', 'w') as filehandle:
				for listitem in regs:
					filehandle.write('%s\n' % listitem)
			with open('readerror.txt', 'w') as filehandle:
				for listitem in error:
					filehandle.write('%s\n' % listitem)	
		else:
			print(now.strftime("%d-%m-%Y %H:%M:%S.%f"))
			print("Масив данных полученный из модбаса был менее или более 10 регистров!")
			errorlist = errorlist + 1
			print("|плохие запросы: " + str(errorlist))
	else:
		print(now.strftime("%d-%m-%Y %H:%M:%S.%f"))
		print("read error")		
		error = [2]
		with open('readerror.txt', 'w') as filehandle:
			for listitem in error:
				filehandle.write('%s\n' % listitem)

	s.enter(5, 1, do_something, (sc,))
s.enter(5, 1, do_something, (s,))
s.run()