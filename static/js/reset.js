$(document).ready(function() {
	
	
	$('#signupSubmit').on('click', function(e) {

		e.preventDefault();
		var email = $('#email').val();
		
		
		
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
		
		$.ajax({
					method: "PUT",
					url: '/email',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'email': email}),
					dataType: "json",
					success: function(data) {
						
						$('#msg').html('<span style="color: green; padding-left: 85px;"> Please Check your inbox</span>');
						
					},statusCode: {
						400: function() {
							var delayInMilliseconds = 800;
							$('#msg').html('<span style="color: red; padding-left: 85px;"> Please Login</span>');
							setTimeout(function() {
							window.location.href = '/';
						}, delayInMilliseconds);
						},
						409 : function() {
							$('#msg').html('<span style="color: red; padding-left: 85px;">You are already registered user</span>');
						}
					},
					error: function(err) {
						log(err);
					}
				});
			
	});
});