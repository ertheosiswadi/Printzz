$(document).ready(function()
{
	console.log('im at sign up page');
	$('#signup_submit').click(() => {

   		//get the value of username and password
		var username = $('#username_field').val();
		var password = $('#password_field').val();

		var jsonData = {username: username, password: password};

		//post to register
    	$.ajax({
            type: 'post',
            url: 'https://printzz.herokuapp.com/register',
            data: JSON.stringify(jsonData),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: function(data){
            	var status = data['status'];
            	if(status)
            	{
					sessionStorage.setItem('auth_key',data['data']['user_id']);
					//alert('saved auth_key (login)-> ' + sessionStorage.getItem('auth_key'));

					//proceed if success
					$.get('/html/p_queue', function(data, status){
						$("#body").html(data);
					});
     			}
				else
				{
					alert('Error: username is taken');
				}
			},
			error: function(textStatus, errorThrown) {
                alert('Error: server error');
            }

        });
	});


	//navigation bar redirect
    $("#signup_nav").click(function(){
    	$.get('/html/p_signup', function(data, status){
	       $("#body").html(data);
	    });
    });
	$('#login_nav').click(() => {
		$.get('/html/p_login', (data, status) => {
			$("#body").html(data);
		});
	});
	$('.navbar-brand').click(function(){
		$.get('/html/p_login', (data, status) => {
			$("#body").html(data);
		});
	});
});
