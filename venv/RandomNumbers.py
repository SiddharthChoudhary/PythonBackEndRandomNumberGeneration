from math import log,ceil,pow
from flask import Flask, request
from flask_restful import Resource, Api
import struct
app = Flask(__name__)
api = Api(app)
lastPosition=0
lastPositionForMegaMillion=0
lastPositionForNormalDistributionFile=0
def readAfile(filename,lower_end_range,higher_end_range,amount):
    with open(filename, 'rb') as f:
        f.seek(lastPosition)
        for chunk in iter(lambda: f.read(1024), b''):
            finalrandomarray = convertHexChunktoBinaryStream(chunk,lower_end_range,higher_end_range,amount)
            if(len(finalrandomarray)==int(amount)):
                global lastPosition
                lastPosition=f.tell()
                break
    return finalrandomarray

def megamillion():
    lower_end_range = 1
    higher_end_range = 70
    amount = 5
    with open("testUniform.bin", 'rb') as f:
        f.seek(lastPositionForMegaMillion)
        for chunk in iter(lambda: f.read(100), b''):
            if(chunk==''):
                return {'finalrandomarray':['file length reached']}
            finalrandomarray = convertHexChunktoBinaryStream(chunk,lower_end_range,higher_end_range,amount)
            if(len(finalrandomarray)==5):
                global lastPositionForMegaMillion
                lastPositionForMegaMillion=f.tell()
                break
    lower_end_range=1
    higher_end_range=25
    amount=1
    with open("testUniform.bin", 'rb') as f:
        f.seek(lastPositionForMegaMillion)
        for chunk in iter(lambda: f.read(100), b''):
            if(chunk==''):
                return {'finalrandomarray':['file length reached']}
            finalrandomarrayForLastnumber = convertHexChunktoBinaryStream(chunk,lower_end_range,higher_end_range,amount)
            if(len(finalrandomarrayForLastnumber)==1):
                global lastPositionForMegaMillion
                lastPositionForMegaMillion=f.tell()
                break
    return {'finalrandomarray':finalrandomarray+finalrandomarrayForLastnumber}

class NormalDistribution(Resource):
    def get(self):
        args = request.args
        lower_end_range = int(args['lower'])
        higher_end_range = int(args['higher'])
        amount = int(args['amount'])
        maximumInTestNormalBinFile = 1000000
        divisor = maximumInTestNormalBinFile/100 #will give something like 10000, so now!
        #with open('normal1.txt', 'rb') as f:
        FinalRandomArray = []
        f = open('normal1.txt')
        #to read till end of the file to note the eof, which we can use later
        lines=f.readlines()
        eof=f.tell()
        f.seek(lastPositionForNormalDistributionFile)
        for piece in f:
            value = int((float(piece))/divisor)
            if(value>=lower_end_range and value<=higher_end_range):
                if(amount==0):
                    break
                if(amount!=0 and amount>0):
                    FinalRandomArray.append(value)
                    amount-=1
        global lastPositionForNormalDistributionFile
        #change it to 0 if we have reached to the end of the file normal1.txt
        lastPositionForNormalDistributionFile= 0 if eof==f.tell() else f.tell()
        return FinalRandomArray
     	#return {'finalrandomarray': readAfile("testNormal.bin",lower_end_range,higher_end_range,amount)}
class MegaMillion(Resource):
    def get(self):
        return megamillion()


def binaryToDecimal(n):
        return int(n,2)
#a function to convertHexaDecimal to Binarystream
def convertHexChunktoBinaryStream(inputarray,lower_end_range,higher_end_range,amount):
    binaryarray =  []
    for i in range(0,len(inputarray)):
        binaryarray.append(bin(struct.unpack('1B',inputarray[i])[0])[2:])
    binaryarray=''.join(binaryarray)
    d= startRandomizer(binaryarray,lower_end_range,higher_end_range,amount)
    for key, value in d.items():
           finalrandomarray=value
    return finalrandomarray
#a function to convertHexaDecimal to startRandomizer
def startRandomizer(inputarray,lower_end_range,higher_end_range,amount):
        lower_end_range =int(lower_end_range)
        higher_end_range=int(higher_end_range)
        amount          =int(amount)
        #range_input is the range
        range_input=higher_end_range-lower_end_range+1
        #taking the log of the range  to generate offset
        log_of_range=log(range_input,2)
        log_of_range=int(ceil(log_of_range))
        higher_end_range_represented_by_bits     =   0
        lower_end_range_represented_by_bits      =   0
        lst                                      =   []
        FinalRandomArray                         =   []
        #creating the maximum of numbers which  it can go to by saving,for ex: 2^3+2^2+2^1+2^0
	for i in range(0,(log_of_range)):
                higher_end_range_represented_by_bits+=pow(2,i)
        while True:
            i=range_input%2
            range_input=range_input/2
            lst.append(i)
            if range_input==0:
                break
        length    =   len(lst)
        #where length is equal to the window size, Inputarray - length makes it go till the end but also setting the offset else you will get an IndexoutofBound error
        for file in range(0,len(inputarray)-length,length):
            digit =[]
            for i in range(0,length):
                digit.append(inputarray[file+i])
            digit=''.join(digit)
            number=binaryToDecimal(digit)+lower_end_range
            if(number>=lower_end_range and number<=higher_end_range):
                    if(amount!=0 and amount>0):
                        FinalRandomArray.append(number)
                        amount-=1
        return {'finalrandomarray':FinalRandomArray}
class ReturnMainModule(Resource):
    def get(self):
	args = request.args
        lower_end_range = args['lower']
        higher_end_range = args['higher']
        amount = args['amount']
        finalrandomarray =readAfile("testUniform.bin",lower_end_range,higher_end_range,amount)
        return {'finalrandomarray':finalrandomarray}
api.add_resource(ReturnMainModule, '/main')
api.add_resource(MegaMillion,'/megaMillion')
api.add_resource(NormalDistribution,'/normalDistribution')
# Driver code
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5050')
