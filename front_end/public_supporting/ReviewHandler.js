var filename = sessionStorage.getItem('filename');
var double_sided = sessionStorage.getItem('double_sided');
var copies = sessionStorage.getItem('copies');
var color = sessionStorage.getItem('color');
//#pagesoption
//var pages = sessionStorage.getItem('pages');

var double_sided_val = 0;
if(double_sided === 'Single Sided')
{
	double_sided_val = 0;
}
else if(double_sided === 'Flip Short Edge')
{
	double_sided_val = 1;
}
else
{
	double_sided_val = 2;
}
var color_val = false;
if(color === 'Color')
{
	color_val = true;
}
var copies_val = parseInt(copies);

var content = 
{
	double_sided: double_sided_val,
	copies: copies_val,
	color: color_val
};

console.log(content);

$(document).ready(function() {

	var output_filename = $('#filename');
	//#pagesoption
	//var output_pages = $('#pages');
	var output_color = $('#color');
	var output_copies = $('#copies');
	var output_doublesided = $('#double_sided');

	output_filename.html(filename);
	output_copies.html(copies);
	//#pagesoption
	//output_pages.html(pages);
	output_color.html(color);
	output_doublesided.html(double_sided);

    $("#printButton").click(function(){
		console.log("print button is clickedddd");

		var auth_key = sessionStorage.getItem("auth_key");
		var uri  = 'https://printzz.herokuapp.com/add_doc_settings?' + $.param({ user_id: auth_key});

	    // $.post(uri, content, function(data, status){
		   //      alert("Data: " + JSON.stringify(data) + "\nStatus: " + status);
	    // 	},
	    // 	"json"
	    // );
    	$.ajax({
            type: 'post',
            url: uri,
            data: JSON.stringify(content),
            contentType: "application/json; charset=utf-8",
            traditional: true,
            success: function(data){
				// alert("Data: " + JSON.stringify(data) + "\nStatus: " + status);

				console.log(JSON.parse(JSON.stringify(data))['status'])
				var status = JSON.parse(JSON.stringify(data))['status'];
				if(status)
				{
					$.get('/html/p_queue', (data, status) => {
						$("#body").html(data);
					});					
				}
				else{
					alert('Error: failed to post settings');
				}


			},
			error: function(textStatus, errorThrown) {
                alert('Error: unable to post settings')
            }
   
        });

	    // $.get('/html/p_queue', function(data, status){
	    //    $("#body").html(data);
	    // });
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