$(document).ready(function() {
    
    $("#printAgainButton").click(function(){
		console.log("print again button is clickedddd");
	    $.get('/html/p_settings', function(data, status){
	    	//alert("Data: " + data + "\nStatus: " + status);
	       $("#body").html(data);
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
		$.get('/html/p_queue', (data, status) => {
			$("#body").html(data);
		});
	});
});