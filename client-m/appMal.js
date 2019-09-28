const express = require('express')
const app = express()
const port = 3000

var limit = process.env.NUM;
var positivas = 0;

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

app.get('/', (req, res) => {	
  res.send('<p>Home</p>')
})

app.get('/numero', (req, res) => {  
  res.send({'current': positivas})
})

app.get('/limit', (req, res) => {  
  res.send(process.env.NUM)
})
// Retorna um valor randômico de temperatura ou umidade para o requisitador
app.get('/value', (req, res) => {
	// console.log('ip: ', req.connection.remoteAddress)
	// console.log('ip1: ', req.socket.remoteAddress)
	var t = 0;
	if( positivas <= limit ) {
		t = getRandomIntInclusive(0, 50);
		positivas++;
	}else {
		t = getRandomIntInclusive(51, 100);
	}
  res.json({'value': t});
})

app.listen(port, () => {
  console.log(`Client rodando em http://localhost:${port}`)
  console.log('Para derrubar o servidor: ctrl + c');
})
















