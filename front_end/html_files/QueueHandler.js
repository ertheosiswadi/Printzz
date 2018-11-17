
var sampleJSON = {
	files: [
		{
			filename: "file1.pdf",
			progress: "70"
		},
		{
			filename: "file2.pdf",
			progress: "40"
		},
		{
			filename: "file3.pdf",
			progress: "30"
		}
	]
}

sessionStorage.setItem("files", JSON.stringify(sampleJSON));

//-- start
var files_array = JSON.parse(sessionStorage.getItem("files")).files;

var filename = 'test.pdf';
var progress_percent = 76;

$(document).ready(() =>{
	//newFile(filename, progress_percent);
	console.log(JSON.parse(sessionStorage.getItem("files")).files);
	for(i in files_array)
	{
		console.log(files_array[i].filename + "," + files_array[i].progress);
		newFile(files_array[i].filename, files_array[i].progress);
	}

	$('#button_addfile').click(function(){
		$.get('/html/p_queue', function(data, status){
	       $("#body").html(data);
	    });
	});
});


function newFile(filename, percentage)
{
	var markup = "<tr><td>" + filename 
			+ "</td><td><div class='progress'>" 
			+ "<div class='progress-bar progress-bar-success progress-bar-striped active' " 
			+ "style='width:" + percentage + "%;'>"
			+ percentage + "%"
			+ "</div></div></td></tr>"
	$('#table_queue tbody').append(markup);
}