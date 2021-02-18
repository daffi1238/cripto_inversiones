//npm install connect server-static
//npm install express
//node server.js


const http = require('http');
var express = require('express');

const hostname = '127.0.0.1';
const port = 8080;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hola Mundo');
});

var app = express();
app.get('/test', function(req, res) {
    res.sendFile('file.html')
});
