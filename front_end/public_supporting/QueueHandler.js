//-- start

var doc_id = [];

$(document).ready(() =>{

	updateQueue();
	var interval_id = setInterval(updateQueue, 4000);
	
	$('#button_addfile').click(function(){

		clearInterval(interval_id);

		$.get('/html/p_upload', function(data, status){
	       $("#body").html(data);
	    });
	});

	$(document).on("click", "button.btn-danger" , function() {
		event.stopImmediatePropagation();
		console.log('delete button is clicked. id-> ' + event.target.id);
       	var index = event.target.id;
		console.log(doc_id[index]);

		var docid = doc_id[index];
		var auth_key = sessionStorage.getItem('auth_key');
		var uri = 'https://printzz.herokuapp.com/delete_doc?doc_id=' + docid + '&user_id=' + auth_key;
		
		//UNCOMMENT BELOW TO ACTIVATE DELETE_DOC
		$.get(uri, function(data, status){
			console.log('performing a delete request..')
			if(data['status'])
			{
				updateQueue();
			}
	       	else{
	       		alert('Error: cannot delete doc')
	       	}
	    });

		//get the id of the button clicked
		//the id is the index will correspond to the document id
		//delete_doc endpoint
		//if delete_doc is successful, refresh the page
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

function getFileMarkup(filename, percentage, index)
{
	return '<tr>'
	        +'<td style="text-align: center;vertical-align: middle;">'+ filename +'</td>'
	        +'<td>'
	              +'<div class="col-md-9 col-sm-9 col-lg-9">'
	                +'<div class="progress" style="vertical-align: middle;margin-bottom: 0px;margin-top: 5px;">'
	                  +'<div class="progress-bar progress-bar-success progress-bar-striped active" style="width:'+ percentage +'%;vertical-align: middle">'+ percentage +'%</div>'
	                +'</div>'
	              +'</div>'
	              +'<div class="col-md-2 col-sm-2 col-lg-2" style="align-self:right;vertical-align: middle">'
	                +'<button id=' + index + ' style="align-self:stretch" class="btn btn-danger">Delete</button>'
	              +'</div>'
	        +'</td>'
	  	+'</tr>';
}

function updateQueue()
{
	var auth_key = sessionStorage.getItem('auth_key');
	var uri = 'https://printzz.herokuapp.com/get_queue?user_id=' + auth_key;
	$.get(uri, function(data, status){
	   	var fileList = {
   			files:data
	   	}
	   	sessionStorage.setItem("files", JSON.stringify(fileList)); 

	   	var files_array = JSON.parse(sessionStorage.getItem("files")).files;

	   	if(files_array.length == 0)
	   	{
	   		showNoFiles();
	   	}
	   	else{
			var auth_key = sessionStorage.getItem("auth_key");
			var markup = '';
			doc_id = [];
			for(i in files_array)
			{
				doc_id.push(files_array[i].doc_id);
				console.log(doc_id);
				markup = markup + getFileMarkup(files_array[i].doc_name, Math.round(files_array[i].progress), i);
			}
			$('#table_queue tbody').html(markup);
	   	}
	});

	updatePrinterStatus();
}

function updatePrinterStatus()
{
	var auth_key = sessionStorage.getItem('auth_key');
	var uri = 'https://printzz.herokuapp.com/printer_status';
	$.get(uri, function(data, status){
		//get status from data parameter
		var p_status = true;
		if(p_status)
		{
			$('.circle').css("background-color", "#006400");
		}
		else
		{
			$('.circle').css("background-color", "#B22222");
		}
	});
}

function showNoFiles()
{
	$('#table_queue tbody').html('<tr>'
	        +'<td style="text-align: center;vertical-align: middle;">'+ 'Print Queue Empty' +'</td>'
	        +'<td style="text-align: center">'
	              +'-'
	        +'</td>'
	  	+'</tr>');
}