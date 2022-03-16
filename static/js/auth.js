$(document).ready(function() {
	
	var isLoggedIn = localStorage.getItem('loggedin');
	
	if(isLoggedIn == 1) {
		$('#sign').hide();
		$('#loginform').hide();
		$('#homeform').show();
		$('#logoff').hide();
	} else {
		$('#sign').show();
		$('#logoff').hide();
	}
	
	$('#loginSubmit').on('click', function(e) {
		e.preventDefault();
		
		var email = $('#email').val();
		var pwd = $('#password').val();
		
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
		
		if(email != "" && pwd != "" ) {
			if(!regex.test(email)) {
				$('#msg').html('<span style="color: red;padding-left: 85px">INVALID EMAIL ADDRESS</span>');
			} else {
				$.ajax({
					
					method: "POST",
					url: '/login',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'username': email, 'password': pwd}),
					dataType: "json",
					
					success: function(data) {
						
						if (data.redirect) {
							window.location.href = data.redirect;
						}
					},
					statusCode: {
						400: function() {
							$('#msg').html('<span style="color: red; display: block; padding-left: 85px">Invalid credentials</span>');
						}
					},
					error: function(err) {
						log(err);
					}
				});
			}
		} else {
			$('#msg').html('<span style="color: red; display: block; padding-left: 80px">Invalid username and password</span>');
		}
	});
	
	$('#logout').on('click', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: '/logout',
			dataType: "json",
			success: function(data) {
				localStorage.setItem('loggedin', 0);
				$('#sign').show();
				$('#logoff').hide();
				$('#msg').html('<span style="color: green;">You are logged off</span>');
			},
			error: function(err) {
				log(err);
			}
		});
	});
});