$(document).ready(function() {

	var input_copies = $('#n_copies');
	//#pagesoption
	//var input_pages = $('#n_pages');
	var input_color = $('#select_color');
	var input_doublesided = $('#select_double_sided');

	var filename = sessionStorage.getItem("filename");
	$('#filename').html(filename);
	console.log('copies-> ' + input_copies.val());
	var default_copies_val = input_copies.val();
    $("#confirmButton").click(function(){
    	if(input_copies.val() == default_copies_val)
    	{
    		alert('Please specify the number of copies');
    	}
    	else if(input_copies.val() <= 0 || input_copies.val() > 20)
    	{
    		alert('Invalid Input: Number of copies should be between 1 and 20');
    	}
    	else
    	{
	    	sessionStorage.setItem('double_sided', input_doublesided.val());
	    	sessionStorage.setItem('color', input_color.val());
	    	sessionStorage.setItem('copies', input_copies.val());
	    	//#pagesoption
	    	//sessionStorage.setItem('pages', input_pages.val());

		    $.get('/html/p_review', function(data, status){
		       $("#body").html(data);
		    });   		
    	}

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
		$.get('/html/p_queue', (data, status) => {
			$("#body").html(data);
		});
	});	
});
