import os
import random

import cherrypy
import pprint
pp = pprint.PrettyPrinter(indent=4)

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

class Battlesnake(object):
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def index(self):
		# This function is called when you register your Battlesnake on play.battlesnake.com
		# It controls your Battlesnake appearance and author permissions.
		# TIP: If you open your Battlesnake URL in browser you should see this data
		return {
			"apiversion": "1",
			"author": "Alistair Hewitt, Djan Tanova",  # TODO: Your Battlesnake Username
			"color": "#ff00ff",  # TODO: Personalize
			"head": "gamer",  # TODO: Personalize
			"tail": "default",  # TODO: Personalize
		}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def start(self):
		# This function is called everytime your snake is entered into a game.
		# cherrypy.request.json contains information about the game that's about to be played.
		data = cherrypy.request.json

		print("START")
		return "ok"

	@cherrypy.expose
	@cherrypy.tools.json_in()
	@cherrypy.tools.json_out()
	def move(self):
		# This function is called on every turn of a game. It's how your snake decides where to move.
		# Valid moves are "up", "down", "left", or "right".
		# TODO: Use the information in cherrypy.request.json to decide your next move.
		data = cherrypy.request.json
		pp.pprint(data)

		# Dimensions of board
		height = data['board']['height']
		width = data['board']['width']

		# Position of head
		head = data['you']['head']
		# List of positions of body
		body = data['you']['body']

		possible_moves = ["up", "down", "left", "right"]
		print(possible_moves)
		# Position of head if snake moves in direction
		def giveNextMove(head):
			upNext = head.copy(); upNext['y'] += 1
			downNext = head.copy(); downNext['y'] -= 1
			leftNext = head.copy(); leftNext['x'] -= 1
			rightNext = head.copy(); rightNext['x'] += 1

			nextPos = {"up":upNext, "down":downNext, "left":leftNext, "right":rightNext}
			return nextPos

		# print(head); print(upNext); print(downNext); print(leftNext); print(rightNext)

		def deleteMoves(nextPos,body, nextPossibleMoves):

			# If move would result in collision with self, remove from possible moves
			if (nextPos["up"] in body) or (nextPos["up"]['y'] >= height):
				nextPossibleMoves.remove('up')
			if (nextPos["down"] in body) or (nextPos["down"]['y'] < 0):
				nextPossibleMoves.remove('down')
			if (nextPos["left"] in body) or (nextPos["left"]['x'] < 0):
				nextPossibleMoves.remove('left')
			if (nextPos["right"] in body) or (nextPos["right"]['x'] >= width):
				nextPossibleMoves.remove('right')
			moveCount = len(nextPossibleMoves)

			return moveCount

		nextPos = giveNextMove(head)
		twoStepPos = twoStep(head)
		deleteMoves(nextPos, body, possible_moves)

		print(possible_moves)
		for newHead in nextPos:
	  		twoStep = giveNextMove(nextPos[newHead])
			nextPossibleMoves = possible_moves
	  		if deleteMoves(twoStep, body, nextPossibleMoves) < 0:
				possible_moves.remove(newHead)

    	# Checks for food in the next moves
		foodMoves = []
		for nextMove in nextPos:
			if nextPos[nextMove] in data['board']['food']:
				foodMoves.append(nextMove)

		if foodMoves != []:
			move = random.choice(foodMoves)
		else:
			move = random.choice(possible_moves)

		print(f"MOVE: {move}")
		return {"move": move}

	@cherrypy.expose
	@cherrypy.tools.json_in()
	def end(self):
		# This function is called when a game your snake was in ends.
		# It's purely for informational purposes, you don't have to make any decisions here.
		data = cherrypy.request.json

		print("END")
		return "ok"


if __name__ == "__main__":
	server = Battlesnake()
	cherrypy.config.update({"server.socket_host": "0.0.0.0"})
	cherrypy.config.update(
		{"server.socket_port": int(os.environ.get("PORT", "8080")),}
	)
	print("Starting Battlesnake Server...")
	cherrypy.quickstart(server)
