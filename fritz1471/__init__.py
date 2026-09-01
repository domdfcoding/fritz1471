#!/usr/bin/env python3
#
#  __init__.py
"""
1471-esque implementation for Fritz!Boxes.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import traceback
from contextlib import suppress
from typing import Optional

# 3rd party
import local_ip_address
from fritzconnection.lib.fritzcall import FritzCall
from pyVoIP.VoIP.VoIP import InvalidStateError, VoIPCall, VoIPPhone

# this package
from fritz1471.fritz import get_last_call
from fritz1471.sip import play_wav
from fritz1471.tts import tts

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["Fritz1471"]


class Fritz1471:
	"""
	1471-esque implementation for Fritz!Boxes.

	:param sip_username: Username for the SIP account.
	:param sip_password: Password for the SIP account.
	:param fritzbox_username: Username for the Fritz!Box. May be an account with restricted capabilities.
	:param fritzbox_password: Password for the Fritz!Box user.
	:param fritzbox_ip: LAN IP address of the Fritz!Box.
	:param local_sip_port: Port on the local machine to use for SIP.
	:param sip_listen_address: IP address to listen for SIP traffic on. Defaults to LAN IPv4 address. ``0.0.0.0`` appears not to work.
	"""

	def __init__(
			self,
			sip_username: str,
			sip_password: str,
			fritzbox_username: str,
			fritzbox_password: str,
			fritzbox_ip: str = "192.168.0.1",
			local_sip_port: int = 5060,
			sip_listen_address: Optional[str] = None,
			):
		self.sip_username = sip_username
		self.sip_password = sip_password
		self.fritzbox_username = fritzbox_username
		self.fritzbox_password = fritzbox_password
		self.fritzbox_ip = fritzbox_ip

		self._fc = FritzCall(
				address=fritzbox_ip,
				user=fritzbox_username,
				password=fritzbox_password,
				)

		if sip_listen_address is None:
			sip_listen_address = str(local_ip_address.local_ip())

		self._phone = VoIPPhone(
				fritzbox_ip,
				5060,
				sip_username,
				sip_password,
				callCallback=self.answer,
				sipPort=local_sip_port,
				myIP=sip_listen_address,
				)

	def answer(self, call: VoIPCall) -> None:
		"""
		Callback for incoming calls.

		:param call:
		"""

		print(call)
		try:

			msg = get_last_call(self._fc)
			data, duration = tts(msg)

			call.answer()
			play_wav(call, data, duration)
		except (Exception, InvalidStateError):
			traceback.print_exc()

		with suppress(InvalidStateError):
			call.hangup()

	def run(self) -> None:
		print(f"SIP client listening on {self._phone.sip.myIP}:{self._phone.sip.myPort}")

		try:
			self._phone.start()
			input("Press enter to disable the phone")
			self._phone.stop()
		except KeyboardInterrupt:
			self._phone.stop()
