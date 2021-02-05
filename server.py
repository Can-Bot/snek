import os
import random

import cherrypy


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
      # This function is called when you register your Battlesnake on play.battlesnake.com
      # It controls your Battlesnake appearance and author permissions.
      # TIP: If you open your Battlesnake URL in browser you should see this data
      return {
        "apiversion": "1",
        "author": "CanBot",  # TODO: Your Battlesnake Username
        "color": "#FF00FF",  # TODO: Personalize
        "head": "gamer",  # TODO: Personalize
        "tail": "tiger-tail",  # TODO: Personalize
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
      snake = data['board']
      print(snake)

		  # List of positions of body
		  body = data['you']['body']
      # Position of head
		  head = data['you']['head']
      
      possible_moves = ["up", "down", "left", "right"]

      # Position of head if snake moves in direction
		  up = head.copy(); up['y'] += 1
		  down = head.copy(); down['y'] -= 1
		  left = head.copy(); left['x'] -= 1
		  right = head.copy(); right['x'] += 1
       
      print(head)
      print(up)
      print(down)
      print(left)
      print(right)

      if (up in body) or (up['y'] >= """y limit"""):
			  possible_moves.remove('up')
	    if (down in body) or (down['y'] < 0):
	  	  possible_moves.remove('down')
	    if (left in body) or (left['x'] < 0):
	  	  possible_moves.remove('left')
	    if (right in body) or (right['x'] >= """x limit"""):
	  	  possible_moves.remove('right')
        
           

      # Choose a random direction to move in
        
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
