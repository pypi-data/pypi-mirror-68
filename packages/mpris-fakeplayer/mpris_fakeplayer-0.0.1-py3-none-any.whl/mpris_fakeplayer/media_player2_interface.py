
from dbus_next.constants import (
	PropertyAccess
)
from dbus_next.service import (
	ServiceInterface,
	method,
	dbus_property
)

class MediaPlayer2Interface(ServiceInterface):

	INTERFACE = 'org.mpris.MediaPlayer2'

	def __init__(self):
		super().__init__(self.__class__.INTERFACE)

	@method()
	def Raise(self):
		pass

	@method()
	def Quite(self):
		pass

	@dbus_property(PropertyAccess.READ)
	def Identity(self) -> 's':
		return 'FakePlayer'
