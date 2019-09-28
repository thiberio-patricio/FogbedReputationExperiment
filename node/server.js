const express = require('express')
const app = express()
const port = 3000

var sensors = [];

for (let i = 201; i < 201 + parseInt(process.env.NODES) ; i++) {
   sensors.push({'ip': '10.0.0.' + i, 'type': getType() ,'history': [], 'reput': 0.5})
}

var type = 1;

// Atribui os tipos de serviço
function getType() {
  
  if (type == 1) {
    type = 0;
    return 'temperatura'
  }else {
    type= 1;
    return 'umidade'
  }
}

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Algoritmo que calucla a reputação de um nó
function calcReput(array) {
  if(array.length == 0) return 0.5;
  let positivos = 0;
  let negativos = 0;  
  for(let i = 0; i < array.length ; i++) {
    if(parseInt(array[i]) == 1) positivos++;
    if(parseInt(array[i]) == 0) negativos++;
  }
  console.log('reput:', (positivos + 1)/(positivos + negativos + 2))
  let reput = (positivos + 1)/(positivos + negativos + 2);
  return parseFloat(reput.toFixed(2));
}
function getIndexRandom(tamanhoArray) {
  return getRandomIntInclusive(0, tamanhoArray - 1);
}
// Retorna o nó de maior reputação
function maiorReput(array) {
  let maiores = [];
  let rep_maior = array[0].reput;
  for(let i = 0; i < array.length ; i++) {
    if(array[i].reput >= rep_maior) rep_maior = array[i].reput;  
  }
  for(let i = 0; i < array.length ; i++) {
    if(array[i].reput >= rep_maior) maiores.push(array[i])
  }
  return maiores[getIndexRandom(maiores.length)];
}

app.get('/', (req, res) => {
  res.send('<h1>Home</h1>')
})

app.get('/init', (req, res) => {
  res.send(process.env.NODES);
})

// Retorna os nós de serviços de temperatura , assim como o nó que atende ao requisito especificado ($indicador)
app.get('/temp', (req, res) => {
  var sel = null;
  let ip = req.connection.remoteAddress.split("ffff:")[1];
  console.log('ip', ip)
  var filtered = sensors.filter((element) => {
    return element.ip != ip && element.type == "temperatura";
  })
  sel = maiorReput(filtered);
  res.json({'sensors': filtered.map((element) => {
    return {'ip': element.ip, type: element.type, 'reputacao': element.reput}  
  }), 'sel':sel.ip});
})
// Retorna os nós de serviços de umidade , assim como o nó que atende ao requisito especificado ($indicador)
app.get('/umi', (req, res) => {
  var sel = null;
  let ip = req.connection.remoteAddress.split("ffff:")[1];
  console.log('ip', ip) 
  var filtered = sensors.filter((element) => {
    return element.ip != ip && element.type == "umidade";
  })
  sel = maiorReput(filtered);
  res.json({'sensors': filtered.map((element) => {
    return {'ip': element.ip, 'type': element.type, 'reputacao': element.reput}  
  }), 'sel':sel.ip});
})

// Envia uma avaliação para o nó de IP e com valor (Value)
app.get('/sendAval/:ip/:value', (req, res) => {
  let ip = req.params.ip;
  let value = req.params.value;
  for(let i = 0; i < sensors.length ; i++) {
    if(sensors[i].ip == ip) {
      sensors[i].history.push(value);
      sensors[i].reput = calcReput(sensors[i].history);
      res.send('Enviado !!');
      return;
    }    
  }
  res.send('Não foi enviado!!');
})
// Retorna a reputação de um nó de ip
app.get('/reput/:ip', (req, res) => {
  let ip = req.params.ip;
  for(let i = 0; i < sensors.length ; i++) {
    if(sensors[i].ip == ip) {
      res.json({'reputacao': sensors[i].reput});
      return;
    }    
  }
  res.send('Não enviado !!');

})

// Retorna a informação de todos os nós da rede
app.get('/all', (req, res) => {  
  res.json({'sensors': sensors.map((element) => {
    return {'ip': element.ip, 'type': element.type, 'reputacao': element.reput, 'history': element.history}  
  })});
})

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`)
  console.log('Para derrubar o servidor: ctrl + c');
})
