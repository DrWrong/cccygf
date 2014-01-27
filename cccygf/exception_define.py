class NotEnoughProduct(Exception):
	"""docstring for NotEnoughProduct"""
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return self.value
class ProductOffline(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return self.value
