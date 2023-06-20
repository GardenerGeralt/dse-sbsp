import math

#import src.database.utils as sdbu

#data = sdbu.read()
#print(data)

Components = {}
Components['Startracker']= {
    'Onsat': 1, #(0=No,1=Yes)
    'Amount': 2,
    'Model': 'T1 Star Tracker',
    'Brand': 'Terma',
    'Weight': 0.76, #kg
    'Power Consumption': 3.3 #Watt
    }
Components['Inertial_Sensor']= {
    'Onsat': 1, #(0=No,1=Yes)
    'Amount': 2,
    'Model': 'HG9900',
    'Brand': 'Honeywell',
    'Weight': 2.7, #kg
    'Power Consumption': 10 #Watt
    }
Components['Sun_Sensor']= {
    'Onsat': 1, #(0=No,1=Yes)
    'Amount': 2,
    'Model': 'BiSon64-ET',
    'Brand': 'LensR&D',
    'Weight': 0.024, #kg
    'Power Consumption': 0 #Watt
    }
Components['Sat_Clock']= {    'Onsat': 1,  # (0=No,1=Yes)
    'Amount': 2,
    'Model': 'USO',
    'Brand': 'AccuBeat',
    'Weight': 2,  # kg
    'Power Consumption': 6.5  # Watt
    }
Components['Moon_Clock']= {
    'Onsat': 0,  # (0=No,1=Yes)
    'Amount': 1,
    'Model': 'USO',
    'Brand': 'AccuBeat',
    'Weight': 2,  # kg
    'Power Consumption': 6.5  # Watt
    }
Components['Sat_Antenna']= {
    'Onsat': 1, #(0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'AC-2000',
    'Brand': 'AAC',
    'Weight': 0.1, #kg
    'Power Consumption': 0, #Watt
    'Gain': 2 #dB
    }
Components['Moon_Antenna']= {
    'Onsat': 0, #(0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'OMNI-A0142',
    'Brand': 'Kuhne',
    'Weight': 0.2, #kg
    'Power Consumption': 0, #Watt
    'Gain': 4 #dB
    }
Components['Transmitter']= {
    'Onsat': 0, #(0=No,1=Yes)
    'Amount': 1,
    'Model': 'TX-2400',
    'Brand': 'AAC',
    'Weight': 0.07, #kg
    'Power Consumption': 2.5 #Watt
    }
Components['Receiver']= {
    'Onsat': 1, #(0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'RX-2000',
    'Brand': 'AAC',
    'Weight': 0.2, #kg
    'Power Consumption': 1.5, #Watt
    'Sensitivity': -117 #dB
    }
Components['Sat_Amplifier']= {
    'Onsat': 1, #(0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'PA LNA 200250',
    'Brand': 'Kuhne',
    'Weight': 0.11, #kg
    'Power Consumption': 0.01, #Watt
    'Gain': 35 #dB
    }
Components['Moon_Amplifier']= {
    'Onsat': 0, #(0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'PA 200270-10 A',
    'Brand': 'Kuhne',
    'Weight': 0.5, #kg
    'Power Consumption': 28, #Watt
    'Gain': 47.5 #dB
    }
Components['Telescope']= {
    'Onsat': 1,  # (0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'ADVANCED VX 700',
    'Brand': 'Celestron',
    'Weight': 8.6,  # kg
    'Power Consumption': 42,  # Watt
    }
Components['CMOS']= {
    'Onsat': 1,  # (0=No,1=Yes,2=Both)
    'Amount': 1,
    'Model': 'CABR127',
    'Brand': 'Machine Vision Store',
    'Weight': 0.09,  # kg
    'Power Consumption': 3.5,  # Watt
    }

def Getweight(Componentlist):
    Components = Componentlist
    GNC_Sat_Weight = 0
    GNC_Sat_Power = 0
    GNC_Moon_Weight = 0
    GNC_Moon_Power = 0
    for elem in Components:
        if Components[elem]['Onsat'] == 1:
            GNC_Sat_Weight += (Components[elem]['Weight'] * Components[elem]['Amount'])
            GNC_Sat_Power += (Components[elem]['Power Consumption'] * Components[elem]['Amount'])
        elif Components[elem]['Onsat'] == 0:
            GNC_Moon_Weight += (Components[elem]['Weight'] * Components[elem]['Amount'])
            GNC_Moon_Power += (Components[elem]['Power Consumption'] * Components[elem]['Amount'])
    return GNC_Sat_Power,GNC_Sat_Weight,GNC_Moon_Power,GNC_Moon_Weight

def FSPL(Altitude,frequency,): #dB, Altitude in km and frequency in GHz
    fspl = 20*(math.log10(Altitude) + math.log10(frequency)) + 92.45
    return fspl

frequency = 2.2 #GHz
Altitude = 14122 #km
fspl = FSPL(Altitude,frequency)
#RF_loss = Components['Sat_Antenna']['Gain'] + Components['Moon_Antenna']['Gain'] + Components['Moon_Amplifier']['Gain'] + Components['Sat_Amplifier']['Gain'] - FSPL(Altitude,frequency)
P_W = Getweight(Components)
print(P_W)
print('fspl',fspl)
#print('RF loss',RF_loss)

#if RF_loss >= Components['Receiver']['Sensitivity']:
#    print('loss < sensitivity')
#else:
#    print('loss too high')

#Numberofspacecraft = data['sc number']
Numberofbeacons = 3
#Total_P_W_sat = (Numberofspacecraft*P_W[0],Numberofspacecraft*P_W[1])
#Total_P_W_Moon = (Numberofbeacons*P_W[2],Numberofbeacons*P_W[3])
#print(Total_P_W_Moon)