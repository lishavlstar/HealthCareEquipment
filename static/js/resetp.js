$(document).ready(function() {
	$('#signupSubmit').on('click', function(e) {
		e.preventDefault();
		
		var email = $('#email').val();
		var pwd = $('#password').val();
		var cnfpwd = $('#cnfpassword').val();
		
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
		
		if(email != "" && pwd != "" && cnfpwd != "") {
			if(pwd != cnfpwd) {
				$('#msg').html('<span style="color: red;">Password and confirm password must match</span>');
			} else if(!regex.test(email)) {
				$('#msg').html('<span style="color: red;">Invalid email address</span>');
			} else {
				$.ajax({
					method: "PUT",
					url: '/passwd',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'username': email, 'password': pwd}),
					dataType: "json",
					success: function(data) {
                        window.alert("Password Reseted");
						if (data.redirect) {
							window.location.href = data.redirect;
						}
						
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
			}
		} else {
			$('#msg').html('<span style="color: red;">All fields are required</span>');
		}
	});
});