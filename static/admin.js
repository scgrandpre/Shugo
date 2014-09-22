$(function() {
	$('input').change(function() {
		$e = $(this);
		$.post("/admin/cell/" + $e.attr('id') + "?checked=" + $e.is(":checked"));
	});

	$('.clear').click(function() {
		$('input').attr('checked', false);
		$.post("/admin/clear");
	});
});
