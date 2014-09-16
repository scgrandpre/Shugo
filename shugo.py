print "hello world"
import random

names_list = [
"1st Kill",
"2nd Kill",
"3rd Kill",
"4th Kill",
"5th Kill",
"6th Kill",
"7th Kill",
"8th Kill",
"9th Kill",
"10th Kill",
"11th Kill",
"12th Kill",
"14th Kill",
"15th Kill",
"16th Kill",
"1st Ace",
"2nd Ace",
"3rd Ace",
"1st Block",
"2nd Block",
"3rd Block",
"1st Point",
"2nd Point",
"3rd Point",
"4th Point",
"5th Point",
"6th Point",
"7th Point",
"8th Point",
"9th Point",
"10th Point",
"11th Point",
"12th Point",
"13th Point",
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