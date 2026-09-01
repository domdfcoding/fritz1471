#!/usr/bin/env python3
#
#  tts.py
"""
Text-to-speech generator.
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
import wave
from io import BytesIO
from typing import Tuple

# 3rd party
from gtts import gTTS  # type: ignore[import-untyped]
from pydub.audio_segment import AudioSegment  # type: ignore[import-untyped]

__all__ = ["tts"]


def tts(msg: str) -> Tuple[bytes, float]:
	"""
	Generate text-to-speech for the given message, as 8-bit mono PCM.

	:param msg:

	:returns: The audio bytes and the duration in seconds.
	"""

	sample_rate = 8000

	mp3_fname = BytesIO()
	wav_fname = BytesIO()

	tts = gTTS(text=msg, lang="en", slow=True, lang_check=True)
	tts.write_to_fp(mp3_fname)
	mp3_fname.flush()
	mp3_fname.seek(0)

	sound = AudioSegment.from_mp3(mp3_fname).set_frame_rate(sample_rate).set_sample_width(1)
	sound.export(wav_fname, format="wav")

	wav_fname.seek(0)

	with wave.open(wav_fname, "rb") as f:
		frames = f.getnframes()
		data = f.readframes(frames)

	return data, (frames / sample_rate)  # frames/sample_rate is the length of the audio in seconds
