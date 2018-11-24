const comment_template = Handlebars.compile(
	document.getElementById('comment_template').innerHTML);

$(document).ready( () => {
  // Initializes the Materialize components
	$('.modal').modal();

	$('.tabs').tabs()

	$('.sidenav').sidenav()
	
	$('.sidenav').tabs()

  // Gets the current secondary title probability from local storage and sets 
  // it to 0.2 if none exists
	if (!localStorage.getItem('p')) {
		localStorage.setItem('p', 0.2);
	}

	var p = localStorage.getItem('p');

  // Determines which title to show based on the probability 
  // and a random number
	if (p == 0) {
		$('.logo1').show();
		$('.logo2').hide();
	}
	if (p == 1) {
		$('.logo1').hide();
		$('.logo2').show();
	}
	else {
		var n = Math.floor(Math.random() * 100);

		if (n <= 99 - (100 * p)) {
			$('.logo1').show();
			$('.logo2').hide();
		}
		if (n >= 100 - (100 * p)) {
			$('.logo1').hide();
			$('.logo2').show();
		}
	}

	var slider = document.getElementById('slider');
    // Creates the slider and sets its range
  	noUiSlider.create(slider, {
	   	start: [p],
	   	connect: [true, false],
	   	step: 0.01,
	  	orientation: 'horizontal',
	  	tooltips: true,
	   	range: {
	    	'min': 0,
	    	'max': 1
	  	}
  	});

  	slider.noUiSlider.on('change', function () {
      // Changes the secondary title probability when the slider is changed
  		localStorage.setItem('p', slider.noUiSlider.get());
  	});

  	$('#new_comment').submit(() => {
      // Creates a new comment upon submission
  		var comment = $('#comment').val();
  		var id = $('#post').html();

  		$.ajax({
  			url: "new_comment",
  			data: {"comment": comment, 'post': id},
  			dataType: 'json',
  			success: function (data) {
  				if (data.valid)
  				{
  					content = comment_template(data);

  					$('.comments').append(content);

  					$('#comment').val("");
  				}
  			},
  		});

  		return false;
  	});

  	$('#randomize').click(event => {
      // Retrieves a random restaurant
  		$.ajax({
  			url: "randomize",
  			data: {},
  			dataType: 'json',
  			success: function (data) {
  				$('#result_name').html(data.result_name);
  				$('#result_location').html(data.result_location);
  			}
  		});

  		return false;
  	});

    // Disables the login submit button
  	$('.login_submit').prop('disabled', true);

  	$('#username_login').change(() => {
      // Checks if the username is valid
  		username = $('#username_login').val();

  		$.ajax({
  			url: "check_username_login",
  			data: {"username": username},
  			dataType: 'json',
  			success: function (data) {
  				if (data.valid) {
  					$('.username_login_helper').html("");
  					$('.login_submit').prop('disabled', false);
  				}
  				else {
  					$('.username_login_helper').html("Username Invalid");
  					$('.login_submit').prop('disabled', true);
  				}
  			}
  		});
  	});

  	$('.login_submit').click(event => {
      // Logs a user in
  		username = $('#username_login').val();

  		password = $('#password_login').val();

  		if (password == "") {
  			$('#login_text').html("No Password Entered");

  			return false
  		}
  		else {
  			$('#login_text').html("");

  			$.ajax({
  				url: "check_login",
  				data: {"username": username, "password": password},
  				dataType: 'json',
  				success: function (data) {
  					if (data.login) {
  						location.reload()
  					}
  					else {
  						$('#login_text').html("Incorrect Password");

  						$('#password_login').html("");
  					}
  				}
  			});
  		}

  		return false
  	});

  	$('.signup_submit').click(event => {
      // Signs a user up
  		first = $('#first').val();

  		last = $('#last').val();

  		username = $('#username_signup').val();

  		password = $('#password_signup').val();

  		email = $('#email').val();

  		$.ajax({
  			url: "check_signup",
  			data: {
  				"first": first,
  				"last": last,
  				"username": username,
  				"password": password,
  				"email": email
  			},
  			dataType: 'json',
  			success: function (data) {
  				if (! data.username_valid) {
  					$('.username_signup_helper').html("Username Taken");
  				}
  				else if (! data.username_length) {
  					$('.username_signup_helper').html(
  						"Username must be at least 5 characters");
  				}
  				else {
  					$('.username_signup_helper').html("");
  				}

  				if (! data.password_valid) {
  					$('.password_signup_helper').html(
  						"Password must be at least 8 characters");
  				}
  				else {
  					$('.password_signup_helper').html("");
  				}

  				if (! data.email_valid) {
  					$('.email_signup_helper').html(
  						"Please enter a valid email address")
  				}
  				else {
  					$('.email_signup_helper').html("")
  				}

  				if (
  					data.username_valid 
  					& data.username_length 
  					& data.password_valid 
  					& data.email_valid) {
  					location.reload()
  				}
  			}
  		});

  		return false;
  	});

  // Creates the restaurant data visualization
	$.ajax({
	  	url: "get_data",
  		success: function (data) {
  			count = []
  			for (var i = data.c.length - 1; i >= 0; i--) {
  				count.push(data.c[i].count)
  			}

  			var height = 10;

  			var chart = d3.select(".chart")
  				.attr("preserveAspectRatio", "xMinYMin meet")
  				.attr("viewBox", "0 0 350 350")

  			var bar = chart.selectAll("g")
  				.data(data.c)
  				.enter()
  				.append("g")
  				.attr("transform", function(d, i) { return "translate(0," + i * height + ")"; })

  			bar.append("rect")
  				.attr("width", function(d) { return 20 * d.count + "px"; })
  				.attr("height", height - 1)

  			bar.append("text")
  				.attr("x", function(d) { return 20 * d.count - 3; })
  				.attr("y", height/2)
  				.attr("dy", ".35em")
  				.text(function (d) { return d.cuisine + " " + d.count; });
  		}
	});

})