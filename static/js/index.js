$(document).ready(function () {
    $('#form2').hide();
    $('#backf').hide();
    $('#form4').hide();
    $('#form6').hide();
    google.maps.event.addDomListener(window, 'load', initMap);
    $('#searchByHospital').on('click', function (e) {
        e.preventDefault();

        var hname = $('#h_name').val();
        
        $.ajax({
            method
            : "GET",
            url: '/searchbyhospital/' + hname,
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            success: function (data) {
                
                $('#customers').hide();
                $('#form2').show();
                $('#form4').show();
                $('#form1').hide();
                $('#form3').hide();
                $('#form5').hide();
                $('#form6').show();
                $('#backf').show();
                $("#hospitalTable tr").remove();
                $("#hospitalTabl tr").remove();
                $("#hospitalTab tr").remove();
                $('#msg').hide();
                $('#head').hide();
                let new1 = "<tr><td>" + data[0].hname + "</td></tr>";

                let new2 = "<tr><tr><td>Hospital Name</td><th>" + data[0].hname + "</th></tr> <tr><td>Total Ventilators</td><th>" + data[0].vnum + "</th></tr><tr><td>Ventilators in Use</td><th>" + data[0].vuse + "</th></tr><tr><td>Available Ventilators</td><<th>" + data[0].vavail + "</th></tr></tr>";
                $("#hospitalTable").append(new2);
                $("#hospitalTabl").append(new1);
                $("#hospitalTab").append(new1);
                google.charts.load("current", {packages:["corechart"]});
                google.charts.setOnLoadCallback(drawpieChart);
                
                num1= data[0].vuse
                num2= data[0].vavail
                num3= data[0].lat
                num4= data[0].lng
                num5= data[0].vnum
                num6= data[0].haddress
                function drawpieChart() {
                   
                    var data = new google.visualization.DataTable();
                    
      data.addColumn('string', 'Topping');
      data.addColumn('number', 'Slices');
          data.addRows([
          
               ['Ventilators in Use', num1 ],
               ['Ventilators Available', num2],
               ]);
                    
                    var options = {
                        colors: ['green', 'red'],
                        is3D: true,
                //pieHole: 0.5
                pieStartAngle: 100,
                chartArea:{left:0,top:0,width:"100%",height:"100%"}
                ,height: "45%"
                ,width: "45%"
                /*slices: {  
                2: {offset: 0.2},
                            3: {offset: 0.3}
                        }*/
                /*slices: {
                            1: { color: 'transparent' }
                        }*/
                    };
            
                    var chart1 = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart1.draw(data, options);
                }
               
                google.maps.event.addDomListener(window, 'load', initMap1(num3, num4, num5, num6));
                
            },
            statusCode: {
                409: function () {
                    $('#msg').html('<span style="color: red;  padding-left: 85px;">Oops! No Hospital Found</span>');
                    $('#msg').show();
                    $('#hospitalTable').hide();
                }
            },
            error: function (err) {
                log(err);
            }
        });


    });

    $('#h_name').keyup(function (e) {
        e.preventDefault();
       
        var hname = $('#h_name').val();
        $.ajax({
            method: "GET",
            url: '/searchLikeHospital/' + hname,
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            success: function (data) {
               
               
                $("ul#searchResult").empty();
                for (var i = 0; i < data.length; i++) {
                    var object = data[i];
                    //put list items here
                    
                    $("#searchResult ul").remove()
                    $("ul#searchResult").append("<li value=" + object.hname + ">" + object.hname + "</li>");
                }

            },
            error: function (err) {
                log(err);
            }
        });


    });

    $('#searchResult').on('click','li',function() { 
        $('#h_name').val($(this).html()); 
        $("ul#searchResult").empty();
    });

    $('#back').on('click', function(e) {
		e.preventDefault();
        $('#backf').hide();
        $('#form1').show();
        $('#form2').hide();
        $('#customers').show();
        $('#form4').hide();
        $('#form3').show();
        $('#form6').hide();
        $('#form5').show();
	});

    $('#logout').on('click', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: '/logout',
			dataType: "json",
			success: function(data) {
				localStorage.setItem('loggedin', 0);
				
				$('#msg').html('<span style="color: green;">You are logged off</span>');
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
