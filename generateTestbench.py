import os
import json

#max length of time (in nano seconds)
MAXTime = 100000

def signalToString(signal: dict, prev_signal: dict, timescale:str, logical_high, setup_time) -> str:
    voltage = '0'
    if signal['value'] == '1':
        voltage = logical_high
    signalstr = str(signal['time']) + timescale + ' ' + str(voltage) + 'V '
    #if there was a change in value, a transition must be made
    if signal['value'] != prev_signal['value']:
        voltage = '0'
        if prev_signal['value'] == '1':
            voltage = logical_high
        setupStart = round((float(signal['time']) - float(setup_time)), 2)
        setupstr = str(setupStart) + timescale + ' ' + str(voltage) + 'V '
        signalstr = str(setupstr) + signalstr
    return signalstr

def generatePWL(signalValues:list, timescale:str, logical_high, setup_time) -> str:
    pwl = ''
    #assume signals are sorted for now.
    newsig = []
    voltage = '0'
    if signalValues[0]['value'] == '1':
        voltage = logical_high
    initialsignalstr = str(signalValues[0]['time']) + timescale + ' ' + str(voltage) + 'V '
    newsig.append(initialsignalstr) #add the first signal
    for i in range(1,len(signalValues)):
        curstr = signalToString(signalValues[i], signalValues[i-1], timescale, logical_high, setup_time)
        newsig.append(curstr)
    pwl = 'PWL('
    pwl += ('\n+ ').join(newsig)
    pwl += (')')
    return pwl

def generateHspiceTestbench(input, tbout):
    temp = open(input)
    tbinfo = json.load(temp)
    temp.close()

    tbLines = []

    #include the circuit file
    dutName = tbinfo['dut_name']
    tbLines.append('* HSPICE Testbench for ' + str(dutName))
    tbLines.append('.include "' + str(tbinfo['circuit_input']) + '"')
    #specify the power supply
    vdd = tbinfo['VDD']
    vdds = str(vdd)
    vss = tbinfo['VSS']
    vsss = str(vss)
    if 'V' not in vdds:
        vdds = vdds + 'V'
    if 'V' not in vsss:
        vsss = vsss + 'V'

    tbLines.append('\n\n* Power Supply ')
    tbLines.append('VDD VDD 0 ' + vdds)
    tbLines.append('VSS VSS 0 ' + vsss)

    timescale = str(tbinfo['timescale'])
    setuptime = tbinfo['transition_values']['setup_time']
    print(tbLines)

    count = 1
    for key in tbinfo['signals'].keys():
        signals = tbinfo['signals'][key]
        print(key, signals)
        pwl = generatePWL(signals, timescale, vdd, setuptime)
        print(pwl)
        full_pwl = 'V' + str(count) + ' ' + str(key) + ' 0 '+ pwl
        tbLines.append('* Input stimuli for ' + key + ' using Piecewise Linear Voltage (PWL)')
        tbLines.append(full_pwl)
        count += 1
        

    tbout = open(tbout, 'w+')
    tbout.write('\n'.join(tbLines))

if __name__ == '__main__':
    generateHspiceTestbench('example.json', 'tb.sp')
