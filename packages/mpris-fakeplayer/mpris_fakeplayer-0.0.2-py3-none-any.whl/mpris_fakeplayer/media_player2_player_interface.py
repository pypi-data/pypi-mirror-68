
from dbus_next.constants import (
	PropertyAccess
)
from dbus_next.service import (
	ServiceInterface,
	method,
	dbus_property
)

class MediaPlayer2PlayerInterface(ServiceInterface):

	INTERFACE = 'org.mpris.MediaPlayer2.Player'

	STATUS_PLAYING = 'Playing'
	STATUS_STOPPED = 'Stopped'

	def __init__(self):
		super().__init__(self.__class__.INTERFACE)

		self.status = self.__class__.STATUS_PLAYING

	@method()
	def Stop(self):
		self.status = self.__class__.STATUS_STOPPED

		self.emit_properties_changed({
			'PlaybackStatus': self.PlaybackStatus
		})

	@dbus_property(PropertyAccess.READ)
	def PlaybackStatus(self) -> 's':
		return self.status
