import time
import random
import json
from src.fogbed.experiment import FogbedExperiment, FogbedDistributedExperiment
from src.fogbed.resourcemodel import CloudResourceModel, EdgeResourceModel, FogResourceModel, PREDEFINED_RESOURCES
from src.fogbed.topo import FogTopo
from src.mininet.link import TCLink
from src.mininet.log import setLogLevel
from src.mininet.node import OVSSwitch

setLogLevel('info')

topo = FogTopo()

#c1 = topo.addVirtualInstance("cloud")
f1 = topo.addVirtualInstance("fog")
e1 = topo.addVirtualInstance("edge")

erm = EdgeResourceModel(max_cu=20, max_mu=2048)
frm = FogResourceModel()
#crm = CloudResourceModel()

e1.assignResourceModel(erm)
f1.assignResourceModel(frm)
#c1.assignResourceModel(crm)

MANAGER_NODES = [];
QTD_EGO = 1;
QTD_NODES_ALL = 15;


node_server = f1.addDocker('server', ip='10.0.0.251', dimage="node-app", environment={"NODES": QTD_NODES_ALL - QTD_EGO}, resources=PREDEFINED_RESOURCES['large'])
i = 1;
for x in range(201, 216):
	current = None
	if x < 209: current = e1.addDocker('d' + str(i), ip='10.0.0.' + str(x), dimage="client", environment={"TYPENODE":"honesto"})
	if x < 215 and x >= 209: current = e1.addDocker('d' + str(i), ip='10.0.0.' + str(x), dimage="client-m", environment={"NUM": 5})
	if x < 216 and x >= 215: current = e1.addDocker('d' + str(i), ip='10.0.0.' + str(x), dimage="client", environment={"TYPENODE":"egoista"})
	MANAGER_NODES.append(current)
	i+=1

# EGOISTAS = 0;


# node_server = f1.addDocker('server', ip='10.0.0.251', dimage="node-app", environment={"NODES": 2 - EGOISTAS}, resources=PREDEFINED_RESOURCES['large'])
# i = 1;
# for x in range(201, 203):
# 	current = None
# 	#if x < 209: current = e1.addDocker('d' + str(i), ip='10.0.0.' + str(x), dimage="client", environment={"TYPENODE":"honesto"})
# 	if x < 203 and x >= 201: current = e1.addDocker('d' + str(i), ip='10.0.0.' + str(x), dimage="client-m", environment={"NUM": 10})
# 	#if x < 216 and x >= 215: current = e1.addDocker('d' + str(i), ip='10.0.0.' + str(x), dimage="client", environment={"TYPENODE":"egoista"})
# 	MANAGER_NODES.append(current)
# 	i+=1

s1 = topo.addSwitch('s1')

topo.addLink(s1, e1)
topo.addLink(e1, f1, cls=TCLink, delay='200ms', bw=1)

exp = FogbedExperiment(topo, switch=OVSSwitch)
exp.start()

def sendAval(node, ip, value):
  exp.get_node("edge.d" + node).cmd("curl 10.0.0.251:3000/sendAval/" + ip + "/" + value)

def randomNode(init, end):
  return random.randint(init, end)

def randomServico():
  r = random.randint(0, 1)
  if r == 0: return 'temp' 
  if r == 1: return 'umi'
  return 'temp' 

def avaliar(x, node_current, ip_avaliable):
	if value > 50:
		print 'Node d' + str(node_current) + ' Avaliando Mal ... ' + str(x)
		print exp.get_node("edge.d" + str(node_current)).cmd("curl 10.0.0.251:3000/sendAval/" + ip_avaliable + "/" + "0")
		return "0"
	else:
		print 'Node d' + str(node_current) + ' Avaliando Bem ... ' + str(x)
		print exp.get_node("edge.d" + str(node_current)).cmd("curl 10.0.0.251:3000/sendAval/" + ip_avaliable + "/" + "1")
		return "1"

arquivo = open('Honesto_1.csv', 'w')
# arquivo.close()
# arquivo = open('resultados.csv', 'r') # Abra o arquivo (leitura)
# conteudo = arquivo.readlines()
arquivo.write("REQUI, NODE_R, NODE_RES, AVALIABLE, REPUT_PREV, REPUT_NOW" + '\n')

try:
	 	exp.monitor()
	 	print "waiting 2 seconds for routing algorithms on the controller to converge"
	 	for x in range(0, 200):
			node_current = randomNode(1, QTD_NODES_ALL - QTD_EGO)
			typeServico = randomServico	()
			data = exp.get_node("edge.d" + str(node_current)).cmd("curl 10.0.0.251:3000/" + typeServico)
			print data
			obj = json.loads(data)
			ip = obj["sel"]
			print obj["sel"] + '\n'
			data = exp.get_node("edge.d" + str(node_current)).cmd("curl " + ip + ":3000/value")
			obj = json.loads(data)
			value = obj["value"]
			print '[' + typeServico + '] ' + 'Servico de d' + ip[8:10] + ' : ' + ' com valor : ' + str(value)
			aval = ""
			reputInitial = json.loads(exp.get_node("edge.d" + str(node_current)).cmd("curl 10.0.0.251:3000/reput/" + ip))["reputacao"]
			if node_current >= 9 and node_current <=14:
				data = exp.get_node("edge.d" + str(node_current)).cmd("curl localhost:3000/numero")
				obj = json.loads(data)
				numero = obj["current"]
				if numero > 5:
					print 'Node malicioso d' + str(node_current) + ' avaliando ruim ...' 
					print exp.get_node("edge.d" + str(node_current)).cmd("curl 10.0.0.251:3000/sendAval/" + ip + "/" + "0")
					aval = "0"
				else: aval = avaliar(x,node_current,ip)
			else: aval = avaliar(x,node_current,ip)
			time.sleep(0.5)
			reputFinal = json.loads(exp.get_node("edge.d" + str(node_current)).cmd("curl 10.0.0.251:3000/reput/" + ip))["reputacao"]
			print reputFinal
			arquivo.write(str(x)  + ', ' + "d" + str(node_current) + ', ' + ip[8:10] + ', ' + aval + ', ' + str(reputInitial) + ', ' + str(reputFinal) + '\n')
		# exp.CLI()
finally:
		# arquivo = open('resultados.csv', 'w') # Abre novamente o arquivo (escrita)
		# arquivo.writelines(conteudo) 
		arquivo.close()
		exp.stop()