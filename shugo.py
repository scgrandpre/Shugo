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
"SHU Point 5",
"SHU Point 10",
"SHU Point 15",
"SHU Point 20",
"SHU Win",
]
cell_checked = {};

print ['G' + str(x) for x in range(61,76)]


def make_cells(names):
	return [{"cell_id": name.replace(' ', '-').lower(), "name": name} for name in names]

def all_cells():
	return make_cells(names_list + [str(x) for x in range(46, 76)])

def generate_board():
	shuffled_list = make_cells(names_list)
	random.shuffle(shuffled_list)

	Gs = make_cells(str(x) for x in range(46, 61))
	random.shuffle(Gs)
	Os = make_cells(str(x) for x in range(61, 76))
	random.shuffle(Os)
	

	return [shuffled_list[x*3:x*3+3] + [Gs[x], Os[x]] for x in xrange(0,5)]

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
	print generate_board()
	return render_template('card.html', board=generate_board())

@app.route("/checked_cells")
def checked_cells():
	return jsonify(**cell_checked)

@app.route("/admin")
def admin():
	return render_template('admin.html', cells=all_cells(), cells_checked=cell_checked)

@app.route("/admin/clear", methods=['POST'])
def clear(cell_id):
	cell_checked = {}
	return jsonify(**cell_checked)

@app.route("/admin/cell/<string:cell_id>", methods=['POST'])
def toggle_cell(cell_id):
	cell_checked[cell_id] = request.args.get("checked") != "false"
	return jsonify(**cell_checked)


if __name__ == "__main__":
    app.run()