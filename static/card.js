$(function() {
	var at = function(row, col) {
		return $($($('tbody').children()[row]).children()[col]).is('.checked');
	};
	var check_victory = function() {
		finished = _.any([0,1,2,3,4], function(x) {
			return _.all([0,1,2,3,4], function(y) {
				return at(x, y);
			}) || _.all([0,1,2,3,4], function(y) {
				return at(y, x);
			});
		});

		downDiagonal = _.all([0,1,2,3,4], function(x) {
			return  at(x, x);
		});

		upDiagonal = _.all([0,1,2,3,4], function(x) {
			return  at(x, 4 - x);
		});

		if (finished || downDiagonal || upDiagonal) {
			$.post("/win", function(res) {
				if (res.won) {
					alert("Congratulations! You got shugo!");
				} else {
					alert("So Close! But somebody else already got shugo.");
				}
			});
		}
	};

	$('body').on('click', ".bingo-cell.blink", function() {
		$(this).toggleClass('checked', true);
		check_victory();
	});

	var poll = function() {
		$.get("/checked_cells", function(data) {
			if ($('.game_id').val() !== "" + data.game_id) {
				window.location.reload(true);
			} 
			for (var cell_id in data.cells) {
				$('#cell-' + cell_id).toggleClass('blink', data.cells[cell_id]);
				if (!data.cells[cell_id]) {
					$('#cell-' + cell_id).toggleClass('checked', false);
				}
			}
		});
	};
	setInterval(poll, 1000);
});
