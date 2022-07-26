import matplotlib.pyplot as plt
from math import ceil
import os

cwndDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
cwndDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
goodputDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
goodputDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
rttDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
rttDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
lossDict04 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}
lossDict15 = {"reno": [0] * 1001, "cubic": [0] * 1001, "yeah": [0] * 1001, "vegas": [0] * 1001}


def splitFile(filename):
	lines = []
	file = open(filename, 'r')
	line = file.readline()
	while line:
		lines.append(line.split())
		line = file.readline()
	return lines

def adjustArray(arr, defaultVal):
	for i in range(len(arr)):
		if arr[i] == defaultVal:
			arr[i] = arr[i-1] if i != 0 else 0
	return arr

def splitCWND(data):
	cwnds04 = [-1] * 1001
	cwnds15 = [-1] * 1001
	for line in data:
		if 'cwnd_' in line:
			indexes = [0,6]
			if line[1] == '0':
				cwnds04[ceil(float(line[0]))] = float(line[6])
			else:
				cwnds15[ceil(float(line[0]))] = float(line[6])
	cwnds04 = adjustArray(cwnds04, -1)
	cwnds15 = adjustArray(cwnds15, -1)

	return cwnds04, cwnds15

def splitAcks(data):
	acks04 = ['none'] * 1001
	acks15 = ['none'] * 1001
	for line in data:
		if 'ack_' in line:
			if line[1] == '0':
				acks04[ceil(float(line[0]))] = int(line[-1])
			else:
				acks15[ceil(float(line[0]))] = int(line[-1])
	return adjustArray(acks04, 'none'), adjustArray(acks15, 'none')

def splitloss(data):
	loss04 = [-1] * 1001
	lastloss04 = 0
	loss15 = [-1] * 1001
	lastloss15 = 0
	for line in data:
		if line[0] == 'd':
			if line[-4][0] == '0':
				lastloss04 += 1
				loss04[ceil(float(line[1]))] = lastloss04
			elif line[-4][0] == '1':
				lastloss15 += 1
				loss15[ceil(float(line[1]))] = lastloss15
	return adjustArray(loss04, -1), adjustArray(loss15, -1)

def splitRtt(data):
	rtt04 = [-1] * 1001
	rtt15 = [-1] * 1001
	for line in data:
		if 'rtt_' in line:
			if line[1] == '0':
				rtt04[ceil(float(line[0]))] = float(line[-1])
			else:
				rtt15[ceil(float(line[0]))] = float(line[-1])
	return adjustArray(rtt04, -1), adjustArray(rtt15, -1)

def addCwndDatas(renoData, cubicData, yeahData,vegasData):
	global cwndDict04, cwndDict15
	renoCwnds04, renoCwnds15 = splitCWND(renoData)
	cubicCwnds04, cubicCwnds15 = splitCWND(cubicData)
	yeahCwnds04, yeahCwnds15 = splitCWND(yeahData)
	vegasCwnds04, vegasCwnds15 = splitCWND(vegasData)

	for i in range(1001):
		cwndDict04['reno'][i] += renoCwnds04[i]
		cwndDict04['cubic'][i] += cubicCwnds04[i]
		cwndDict04['yeah'][i] += yeahCwnds04[i]
		cwndDict04['vegas'][i] += vegasCwnds04[i]
		cwndDict15['reno'][i] += renoCwnds15[i]
		cwndDict15['cubic'][i] += cubicCwnds15[i]
		cwndDict15['yeah'][i] += yeahCwnds15[i]
		cwndDict15['vegas'][i] += vegasCwnds15[i]

def addGoodputDatas(renoData, cubicData, yeahData,vegasData):
	global goodputDict04, goodputDict15
	renoGoodputs04, renoGoodputs15 = splitAcks(renoData)
	cubicGoodputs04, cubicGoodputs15 = splitAcks(cubicData)
	yeahGoodputs04, yeahGoodputs15 = splitAcks(yeahData)
	vegasGoodputs04, vegasGoodputs15 = splitAcks(vegasData)

	for i in range(1001):
		goodputDict04['reno'][i] += renoGoodputs04[i]
		goodputDict04['cubic'][i] += cubicGoodputs04[i]
		goodputDict04['yeah'][i] += yeahGoodputs04[i]
		goodputDict04['vegas'][i] += vegasGoodputs04[i]
		goodputDict15['reno'][i] += renoGoodputs15[i]
		goodputDict15['cubic'][i] += cubicGoodputs15[i]
		goodputDict15['yeah'][i] += yeahGoodputs15[i]
		goodputDict15['vegas'][i] += vegasGoodputs15[i]

