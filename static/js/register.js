$(document).ready(function() {
	$('#signupSubmit').on('click', function(e) {
		e.preventDefault();
		
		var name = $('#fullname').val();
		var hname = $('#hname').val();
		var address = $('#address').val();
		var district = $('#district').val();
		var pincode = $('#pincode').val();
		var phno = $('#phno').val();
		var email = $('#email').val();
		var pwd = $('#password').val();
		var cnfpwd = $('#cnfpassword').val();
		
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
		
		if(email != "" && pwd != "" && cnfpwd != "") {
			if(pwd != cnfpwd) {
				$('#msg').html('<span style="color: red; display: block;">Password and confirm password must match</span>');
			} else if(!regex.test(email)) {
				$('#msg').html('<span style="color: red;">Invalid email address</span>');
			} else {
				$.ajax({
					method: "POST",
					url: '/signup',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'name': name, 'hname':hname, 'address': address, 'district': district, 'pincode': pincode, 'phno': phno, 'email': email, 'password': pwd}),
					dataType: "json",
					success: function(data) {
						if (data.redirect) {
							window.location.href = data.redirect;
						}
						
					},statusCode: {
						400: function() {
							$('#msg').html('<span style="color: red; padding-left: 85px;">Bad request parameters</span>');
						},
						409 : function() {
							var delayInMilliseconds = 800;
							$('#msg').html('<span style="color: red; display: block; padding-left: 85px;">You are already registered user, Please Login</span>');
							setTimeout(function() {
							window.location.href = '/';
						}, delayInMilliseconds);
					}
					},
					error: function(err) {
						log(err);
					}
				});
			}
		} else {
			$('#msg').html('<span style="color: red; display: block;">All fields are required</span>');
		}
	});
});