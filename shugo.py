print "hello world"
import random

names_list = [
"Kill 1",
"Kill 2",
"Kill 3",
"Kill 4",
"Kill 5",
"Kill 6",
"Kill 7",
"Kill 8",
"Kill 9",
"Kill 10",
"Kill 11",
"Kill 12",
"Kill 13",
"Kill 14",
"Kill 15",
"Ace 1",
"Ace 2",
"Ace 3",
"Block 1",
"Block 2",
"Block 3",
"SHU Point 1",
"SHU Point 2",
"SHU Point 3",
"SHU Point 4",
"SHU Point 5",
"SHU Point 6",
"SHU Point 7",
"SHU Point 8",
"SHU Point 9",
"SHU Point 10",
"SHU Point 11",
"SHU Point 12",
"SHU Point 13",
"SHU Point 14",
"SHU Point 15",
"SHU Point 16",
"SHU Point 17",
"SHU Point 18",
"SHU Point 19",
"SHU Point 20",
"SHU Point 21",
"SHU Point 22",
"SHU Point 23",
"SHU Point 24",
"SHU Win",
]
globals = {"seed": random.randint(0, 10000), "cell_checked": {}};



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
	
	return [shuffled_list[x*5:x*5+5] for x in xrange(0,5)]

from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	seed = request.cookies.get('seed', random.randint(0, 10000))
	resp = make_response(render_template('card.html', board=generate_board(seed)))
	resp.set_cookie('seed', str(seed))
	return resp

@app.route("/checked_cells")
def checked_cells():
	return jsonify(**globals["cell_checked"])

@app.route("/admin")
def admin():
	return render_template('admin.html', cells=all_cells(), cells_checked=globals["cell_checked"])

@app.route("/admin/clear", methods=['POST'])
def clear():
	globals["cell_checked"] = {}
	globals["seed"] = random.randint(0,10000)
	return jsonify(**globals["cell_checked"])

@app.route("/admin/cell/<string:cell_id>", methods=['POST'])
def toggle_cell(cell_id):
	globals["cell_checked"][cell_id] = request.args.get("checked") != "false"
	return jsonify(**globals["cell_checked"])


if __name__ == "__main__":
    app.run()