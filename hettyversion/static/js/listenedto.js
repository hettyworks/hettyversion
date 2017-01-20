$(document).ready(function() {
	$('a.lt').click(function(e) {
		e.preventDefault();
		var lt = $(this);
		data = {
			version_id: lt.data('version_id'),
			listened_to: lt.data('listened_to')
		};
		$.ajax(this.href, {
			type: 'POST',
			data: JSON.stringify(data, null, '\t'),
			contentType: 'application/json;charset=UTF-8',
			success: function(data) {
				lt.data('listened_to', data.listened_to);
				lt.removeClass('lt-false');
				lt.removeClass('lt-true');
				lt.addClass('lt-' + data.listened_to);
			},
			error: function(data) {
				if(data.status == 403) {
					alert('You must log in to check off versions.');
				}
			}
		})
	});
});