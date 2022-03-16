$(document).ready(function() {
	$('#signupSubmit').on('click', function(e) {
		e.preventDefault();
		
		var vnum = $('#vnum').val();
		var vuse = $('#vuse').val();
		var vavail = $('#vavail').val();
		var hname = $('#edit').val();
		
		
		$.ajax({
					method: "PUT",
					url: '/edit',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'vnum': vnum, 'vuse': vuse, 'vavail': vavail, 'hname': hname}),
					dataType: "json",
					success: function(data) {
						var delayInMilliseconds = 900;
                        $('#msg').html('<span style="color: red; padding-left: 85px; display: block;">Updation Completed!!</span>');
						setTimeout(function() {
							window.location.href = '/';
						}, delayInMilliseconds);
						  
					},statusCode: {
						400: function() {
							$('#msg').html('<span style="color: red; padding-left: 85px; display: block;">Bad request parameters</span>');
						},
						409 : function() {
							$('#msg').html('<span style="color: red; padding-left: 85px; display: block;">You are already registered user</span>');
						}
					},
					error: function(err) {
						log(err);
					}
				});
			
	});
});