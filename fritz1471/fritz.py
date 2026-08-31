#!/usr/bin/env python3
#
#  fritz.py
"""
Fritz!Box interface.
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
import datetime

# 3rd party
import inflect
from fritzconnection.lib.fritzcall import FritzCall

__all__ = ["get_last_call"]

ordinal = inflect.engine().ordinal


def get_last_call(fc: FritzCall) -> str:

	today = datetime.date.today()
	yesterday = today - datetime.timedelta(days=1)
	# for call in [*fc.get_missed_calls(), *fc.get_received_calls()]:
	for call in fc.get_calls(num=4):
		# print(call)
		# print(dir(call))
		# print(call.__dict__)
		if call.type == 3:
			continue
		# call_dt = datetime.datetime.strptime("%d.%m.%y")
		call_dt: datetime.datetime = call.date
		call_date = call_dt.date()
		call_time = call_dt.time()
		if call_date == today:
			date_str = "today"
		elif call_date == yesterday:
			date_str = "yesterday"
		else:
			date_str = f"{call_date.strftime('%A')}, {ordinal(call_date.day)} {call_date.strftime('%B')}"
			# TODO: year if not current year
		time_str = call_time.strftime("%-I %M %p")
		caller: str = call.Caller
		assert caller.isnumeric()
		phone_number = ' '.join(caller)
		msg = f"Telephone number {phone_number} called {date_str} at {time_str}".format_map(call.__dict__)
		return msg

	return "No calls received."
