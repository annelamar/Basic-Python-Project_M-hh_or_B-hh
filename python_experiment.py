import csv
from expyriment import design, control, stimuli, io, misc
from random import randint
import pandas as pd
from expyriment.misc import data_preprocessing, constants
import numpy as np
#to be able to draw a plot
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import seaborn as sns



# Create and initialize an Experiment
exp = design.Experiment("Mähh and Bähh")
control.initialize(exp)



# Define and preload standard stimuli
fixcross = stimuli.FixCross()
fixcross.preload()

# Create IO
#response_device = io.EventButtonBox(io.SerialPort("/dev/ttyS1"))
response_device = exp.keyboard

task = None
# Create design
for task in ["left key for goat", "left key for sheep"]:
    b = design.Block()
    b.set_factor("Response", task)
    for where in [["left", -300], ["right", 300]]:
        for num in range(5):
            i = randint(1,4)
            t = design.Trial()
            if i == 1:
                t.set_factor("Position", where[0])
                sheep1 = stimuli.Picture("markusLanz.jpg", position=[where[1], 0])
                sheep1.preload()
                t.add_stimulus(sheep1)
                b.add_trial(t, copies=1)
            elif i ==2:
                t.set_factor("Position", where [0])
                goat1=stimuli.Picture("higherHans.jpg", position = [where[1],0])
                goat1.preload()
                t.add_stimulus(goat1)
                b.add_trial(t, copies=1)
            elif i ==3:
                t.set_factor("Position", where[0])
                sheep2 = stimuli.Picture("Ingridtanzt2.jpg", position = [where[1], 0])
                sheep2.preload()
                t.add_stimulus(sheep2)
                b.add_trial(t, copies=1)
            else:
                t.set_factor("Position", where[0]) 
                goat2 = stimuli.Picture("frecherFranz.jpg", position=[where[1], 0])
                goat2.preload()
                t.add_stimulus(goat2)
                b.add_trial(t, copies=1)
    b.shuffle_trials()
    exp.add_block(b)
exp.add_bws_factor("ResponseMapping", [1, 2])
exp.data_variable_names = ["Position", "Correct_Click", "Button", "RT"]

# Start Experiment
control.start()
exp.permute_blocks(misc.constants.P_BALANCED_LATIN_SQUARE)
for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("Response")).present()
    response_device.wait()
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(1000 - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = response_device.wait()
        if b.get_factor("Response") == "left key for sheep" and button ==constants.K_LEFT and (stimuli == goat1 or goat2):
            correct_click = True
        elif b.get_factor("Response") == "left jey for sheep" and button == constants.K_LEFT and (stimuli == goat1 and goat2):
            correct_click = True
        else:
            correct_click = False
            
        data = exp.data.add([trial.get_factor("Position"), correct_click, button, rt])


# End Experiment
control.end()
#transcripting xpd-files into one csv-file
misc.data_preprocessing.write_concatenated_data('./data', 'python_experiment', output_file="C:/Users/Anne/Documents/Studium/Mähh_or_Bähh/python_experiment_to_csv.csv", delimiter=',', to_R_data_frame=False, names_comprise_glob_pattern=False)
#creating a dataframe show_csv in pandas, so that we can evaluate our data in the following steps

show_csv = pd.read_csv("C:/Users/Anne/Documents/Studium/Mähh_or_Bähh/python_experiment_to_csv.csv", sep=',' ,index_col = None, names = ["Subject ID", "Position", "Correct Key", "Button", "RT"], header=0)
show_csv.drop([0], axis=0, inplace=True)
show_csv['RT']=show_csv['RT'].astype(float)
print(show_csv)
print(list(show_csv.columns))
#show_csv['RT'] = pd.to_numeric(show_csv['RT'])

print("Calculated median for the Reaction Time (short: RT):",show_csv["RT"].median())
mean_of_RT =show_csv['RT'].mean()
print("Calculation of the average reaction time RT:",mean_of_RT)
#print(show_csv.columns.values)
#print("Description of the needed reaction time" , show_csv["RT"].describe)
#print(show_csv.describe())
print("Description of the column 'RT':",show_csv["RT"].describe())
print("Description of our dataframe:",show_csv.describe())

#show_csv["RT"].plot(x="Number of runs", y= "time in milliseconds")
#plt.show()

#plt.savefig(sys.stdout.buffer)
#sys.stdout.flush()
#plt.plot(show_csv["RT"])

#df= pd.read_csv('python_experiment_to_csv.csv') 
#df.plot(kind='scatter', x= 'Button', y ='RT')

"""plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
columns = ['Subject ID','Position', 'Correct_Click', 'Button', 'RT']
df = pd.read_csv("python_experiment_to_csv.csv", usecols=columns)

df.plot
plt.show()"""

plot = show_csv["RT"].plot(title="Needed Reaction Time throughout the experiment", xlabel="stimuli occurrence", ylabel="time in milliseconds")
fig = plot.get_figure()
fig.savefig("output.png")

plot2= show_csv.plot(x="Correct Key", y = "RT", kind = "bar")
fig2 = plot2.get_figure()
fig2.savefig("output2.png")

fig,ax = plt.subplots()
for key, group in show_csv.groupby('Correct Key'):
    group.plot('Subject ID','RT',label=key,ax=ax)

y_avg = mean_of_RT * len('Subject ID') 
plt.plot('Subject ID', y_avg, color='r', label="average plot")

plt.legend(loc=0)
print(y_avg)
print(mean_of_RT)
#plt.plot(mean_of_RT)
#plt.xlim(0,63)
plt.show()

