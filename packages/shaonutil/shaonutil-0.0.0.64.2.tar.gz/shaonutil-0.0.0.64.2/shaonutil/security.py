"""Security"""
from uuid import UUID
import random
import string
import os


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    for c in range(10):
        letters = letters + str(c)

    return ''.join(random.choice(letters) for i in range(stringLength))



def generateSecureRandomString(stringLength=10):
    """Generate a secure random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits #+ string.punctuation
    return ''.join(secrets.choice(password_characters) for i in range(stringLength))

def CryptRandInt(length=10):
	"""Get random integer in range"""
	#byte = os.urandom(100)
	#rand = int(byte.hex(),16)
	r = random.SystemRandom()
	rndint = r.randrange( length )
	return rndint

def CryptRandString(stringLength=10,filters=[]):
	"""Generate a random string in a UUID fromat which is crytographically secure and random"""
	#generateCryptographicallySecureRandomString(stringLength=10,filters=[]):
	# uuid.uuid4() returns UUID(bytes=os.urandom(16), version=4)
	#randomString = uuid.uuid4().hex
	#os.urandom(size)
	"""
	class secrets.SystemRandom
	A class for generating random numbers using the highest-quality sources provided by the operating system. See random.SystemRandom for additional details.
	"""
	"""
	 import os

	 rand = int(os.urandom(4).encode('hex'), 16)
	 # You can then 'cycle' it against the length.
	 rand_char = chars_list[rand % 80] # or maybe '% len(chars_list)'
	"""
	"""
	If you need it for crypto purposes, use random.SystemRandom().randint(a, b), which makes use of os.urandom().
	"""
	# for reproducable classs use random and randome.seed()
	"""
	os.urandom(size) use system entropy to generate random string useful to cryptographical purposes
	Return a string of size random bytes suitable for cryptographic use.
	This function returns random bytes from an OS-specific randomness source. The returned data should be unpredictable enough for cryptographic applications, though its exact quality depends on the OS implementation.
	"""
	#uuid.uuid4() - implemented return UUID(bytes=os.urandom(16), version=4).hex
	# we will pass the size also instead of cutting the screen

	# UUID class needs 16 char bytes or it will raise ValueError: bytes is not a 16-char string
	bytess = os.urandom(16)
	randomString = UUID(bytes=bytess, version=4).hex
	

	if 'number' in filters:
		randomString = str(int(randomString,16))
	else:
		randomString = randomString.upper()
	
	randomString  = randomString[0:stringLength]

	return randomString

def generateCryptographicallySecureRandomString(stringLength=10,filters=[]):
	"""Generate a random string in a UUID fromat which is crytographically secure and random"""
	#generateCryptographicallySecureRandomString(stringLength=10,filters=[]):
	# uuid.uuid4() returns UUID(bytes=os.urandom(16), version=4)
	#randomString = uuid.uuid4().hex
	#os.urandom(size)
	"""
	class secrets.SystemRandom
	A class for generating random numbers using the highest-quality sources provided by the operating system. See random.SystemRandom for additional details.
	"""
	"""
	 import os

	 rand = int(os.urandom(4).encode('hex'), 16)
	 # You can then 'cycle' it against the length.
	 rand_char = chars_list[rand % 80] # or maybe '% len(chars_list)'
	"""
	"""
	If you need it for crypto purposes, use random.SystemRandom().randint(a, b), which makes use of os.urandom().
	"""
	# for reproducable classs use random and randome.seed()
	"""
	os.urandom(size) use system entropy to generate random string useful to cryptographical purposes
	Return a string of size random bytes suitable for cryptographic use.
	This function returns random bytes from an OS-specific randomness source. The returned data should be unpredictable enough for cryptographic applications, though its exact quality depends on the OS implementation.
	"""
	#uuid.uuid4() - implemented return UUID(bytes=os.urandom(16), version=4).hex
	# we will pass the size also instead of cutting the screen

	# UUID class needs 16 char bytes or it will raise ValueError: bytes is not a 16-char string
	bytess = os.urandom(16)
	randomString = UUID(bytes=bytess, version=4).hex
	

	if 'number' in filters:
		randomString = str(int(randomString,16))
	else:
		randomString = randomString.upper()
	
	randomString  = randomString[0:stringLength]

	return randomString
