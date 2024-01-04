from QueueSLL import *
from HeapPriorityQueue import *
from LinkedDeque import *
from AdaptableHeapPriorityQueue import *
from LinkedDeque import *

class NotMutable(Exception):
	pass;



class SimulatorProblem:

	Time = 0

	class _Customer:
		__slots__ = '_id', '_time', '_count', '_timeO'

		def __init__(self, id, Time, count, timeO = None):
			self._id = id
			self._time = Time
			self._count = count
			self._timeO = timeO


	def __init__(self):
		self._billingQ = []
		self._burgerC = 0
		self._totalData = []  # fistly we will add all customer her or it is the database of customer.
		self._priority = AdaptableHeapPriorityQueue()
		self._locQ = [] # it conatins the location of all self._priority in order 1 - K.
		self._localData = []

	def isEmpty(self):
		"""Returns 1(int) if there are no further events to simulate."""
		pass;

	def setK(self, k):
		"""
		The parameter k specifies the number of billing queues in the restaurant. The function returns
		with an appropriate error message if an attempt is made to modify the value of k, i.e., the
		function is called more than once
		"""
		# pass;
		if len(self._billingQ) != 0:
			raise NotMutable("you can not change the size of the billing queues")

		for i in range(k):
			self._billingQ.append(LinkedDeque())
			self._locQ.append(self._priority.add(len(self._billingQ[i]), self._billingQ[i]))

	def setM(self, m):
		"""
		The parameter m specifies maximum number of burgers that can be cooked in the griddle
		simultaneously. The function returns with an appropriate error message if an attempt is made to
		modify the value of m, i.e., the function is called more than once.
		"""
		# pass;
		if self._burgerC != 0:
			raise NotMutable("you can not change the size of the griddle")

		else:
			self._burgerC = m

	def advanceTime(self, t):
		"""Runs the simulation forward simulating all events upto (including) time t."""
		# pass;
		while SimulatorProblem.Time <= t:
			# print("yes")
			self._HendalCounter()
			SimulatorProblem.Time += 1

	def arriveCustomer(self, id, t, numb):
		"""
		A customer with ID = id arrives at time t and orders numb number of burgers. The function
		returns with appropriate error messages in the following scenarios:
			the arrival time of a customer is lower than that of a previous customer
			numb is negative
			the IDs are not consecutive

		"""
		# pass;
		newcustomer = self._Customer(id, t, numb)
		if len(self._totalData) != 0:
			lastCustomer = self._totalData[-1]
			if newcustomer._time < lastCustomer._time:
				raise ValueError("It is not possible for a new customer to arrive before the last customer.")
			if newcustomer._id - lastCustomer._id != 1:
				raise ValueError("The IDs of the customers must be consecutive integers. Please assign the new customer ID as " + str(lastCustomer._id + 1))
		if numb < 0:
			raise ValueError("The number of burgers must be positive.")
		if not len(self._totalData) == 0 and newcustomer._id == 1:
			raise ValueError("The ID of first customer must be 1")
		self._totalData.append(newcustomer)
		self._localData.append(newcustomer)

		

	def _HendalCounter(self):
		for loc in self._locQ:
			if len(loc._value) == 0:
				continue;
			for i in range(len(loc._value)):
				# print(loc._value.first()._timeO)
				if loc._value.first()._timeO == SimulatorProblem.Time:
					customer = loc._value.delete_first()
					self._priority.update(loc, len(loc._value), loc._value)
					print(f"customer with ID {customer._id} left the counter {self._locQ.index(loc) + 1} at time {customer._timeO} \n")
				else:
					continue;


		for custo in range(len(self._localData)):
			customer = self._localData[0]
			if customer._time != SimulatorProblem.Time:
				continue;
			lenOfQ1 = len(self._billingQ[0])
			lenCheck = True
			for Q in self._billingQ:
				if len(Q) != lenOfQ1:
					lenCheck = False
			if lenCheck:
				if(len(self._billingQ[0]) != 0):
					preTime = self._billingQ[0].last()._timeO
					if(preTime > customer._time):
						customer._timeO = (preTime - customer._time) + 1 + customer._time
					else:
						customer._timeO = customer._time + 1
				else:
					customer._timeO = customer._time + 1
				# customer._timeO = len(self._billingQ[0]) * 1 + 1 + customer._time
				self._billingQ[0].insert_last(customer)
				self._priority.update(self._locQ[0], len(self._billingQ[0]),self._billingQ[0])
				print(f"customer with ID {customer._id} joined in counter 1 at time {customer._time}\n")

			else:
				minQ = self._priority.min()
				if(len(minQ[1]) != 0):
					preTime = minQ[1].last()._timeO
					if(preTime > customer._time):
						customer._timeO = (preTime - customer._time) + self._billingQ.index(minQ[1]) + 1 + customer._time
					else:
						customer._timeO = customer._time + self._billingQ.index(minQ[1]) + 1
				else:
					customer._timeO = customer._time + self._billingQ.index(minQ[1]) + 1
				# customer._timeO = len(minQ[1]) * (self._billingQ.index(minQ[1]) + 1) + self._billingQ.index(minQ[1]) + 1 + customer._time
				minQ[1].insert_last(customer)
				locQ = 0
				for loc in self._locQ:
					if loc._value is minQ[1]:
						locQ = loc
				self._priority.update(locQ, len(minQ[1]), minQ[1])
				print(f"customer with ID {customer._id} joined in counter {self._locQ.index(locQ) + 1} at time {customer._time}\n") 
				# print(customer._timeO)
			self._localData.remove(self._localData[0])

	def customerState(self, id, t):
		print("not completed yet")
		pass

	def griddleState(self, t):
		print("not completed yet")
		pass

	def griddleWait(self, t):
		print("not completed yet")
		pass

	def customerWaitTime(self, id):
		print("not completed yet")
		pass

	def avgWaitTime():
		print("not completed yet")
		pass


		

			



# s = SimulatorProblem()
# s.setK(3)
# s.setM(5)
# s.arriveCustomer(1,5,2)
# s.arriveCustomer(2,10,1)
# s.arriveCustomer(3,11,3)
# s.arriveCustomer(4,12,1)
# s.advanceTime(5)
# s.advanceTime(8)
# s.advanceTime(11)
# s.advanceTime(18)

s = SimulatorProblem()
s.setK(2)
s.setM(5)
s.arriveCustomer(1,1,1)
s.arriveCustomer(2,1,1)
s.arriveCustomer(3,1,3)
s.arriveCustomer(4,2,1)
s.arriveCustomer(5,2,1)
s.arriveCustomer(6,3,1)
s.arriveCustomer(7,3,1)
s.advanceTime(1)
s.advanceTime(2)
s.advanceTime(3)
s.advanceTime(4)
s.advanceTime(5)
s.advanceTime(6)
s.advanceTime(7)


		



