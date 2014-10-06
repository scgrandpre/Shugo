print "hello world"
import random
import os
import urlparse
import redis
url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL', 'http://localhost:6379'))
print url, url.hostname, url.port
r = redis.Redis(host=url.hostname, port=url.port, password=url.password)


names_list = [
"1st Kill",
"2nd Kill",
"3rd Kill",
"5th Kill",
"7th Kill",
"9th Kill",
"10th Kill",
"11th Kill",
"12th Kill",
"14th Kill",
"15th Kill",
"16th Kill",
"17th Kill",
"18th Kill",
"19th Kill",
"20th Kill",
"1st Ace",
"2nd Ace",
"3rd Ace",
"4th Ace",
"5th Ace",
"6th Ace",
"7th Ace",
"1st Block",
"2nd Block",
"3rd Block",
"4th Block",
"5th Block",
"6th Block",
"7th Block",
"10th Point",
"12th Point",
"14th Point",
"15th Point",
"16th Point",
"17th Point",
"18th Point",
"19th Point",
"20th Point",
"21st Point",
"22nd Point",
"23rd Point",
"24th Point",
"SHU Win",
]
globals = {"seed": random.randint(0, 10000), "cell_checked": {}, "won": False, "current_game": "unnamed"};


def make_cells(names):
	return [{"cell_id": name.replace(' ', '-').lower(), "name": name} for name in names]

def all_cells():
	return make_cells(names_list + [str(x) for x in range(46, 76)])

def generate_board(seed):
	s = globals["seed"] + int(seed)
	random.seed(s)
	shuffled_list = make_cells(names_list)
	random.shuffle(shuffled_list)

	Gs = make_cells(str(x) for x in range(46, 61))
	random.shuffle(Gs)
	Os = make_cells(str(x) for x in range(61, 76))
	random.shuffle(Os)
	
	board = [shuffled_list[x*5:x*5+5] for x in xrange(0,5)]
	board[2][2] = {"cell_id": "free", "name": "FREE"}
	return board

from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)
app.debug = True

@app.route("/join")
def join_default():
	return render_template('join.html', game=globals["current_game"])

@app.route("/join/<string:game>")
def join(game):
	return render_template('join.html', game=game)

@app.route("/play")
def play():
	game = request.args.get("game", "default game").replace(' ', '_')
	name = request.args.get("name", "default name")

	r.sadd("game:" + game, name)

	seed = request.cookies.get('seed', random.randint(0, 10000))
	resp = make_response(render_template('card.html',
		board=generate_board(seed), game_id=globals["seed"]))
	resp.set_cookie('seed', str(seed))
	return resp

@app.route("/win", methods=['POST'])
def win():
	won = not globals["won"]
	globals["won"] = True
	return jsonify(won=won)


@app.route("/checked_cells")
def checked_cells():
	return jsonify(game_id=globals["seed"], cells=globals["cell_checked"])

@app.route("/admin")
def admin():
	return render_template('admin.html', cells=all_cells(), cells_checked=globals["cell_checked"], game=globals["current_game"])

@app.route("/admin/newgame")
def newgame():
	return render_template('newgame.html')

@app.route("/admin/newgame/<string:game_name>", methods=['POST'])
def create_new_game(game_name):
	print game_name
	return render_template('newgame.html')

@app.route("/admin/clear", methods=['POST'])
def clear():
	globals["cell_checked"] = {}
	globals["seed"] = random.randint(0,10000)
	globals["won"] = False
	return jsonify(**globals["cell_checked"])

@app.route("/admin/cell/<string:cell_id>", methods=['POST'])
def toggle_cell(cell_id):
	globals["cell_checked"][cell_id] = request.args.get("checked") != "false"
	return jsonify(**globals["cell_checked"])

@app.route("/admin/set_game/<string:game_name>", methods=['POST'])
def name_game(game_name):
	globals["current_game"] = game_name
	return jsonify(ok=True)

@app.route("/admin/games")
def admin_games():
	return make_response(
			"<br>".join(game[len("game:"):] + ": " + ", ".join(r.smembers(game)) 
				for game in r.keys("game:*")))

if __name__ == "__main__":
    app.run()
