$(document).ready(function() {
	$('#signupSubmit').on('click', function(e) {
		e.preventDefault();
		
		
		var hname = $('#hname').val();
		var haddress = $('#haddress').val();
		var lat =  $('#latp').val();
		var lng =  $('#lngp').val();
		var hdistrict = $('#hdistrict').val();
		var hpincode = $('#hpincode').val();
		var hphno = $('#hphno').val();
		var hemail = $('#hemail').val();
		var vnum = $('#vnum').val();
		var vuse = $('#vuse').val();
		var vavail = $('#vavail').val();
		var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/i;
		
		if(hemail != "") {
			if(!regex.test(hemail)) {
				$('#msg').html('<span style="color: red;">Invalid email address</span>');
			} else {
				$.ajax({
					method: "POST",
					url: '/signup1',
					contentType: 'application/json;charset=UTF-8',
					data: JSON.stringify({'hname':hname, 'haddress': haddress,  'lat':lat, 'lng':lng, 'hdistrict': hdistrict, 'hpincode': hpincode, 'hphno': hphno, 'hemail': hemail, 'vnum': vnum, 'vuse': vuse, 'vavail': vavail  }),
					dataType: "json",
					success: function(data) {
						var delayInMilliseconds = 900;
						$('#msg').html('<span style="color: red; padding-left: 85px; display: block;">Registered Successfully, Please Login</span>');

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
						console.log(err);
					}
				});
			}
		} else {
			$('#msg').html('<span style="color: red;">All fields are required</span>');
		}
	});
	$('#logout').on('click', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: '/logout1',
			dataType: "json",
			success: function(data) {
				localStorage.setItem('loggedin', 0);
				
				window.alert("Registered Successfully");
				if (data.redirect) {
					window.location.href = data.redirect;
				}
			},
			error: function(err) {
				log(err);
			}
		});
	});
});