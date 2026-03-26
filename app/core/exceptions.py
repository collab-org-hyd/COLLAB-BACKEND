class ResourceNotFoundError(Exception):
	"""Exception raised when a requested resource is not found."""
	pass

class BadRequestError(Exception):
	"""Exception raised for invalid requests."""
	pass

class AuthenticationError(Exception):
	"""Exception raised for authentication failures."""
	pass
