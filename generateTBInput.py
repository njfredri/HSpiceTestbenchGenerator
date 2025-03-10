import os
import json

#TODO: decide whether or not to include the signal if it is an input or output


def extractSignalNames(line: str, delimiter:str = '_bus*num*_'):
    columns = line.split('|')
    signals = {}
    for col in columns:
        words = col.strip().split('=')
        signalName = words[0]
        value = words[1]
        bitsize = len(value)
        if bitsize <= 1:
            signals[signalName] = [signalName]
        else:
            signals[signalName] = []
            for i in range(bitsize):
                delim = delimiter.replace('*num*', str(i))
                signalbit = signalName+delim
                signals[signalName].append(signalbit)
    return signals

def extractSignalValues(line: str, signalDef: dict, ignoreLength = ["time"]):
    columns = line.split('|')
    sigvals = {}
    for col in columns:
        words = col.strip().split('=')
        signalName = words[0]
        value = words[1]
        # bitsizecheck = len(signalDef[signalName])
        bitsize = len(value)

        if bitsize <= 1 or signalName.lower() in ignoreLength:
            sigvals[signalName] = value
        else:
            for i in range(bitsize):
                subsigname = signalDef[signalName][i]
                sigvals[subsigname] = value[i]
    return sigvals


def generateTBInput(infile, outfile):
    temp = open(infile)
    lines = temp.readlines()
    temp.close()

    sim_length = 0

    #extract the signal names
    signaldef = extractSignalNames(lines[0])
    signalValues = {}
    for line in lines:
        linevals = extractSignalValues(line, signaldef)
        for key in linevals.keys():
            if key in signalValues.keys():
                signalValues[key].append(linevals[key])
            else:
                signalValues[key] = [linevals[key]]
    tbinfo = {}
    tbinfo['input_signals'] = {}
    tbinfo['output_signals'] = {}
    timescale = 1000
    timeskey = ''
    for key in signalValues.keys():
        if 'time' in key.lower():
            timeskey = key
    newtime = []
    ndigits = 2

    #loop through and adjust the time scale (assume ps to ns)
    for time in signalValues[timeskey]:
        scaledtimestr = str(round(float(time)/float(timescale), ndigits))
        #go through the number string and remove any unneccessary 0's 
        if '.' in scaledtimestr:
            endindex = len(scaledtimestr)-1
            while (scaledtimestr[endindex]=='0' or scaledtimestr[endindex]=='.') and (endindex > 0):
                endindex -= 1
            scaledtimestr = scaledtimestr[0:endindex+1]
        newtime.append(scaledtimestr)
    sim_length = newtime[-1]
    print(sim_length)
    #TODO: make the input signals automatic when file format is changed
    input_signals = ['clk', 'x', 'y', 'ce_alu']

    #loop through the keys and add each signal to the appropriate dictionary
    for key in signalValues.keys():
        if 'time' in key.lower(): continue #skip time signal
        elif key in input_signals:
            if key not in tbinfo['input_signals'].keys():
                tbinfo['input_signals'][key] = []
            #loop through and add the list to the dictionary
            for i in range(len(signalValues[key])):
                tbinfo['input_signals'][key].append({'time': newtime[i], key: signalValues[key][i]})
        else:
            if key not in tbinfo['output_signals'].keys():
                tbinfo['output_signals'][key] = []
            #loop through and add the list to the dictionary
            for i in range(len(signalValues[key])):
                tbinfo['output_signals'][key].append({'time': newtime[i], key: signalValues[key][i]})

    #write the tbinfo to json
    with open(outfile, 'w+') as out:
        json.dump(tbinfo, out, indent=4)


generateTBInput("Alu_times.txt", "output.json")