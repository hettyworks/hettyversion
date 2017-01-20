$(document).ready(function() {
	$('a.lt').click(function(e) {
		e.preventDefault();
		$.ajax(this.href, {
			type: 'POST',
			success: function(data) {
				console.log(data);
			},
			error: function(data) {
				console.error(data);
			}
		})
	});
});