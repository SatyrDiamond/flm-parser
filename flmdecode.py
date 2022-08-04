#!/bin/python3 
from io import BytesIO

def bytearray2BytesIO(bytearray):
	riffinsideriffobj = BytesIO()
	riffinsideriffobj.write(bytearray)
	return riffinsideriffobj

def readriffdata(riffbytebuffer, offset):
	if isinstance(riffbytebuffer, (bytes, bytearray)) == True:
		riffbytebuffer = bytearray2BytesIO(riffbytebuffer)
	riffobjects = []
	riffbytebuffer.seek(0,2)
	filesize = riffbytebuffer.tell()
	riffbytebuffer.seek(offset)
	while filesize > riffbytebuffer.tell():
		chunkname = riffbytebuffer.read(4)
		chunksize = int.from_bytes(riffbytebuffer.read(4), "little")
		chunkdata = riffbytebuffer.read(chunksize)
		riffobjects.append([chunkname, chunkdata])
	return riffobjects

def parse_evn2_test(evn2bytes):
	notelistdata = BytesIO()
	notelistdata.write(evn2bytes)
	fileobject.seek(0,2)
	notelistdata_filesize = notelistdata.tell()
	notelistdata.seek(0)
	something = int.from_bytes(notelistdata.read(2), "little")
	while notelistdata.tell() < notelistdata_filesize:
		outfile.write('\t\t\t\t' + bytes(notelistdata.read(19)).hex() + '\n')

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("flm")

args = parser.parse_args()

fileobject = open(args.flm, 'rb')
fileobject.seek(0,2)
filesize = fileobject.tell()
fileobject.seek(0)
headername = fileobject.read(4)

riffobjects = readriffdata(fileobject, 4)

outfile = open('flms.flms', 'w')

tabcount = 0
for riffobject in riffobjects:
	if riffobject[0] == b'RACK':
		outfile.write(str(riffobject[0].decode("utf-8")) + ' ' + bytes(riffobject[1][:4]).hex() + '\n')
		rackdata = readriffdata(bytearray2BytesIO(riffobject[1]),8)
		for riffobject in rackdata:
			if riffobject[0] == b'RMOd':
				outfile.write('\t' + str(riffobject[0].decode("utf-8")) + ' ' + bytes(riffobject[1][:8]).hex() + '\n')
				RMOd = readriffdata(bytearray2BytesIO(riffobject[1]),8)
				for riffobject in RMOd:
					if riffobject[0] == b'CSTM':
						CSTMdata = readriffdata(bytearray2BytesIO(riffobject[1]),4)
						if riffobject[1][:4] == b'10WD':
							outfile.write('\t\t' + str(riffobject[0].decode("utf-8")) + '\n')
							for riffobject in CSTMdata:
								outfile.write('\t\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
						else:
							outfile.write('\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
					else:
						outfile.write('\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
			else:
				outfile.write('\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
	elif riffobject[0] == b'CHNL':
		outfile.write(str(riffobject[0].decode("utf-8")) + ' ' + bytes(riffobject[1][:4]).hex() + '\n')
		chnldata = readriffdata(bytearray2BytesIO(riffobject[1]),8)
		for riffobject in chnldata:
			if riffobject[0] == b'TRKH':
				outfile.write('\t' + str(riffobject[0].decode("utf-8")) + '\n')
				trackdata = readriffdata(bytearray2BytesIO(riffobject[1]),0)
				for riffobject in trackdata:
					if riffobject[0] == b'CLIP':
						position = riffobject[1][:4]
						outfile.write('\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(int.from_bytes(position, "little")) + '\n')
						clipdata = readriffdata(bytearray2BytesIO(riffobject[1]),8)
						for riffobject in clipdata:
							if riffobject[0] == b'EVN2':
								outfile.write('\t\t\t' + str(riffobject[0].decode("utf-8")) + '\n')
								parse_evn2_test(riffobject[1])
							elif riffobject[0] == b'CLSm':
								outfile.write('\t\t\t' + str(riffobject[0].decode("utf-8")) + '\n')
								CLSmdata = readriffdata(bytearray2BytesIO(riffobject[1]),4)
								for riffobject in CLSmdata:
									outfile.write('\t\t\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
							else:
								outfile.write('\t\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
					else:
						outfile.write('\t\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
			else:
				outfile.write('\t' + str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
	else:
		outfile.write(str(riffobject[0].decode("utf-8")) + ' ' + str(riffobject[1]) + '\n')
