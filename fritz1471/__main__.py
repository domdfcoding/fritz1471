#!/usr/bin/env python3
#
#  __main__.py
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
from typing import Optional

# 3rd party
from click import argument
from consolekit import click_command, option
from consolekit.options import auto_default_option
from dotenv import load_dotenv

__all__ = ["main"]

load_dotenv()  # reads variables from a .env file and sets them in os.environ


@argument("sip_username", envvar="SIP_USERNAME")  # "Username for the SIP account."
@argument("sip_password", envvar="SIP_PASSWORD")  # "sip_password: Password for the SIP account."
# "fritzbox_username: Username for the Fritz!Box. May be an account with restricted capabilities."
@argument("fritzbox_username", envvar="FRITZBOX_USERNAME")
@argument("fritzbox_password", envvar="FRITZBOX_PASSWORD")  # "fritzbox_password: Password for the Fritz!Box user."
@auto_default_option("--fritzbox-ip", envvar="FRITZBOX_IP", help="fritzbox_ip: LAN IP address of the Fritz!Box.")
@auto_default_option(
		"--local-sip-port",
		envvar="LOCAL_SIP_PORT",
		help="local_sip_port: Port on the local machine to use for SIP.",
		type=int,
		)
@option(
		"--sip-listen-address",
		envvar="SIP_LISTEN_ADDRESS",
		help="sip_listen_address: IP address to listen for SIP traffic on.",
		)
@click_command()
def main(
		sip_username: str,
		sip_password: str,
		fritzbox_username: str,
		fritzbox_password: str,
		fritzbox_ip: str = "192.168.0.1",
		local_sip_port: int = 5060,
		sip_listen_address: Optional[str] = None,
		):

	# this package
	from fritz1471 import Fritz1471

	Fritz1471(
			sip_username=sip_username,
			sip_password=sip_password,
			fritzbox_username=fritzbox_username,
			fritzbox_password=fritzbox_password,
			fritzbox_ip=fritzbox_ip,
			local_sip_port=local_sip_port,
			sip_listen_address=sip_listen_address,
			).run()


if __name__ == "__main__":
	main()
