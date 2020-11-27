import argparse
import csv
import os
import sys

parser = argparse.ArgumentParser(description='TWA Simulator')
parser.add_argument('program_filename', metavar='program_filename', type=str, nargs=1,
                    help='State machine CSV filename')
parser.add_argument('inputs_filename', metavar='inputs_filename', type=str, nargs=1,
                    help='Filename of txt file containing sample inputs')
parser.add_argument('--debug', dest='debug_mode', action='store_true',
                    help='show debug messages (default is false)')

args = parser.parse_args()
program_filename = args.program_filename[0]
inputs_filename = args.inputs_filename[0]
debug_mode = args.debug_mode

"""
Created on Sat Nov 7 15:04:30 2020

@author: ianona
"""

class StateMachine:
	def __init__(self, states):
		self.states = states

	def eval(self, test):
		# skip the first hashtag
		# fix code here to skip leading hashtags
		self.arrow = 1

		# assumption: state 1 is starting state
		self.currentState = 1
		while self.states[self.currentState].getMove() != 'accept' and self.states[self.currentState].getMove() != 'reject':
			move = ''
			move += 'Currently at state ' + str(self.currentState)

			char = test[self.arrow]
			transition = self.states[self.currentState].getTransition(char)
			self.currentState = int(transition)

			move += '. Transitioning to state ' + str(transition) + ' on input ' + char
			if (self.states[self.currentState].getMove() == 'right' or self.states[self.currentState].getMove() == 'left'):
				move += '. Moving arrow head to the ' + self.states[self.currentState].getMove()
			else:
				move += '. Reached terminal state'

			if debug_mode:
				print(move)

			if self.states[self.currentState].getMove() == 'right':
				self.arrow += 1
			elif self.states[self.currentState].getMove() == 'left':
				self.arrow -= 1


		print(self.states[self.currentState].getMove().upper())

class State:
	def __init__(self, sid, move):
		self.sid = sid
		self.move = move
		self.transitions = {}

	def addTransition(self, transition):
		self.transitions[transition[0]] = int(transition[1])

	def getTransition(self, symbol):
		return self.transitions[symbol]

	def getMove(self):
		return self.move

	def __str__(self):
		return (self.move,self.transitions)

	def __repr__(self):
		return self.move + "-"+str(self.transitions)

if __name__ == "__main__":
	with open(program_filename, encoding='utf-8-sig') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		states = {}

		print("Loading machine...")
		for row in csv_reader:
			# print(row)
			sid = int(row[0])
			move = row[1]
			if sid not in states:
				states[sid] = State(sid,move)
			for index in range(2,len(row)):
				transition = row[index]
				if transition != '':
					transition = transition.split(',')
					states[sid].addTransition(transition)
			line_count += 1
		print(f'TWA loaded. Processed {line_count} lines.')

# print(states)
sm = StateMachine(states)

filepath = inputs_filename
with open(filepath) as fp:
	line = fp.readline()
	cnt = 1
	print("Starting tests...")
	print('--------------------------')
	while line:
		print("Line {}: {}".format(cnt, line.strip()))
		sm.eval(line.strip())
		print('--------')
		line = fp.readline()
		cnt += 1
	print("Tests finished! Program terminating...")







