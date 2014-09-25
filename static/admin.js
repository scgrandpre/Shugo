$(function() {
	$('input.checkbox').change(function() {
		$e = $(this);
		$.post("/admin/cell/" + $e.attr('id') + "?checked=" + $e.is(":checked"));
	});

	$('.set-game').click(function() {
		name = $('.game-name').val();
		$.post("/admin/set_game/" + name);
	});


	$('.clear').click(function() {
		$('input').attr('checked', false);
		$.post("/admin/clear");
	});
});
