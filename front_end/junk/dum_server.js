const express = require('express');
var fs = require("fs");
const cheerio = require('cheerio');
const fileUpload = require('express-fileupload');

const app = express();

//app.use(express.json());
var bodyParser = require('body-parser')
app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: true }));
app.use(fileUpload());

var content_pupload = getHTMLBody('./html_files/print_upload.html');
var content_psettings = getHTMLBody('./html_files/print_settings.html');
var content_preview = getHTMLBody('./html_files/print_review.html');
var content_psuccess = getHTMLBody('./html_files/print_success.html');

app.use(express.static('./public_supporting'));

app.get('', (request, response) => {
	response.set('Content-Type', 'text/html');
	setHTMLFile(response, 0);
	response.sendFile(__dirname + '/LoginHandler.js');
	response.end();
});

app.get('/html/:page', (request, response) => {
	var page = request.params.page;
	var content = '';
	if(page === 'p_upload')
	{
		content = content_pupload;
	}
	else if(page === 'p_settings')
	{
		content = content_psettings;
	}
	else if(page === 'p_review')
	{
		content = content_preview;
	}
	else if(page === 'p_success')
	{
		content = content_psuccess;
	}
	response.set('Content-Type', 'text/text');
	response.write(content);
	//console.log(content);
	response.end();
});

app.post('/add_doc', (request, response) => {
	console.log(request.body);
	var double_sided = request.body.double_sided;
	var copies = request.body.copies;
	var color = request.body.color;

	console.log(double_sided + " " + copies + " " + color);
	var res = {
		"double_sided" : double_sided,
		"copies" : copies,
		"color" : color
	}
	response.send("I gotchu ;) -> " + request.body);
});

app.post('/upload', (request, response) => {
	if(Object.keys(request.files).length == 0)
	{
		return response.status(400).send('No files were uploaded');
	}
	let file = request.files.input_file;
	console.log(file);
	moveFileToDestination(file, response);
});

function setHTMLFile(response, specifier){
	var filename = ''
	if(specifier === 0)
	{
		filename = 'index';
	}
	else if(specifier === 1)
	{
		filename = 'print_settings';
	}
	var fileContents = fs.readFileSync('./html_files/' + filename + '.html', {encoding: "utf8"});
	response.write(fileContents);
	console.log(filename);
}

app.listen(3002, () => {
	console.log('server is live');
});

function getHTMLBody(filepath)
{
	var html = fs.readFileSync(filepath).toString();
	//console.log(html);
	var $ = cheerio.load(html);
	var body = $('body').html().toString();
	return body;
}

function moveFileToDestination(file, response)
{
	let directory = './uploaded_files'
	fs.readdir(directory, (error, files) =>
	{
		console.log('dir_length-> ' + files.length);
		file.mv('./uploaded_files/' + files.length + '.pdf', (err)=>{
			console.log('file uploaded');
			response.send('File Uploaded');
		});
	})
}