# jslint.py - sublimelint package for checking Javascript files

import subprocess
import os
import sublime

def check(codeString, filename):
	info = None
	base = os.path.dirname(os.path.dirname(os.path.abspath( __file__ )))
	if os.name == 'nt':
		info = subprocess.STARTUPINFO()
		info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		info.wShowWindow = subprocess.SW_HIDE

	s = sublime.load_settings("Base File.sublime-settings")
	jsl = s.get("jslint_path", "/usr/local/bin/jsl")

	process = subprocess.Popen((jsl, '-conf', os.path.join(base, 'jslint', 'config'), '-nocontext', '-nosummary', '-nofilelisting', '-nologo', '-stdin'), stdin=subprocess.PIPE, stdout=subprocess.PIPE, startupinfo=info)
	result = process.communicate(codeString)[0]
	print result
	return result

# start sublimelint jslint plugin
import re
__all__ = ['run', 'language']
language = 'JavaScript'

def run(code, view, filename='untitled'):
	errors = check(code, filename)

	lines = set()
	underline = [] # leave this here for compatibility with original plugin

	errorMessages = {}
	def addMessage(lineno, message):
		message = str(message)
		if lineno in errorMessages:
			errorMessages[lineno].append(message)
		else:
			errorMessages[lineno] = [message]

	for line in errors.splitlines():
		match = re.search('\((?P<line>\d*)\): ([a-zA-Z ]*): (?P<error>.*)', line)
		if match:
			error, line = match.group('error'), match.group('line')

			lineno = int(line) - 1
			lines.add(lineno)
			addMessage(lineno, error)

	return underline, lines, errorMessages, True
