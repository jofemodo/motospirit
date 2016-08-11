# Code from:
# http://codereview.stackexchange.com/questions/33878/pdomapping-a-can-open-process-data-object-management-class

import CANOpen
import csv, StringIO, binascii

"""@package PDOMapping
This package defines a PDOMapping, which is the PDO interpretation of the DictionaryEntry, but instead does the heavy lifting for PDOs. It defines the methods for sending and retrieving PDOs from CANSock.
"""

class PDOMapping(object):
	"""Provides an easy to use method for sending and recieving PDOs for a specific device."""

	def __init__(self, CANBus, deviceID):
		"""Constructor for the PDOMapping. Takes in a CANBus to communicate over and a deviceID, and calculates the 8 possible PDO identifiers from there."""
		self.CANBus = CANBus
		self.deviceID = deviceID
		self.transmitPDOBases = {}
		self.receivePDOs = {}
		for i in range(1, 5):
			self.transmitPDOBases[str(i)] = 0x80 + (0x100 * i) + self.deviceID
			msg = CANOpen.PDO((0x100 + (0x100 * i) + self.deviceID), [0x00]*8)
			self.receivePDOs[str(i)] = msg
		for i in range(5, 9):
			self.transmitPDOBases[str(i)] = 0xC0 + (0x100 * (i - 4)) + self.deviceID
			msg = CANOpen.PDO((0x140 + (0x100 * (i - 4)) + self.deviceID), [0x00]*8)
			self.receivePDOs[str(i)] = msg

	def send(self, mappingList, value):
		"""Takes in a list of different positions and a value. It breaks the value down into the appropriate number of bytes (The least amount possible) and then distributes the bytes to their different positions. This allows for one value to be spread over any number of different PDOs in any order. The mapping list must be ordered highest byte to lowest byte and specifies a tuple containing the PDO number and byte number for that bytes position. It then sends out all the PDOs needed to complete the message. Raises an exception if the value is too large for the provided list of positions, and returns false if the communication with CANSock failed, or true if everything went well."""
		stringValue = hex(value)
		stringValue = stringValue.replace('0x', '')

		if len(stringValue) > (len(mappingList) * 2):
			raise Exception('Value is too large to fit into the PDO!')
		# String needs to have an even number of characters
		if (len(stringValue) % 2) == 1:
			stringValue = '0' + stringValue

		while (len(mappingList) * 2) > len(stringValue):
			stringValue = "00" + stringValue

		valueStringList = []
		while len(stringValue) > 0:
			valueStringList.append(stringValue[-2:])
			stringValue = stringValue[:-2]

		valueList = []
		for v in valueStringList:
			valueList.append(int(v, 16))

		PDOsToSend = []
		for messageLocation in mappingList:
			self.receivePDOs[str(messageLocation[0])].payload[messageLocation[1]-1] = valueList.pop()
			if not self.receivePDOs[str(messageLocation[0])] in PDOsToSend:
				PDOsToSend.append(self.receivePDOs[str(messageLocation[0])])
		for pdo in PDOsToSend:
			worked = self.CANBus.send(pdo.toString())
			if worked == False:
				print "Got a bad response on a send!"
				return False
		return True

	def retrieve(self, mappingList):
		"""Does the opposite of the send. Takes in a mapping list formatted in the same way as the send mapping, and then figures out which PDOs it needs to retrieve to construct the value, then does the appropriate bit shifting to create the value and returns that as an integer."""
		PDOsToRetrieve = []
		for messageLocation in mappingList:
			if not (messageLocation[0] in PDOsToRetrieve):
				PDOsToRetrieve.append(messageLocation[0])
		PDOS = {}
		for pdo in PDOsToRetrieve:
			PDOS[str(pdo)] = self.fetchPDO(pdo)
		value = '';
		for messageLocation in mappingList:
			value += PDOS[str(messageLocation[0])][messageLocation[1]]
		return int(value.replace('0x', ''), 16)

	def fetchPDO(self, pdoNumber):
		"""Private method used to retrieve a PDO. This ensures that the whole PDO is grabbed at once as opposed to fetching the same PDO 4 times to get 4 different data bytes out of it."""
		PDOCOB = self.transmitPDOBases[str(pdoNumber)]
		response = self.CANBus.send(hex(PDOCOB))
		f = StringIO.StringIO(response)
		reader = csv.reader(f, delimiter= ',', skipinitialspace=True)
		message = reader.next()
		if message[-1] == 'T':
			print 'This is the dead message: ', 
			print message
			raise Exception('PDO retrieve shows dead PDO!')
		return message
