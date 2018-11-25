$(document).ready(function() {
	var default_val_inputfile = $('#input_file').val();

    $("#button_upload").click(function(){
    	if($('#input_file').val() == default_val_inputfile)
    	{
    		alert('Please select a file to print');
    	}
    	else
    	{
    		uploadForm();
    	}
	});

	$('#input_file').change(function(){
		var path = $(this).val();
		var path_array = path.split('\\');
		console.log('path_array-> ' + path_array);
		var filename = path_array[path_array.length-1];
		console.log(filename);
		$('#filename_label').html(filename)
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

//uploading the form
var form = document.getElementById('form_test');
var fileSelect = document.getElementById('input_file');
var uploadButton = document.getElementById('button_upload');

function uploadForm(){
	uploadButton.innerHTML = 'Uploading...';

	console.log('file-length -> ' + fileSelect.files.length);

	var files = fileSelect.files;
	var file = files[0];

	var formData = new FormData();
	formData.append('input_file', file);

	sessionStorage.setItem("filename", file.name);

	var auth_key = sessionStorage.getItem("auth_key");
	var uri  = 'https://printzz.herokuapp.com/add_doc_file?' + $.param({ user_id: auth_key});
	console.log('upload uri -> ' + uri);
	var xhr = new XMLHttpRequest();
	xhr.open('POST', uri, false);
	xhr.onload = function(){
		if (xhr.status === 200) {
			uploadButton.innerHTML = 'Upload';
			var status = JSON.parse(xhr.responseText)['status'];
			if(status)
			{
				$.get('/html/p_settings', function(data, status){
			       $("#body").html(data);
			    });
			}
			else{
				alert('Error: Uploading File')
			}
		}
		else{
			uploadButton.innerHTML = 'Upload';
			alert('error occured');
		}
	};
	xhr.send(formData);
}