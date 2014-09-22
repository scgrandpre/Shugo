$(function() {
	$('.submit').click(function() {
		game_name = $('.name').val();
		$.post("/admin/newgame/" + game_name, function(res) {
			console.log(res);
		});
	});
});
