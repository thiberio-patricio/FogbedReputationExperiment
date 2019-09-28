const express = require('express')
const app = express()
const port = 3000


function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

app.get('/', (req, res) => {	
  res.send(process.env.TYPENODE)
})

// Retorna um valor randômico de temperatura ou umidade para o requisitador
app.get('/value', (req, res) => {
	// console.log('ip: ', req.connection.remoteAddress)
	// console.log('ip1: ', req.socket.remoteAddress)
	var t = getRandomIntInclusive(0, 50);
  res.json({'value': t});
})

app.listen(port, () => {
  console.log(`Client rodando em http://localhost:${port}`)
  console.log('Para derrubar o servidor: ctrl + c');
})















