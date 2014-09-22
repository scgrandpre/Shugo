$(function() {
	$('.submit').click(function() {
		name = $('.name').val();
		game = $('.game').val();
		window.location.href = "/play?name=" + encodeURIComponent(name) + "&game=" + encodeURIComponent(game);
	});
});
