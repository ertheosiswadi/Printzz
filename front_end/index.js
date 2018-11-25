const express = require('express');
var fs = require("fs");
const cheerio = require('cheerio');
const fileUpload = require('express-fileupload');
const http = require('http');
const req = require('request');

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
var content_psignup = getHTMLBody('./html_files/sign_up.html');
var content_plogin = getHTMLBody('./html_files/index.html');
var content_pqueue = getHTMLBody('./html_files/print_queue.html');

app.use(express.static('./public_supporting'));

app.get('', (request, response) => {
	response.set('Content-Type', 'text/html');
	setHTMLFile(response);
	response.end();
});

app.get('/html/:page', (request, response) => {
	var page = request.params.page;
	var content = '';
	if(page === 'p_upload')
	{
		content = content_pupload;
	}
	else if(page === 'p_queue')
	{
		content = content_pqueue;
	}
	else if(page === 'p_signup')
	{
		content = content_psignup;
	}
	else if(page === 'p_login')
	{
		content = content_plogin;
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
	response.end();
});

function setHTMLFile(response){
	var fileContents = fs.readFileSync('./html_files/' + 'index' + '.html', {encoding: "utf8"});
	response.write(fileContents);
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