def addRttDatas(renoData, cubicData, yeahData,vegasData):
	global rttDict04, rttDict15
	renoRtts04, renoRtts15 = splitRtt(renoData)
	cubicRtts04, cubicRtts15 = splitRtt(cubicData)
	yeahRtts04, yeahRtts15 = splitRtt(yeahData)
	vegasRtts04, vegasRtts15 = splitRtt(vegasData)

	for i in range(1001):
		rttDict04['reno'][i] += renoRtts04[i]
		rttDict04['cubic'][i] += cubicRtts04[i]
		rttDict04['yeah'][i] += yeahRtts04[i]
		rttDict04['vegas'][i] += vegasRtts04[i]
		rttDict15['reno'][i] += renoRtts15[i]
		rttDict15['cubic'][i] += cubicRtts15[i]
		rttDict15['yeah'][i] += yeahRtts15[i]
		rttDict15['vegas'][i] += vegasRtts15[i]

def addlossDatas(renoData, cubicData, yeahData,vegasData):
	global lossDict04, lossDict15
	renoloss04, renoloss15 = splitloss(renoData)
	cubicloss04, cubicloss15 = splitloss(cubicData)
	yeahloss04, yeahloss15 = splitloss(yeahData)
	vegasloss04, vegasloss15 = splitloss(vegasData)

	for i in range(1001):
		lossDict04['reno'][i] += renoloss04[i]
		lossDict04['cubic'][i] += cubicloss04[i]
		lossDict04['yeah'][i] += yeahloss04[i]
		lossDict04['vegas'][i] += vegasloss04[i]
		lossDict15['reno'][i] += renoloss15[i]
		lossDict15['cubic'][i] += cubicloss15[i]
		lossDict15['yeah'][i] += yeahloss15[i]
		lossDict15['vegas'][i] += vegasloss15[i]

def runOneEpoch():
	os.system("ns renoCode.tcl")
	os.system("ns cubicCode.tcl")
	os.system("ns yeahCode.tcl")
	os.system("ns vegasCode.tcl")

	renoData = splitFile('renoTrace.tr')
	cubicData = splitFile('cubicTrace.tr')
	yeahData = splitFile('yeahTrace.tr')
	vegasData = splitFile('vegasTrace.tr')

	addCwndDatas(renoData, cubicData, yeahData, vegasData)
	addGoodputDatas(renoData, cubicData, yeahData, vegasData)
	addRttDatas(renoData, cubicData, yeahData, vegasData)
	addlossDatas(renoData, cubicData, yeahData, vegasData)

def calcAvgVars():
	global cwndDict04, cwndDict15, goodputDict04, goodputDict15
	for key in cwndDict04.keys():
		for i in range(1001):
			cwndDict04[key][i] /= 10
			cwndDict15[key][i] /= 10
			goodputDict04[key][i] /= 10
			goodputDict15[key][i] /= 10
			rttDict04[key][i] /= 10
			rttDict15[key][i] /= 10
			lossDict04[key][i] /= 10
			lossDict15[key][i] /= 10

def run():
	runOneEpoch()


def derivative(arr):
	arr2 = [0] * len(arr)
	for i in range(1,len(arr)):
		arr2[i] = arr[i] / i 
	arr2[0] = arr[0]
	return arr2

def difference(arr):
	arr2 = [0] * len(arr)
	for i in range(1, len(arr)):
		arr2[i] = arr[i] - arr[i-1]
	arr2[0] = arr[0]
	return arr2

def analyzeGoodPut():
	global goodputDict04, goodputDict15

	colors = ['c', 'm', 'y', 'g', 'b', 'r', 'k', 'k']
	for key in goodputDict04.keys():
		plt.plot(range(1001),derivative(goodputDict04[key]), label=key+'04', c = colors[-1])
		colors.pop()
		plt.plot(range(1001), derivative(goodputDict15[key]), label=key+'15', c = colors[-1])
		colors.pop()

	plt.xlabel("time") 
	plt.ylabel("Goodput rate") 
	plt.title("Goodput rate per second") 
	plt.legend() 
	plt.show() 



def analyzeloss():
	global lossDict04, lossDict15
	colors = ['c', 'm', 'y', 'g', 'b', 'r', 'k', 'k']
	for key in lossDict04.keys():
		plt.plot(range(1001),difference(lossDict04[key]), label=key+'04', c = colors[-1])
		colors.pop()
		plt.plot(range(1001), difference(lossDict15[key]), label=key+'15', c = colors[-1])
		colors.pop()

	plt.xlabel("time") 
	plt.ylabel("Packet loss rate") 
	plt.title("Packet loss rate per second") 
	plt.legend() 
	plt.show() 

	# colors = ['c', 'm', 'y', 'g', 'b', 'r']
	# for key in lossDict04.keys():
	# 	plt.plot(range(1001),difference(lossDict04[key]), label=key+'04', c = colors[-1])
	# 	colors.pop()
	# 	plt.plot(range(1001), difference(lossDict15[key]), label=key+'15', c = colors[-1])
	# 	colors.pop()

	# plt.xlabel("time") 
	# plt.ylabel("Packet loss rate") 
	# plt.title("Packet loss rate per second") 
	# plt.legend() 
	# plt.show() 


run()
analyzeGoodPut()

analyzeloss()
