//var FormData = require('form-data');

$(document).ready(function() {



	var form = new FormData($("#form_test"));
	
	$("#form_test").onsubmit = (event)=>{
		event.preventDefault();
		var request = new XMLHttpRequest();
		request.open('POST', 'localhost:3001/upload', false);
		request.send(form);
		console.log(request.response);
	}


	// $("#chooseButton").click(function() {
	//     $("#input_file").click();
	//     console.log('hello');
	// })

	// $('#input_file').change(function() {
	//     console.log($('#input_file').val());
	//     $('#input_file').submit(function(){
	// 	    alert("Submitted");
	// 	});
	// });
});
var button = document.getElementById('button_submit');
var data = new FormData(document.getElementById('form_test'));


var xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function () {
  if (this.readyState === 4) {
    console.log(this.responseText);
  }
});
button.onclick = ()=>{
	console.log('submitbutton clicked')
	xhr.open("POST", "/upload");
	xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
	xhr.setRequestHeader("Cache-Control", "no-cache");
	xhr.setRequestHeader("Access-Control-Allow-Origin","*");
	// xhr.setRequestHeader("Postman-Token", "f87cc140-05fb-4b17-a50c-4b11030e5093");

	xhr.send(data);
}
