$(function() {
	var hasCells = false;
	var at = function(row, col) {
		return board[row][col];
	}
	var check_victory = function(cells) {
		finished = _.any([0,1,2,3,4], function(x) {
			return _.all([0,1,2,3,4], function(y) {
				return cells[at(x, y).cell_id];
			}) || _.all([0,1,2,3,4], function(y) {
				return cells[at(y, x).cell_id];
			});
		});

		downDiagonal = _.all([0,1,2,3,4], function(x) {
			return  cells[at(x, x).cell_id];
		});

		upDiagonal = _.all([0,1,2,3,4], function(x) {
			return  cells[at(x, 4 - x).cell_id];
		});

		if (finished || downDiagonal || upDiagonal) {
			console.log("you win!");
		}
	};
	var poll = function() {
		$.get("/checked_cells", function(cells) {
			if (_.keys(cells).length == 0) {
				if (hasCells) {
					window.location.reload(true);
				}
			} else {
				hasCells = true;
			}
			for (var cell_id in cells) {
				$('#cell-' + cell_id).toggleClass('checked', cells[cell_id]);
			}
			check_victory(cells);
		});
	}
	setInterval(poll, 1000);
});