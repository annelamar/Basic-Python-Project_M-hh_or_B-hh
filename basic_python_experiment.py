import csv
import string

from expyriment import design, control, stimuli, io, misc
from random import randint
import pandas as pd
from expyriment.misc import data_preprocessing, constants
import matplotlib.pyplot as plt 


# Create and initialize an Experiment
exp = design.Experiment("Mähh and Bähh")
control.initialize(exp)
#stimuli.TextScreen("","Welcome to our experiment. This is loosely based off the Simons effect. To read more: https://en.wikipedia.org/wiki/Simon_effect#:~:text=A%20typical%20demonstration%20of%20the%20Simon%20effect%20involves,on%20the%20left%20when%20they%20see%20something%20green. You will be presented with images of either goats or sheep. React as quickly as possible. Please read the instructions beforehand carefully. Press Enter until Experiment starts. Have fun!").present


# Define and preload standard stimuli
fixcross = stimuli.FixCross()
fixcross.preload()

# Create IO
#response_device = io.EventButtonBox(io.SerialPort("/dev/ttyS1"))
response_device = exp.keyboard
task = None
# Create design
for task in ["Press the left arrow key if a goat is shown. Otherwise, press the right arrow key.", "Press the left arrow key if a sheep is shown. Otherwise, press the right arrow key."]:
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
            elif i == 2:
                #t = design.Trial()
                t.set_factor("Position", where [0])
                goat1=stimuli.Picture("higherHans.jpg", position = [where[1],0])
                goat1.preload()
                t.add_stimulus(goat1)
                b.add_trial(t, copies=1)
            elif i == 3:
                #t = design.Trial()
                t.set_factor("Position", where[0])
                sheep2 = stimuli.Picture("Ingridtanzt2.jpg", position = [where[1], 0])
                sheep2.preload()
                t.add_stimulus(sheep2)
                b.add_trial(t, copies=1)
            else:
                #t = design.Trial()
                t.set_factor("Position", where[0]) 
                goat2 = stimuli.Picture("frecherFranz.jpg", position=[where[1], 0])
                goat2.preload()
                t.add_stimulus(goat2)
                b.add_trial(t, copies=1)
    b.shuffle_trials()
    exp.add_block(b)
exp.add_bws_factor("ResponseMapping", [1, 2])
exp.data_variable_names = ["Position", "Correct_Click", "Button", "Time"]


# Start Experiment
control.start()
exp.permute_blocks(misc.constants.P_BALANCED_LATIN_SQUARE)
for block in exp.blocks:
    stimuli.TextScreen("","Welcome to our experiment. This is loosely based off the Simons effect. To read more: https://en.wikipedia.org/wiki/Simon_effect#:~:text=A%20typical%20demonstration%20of%20the%20Simon%20effect%20involves,on%20the%20left%20when%20they%20see%20something%20green. You will be presented with images of either goats or sheep. React as quickly as possible. Please read the instructions beforehand carefully. Press Enter until Experiment starts. Have fun!").present()
    stimuli.TextScreen("Instructions", block.get_factor("Response")).present()
    response_device.wait()
    # making sure the correct key is pressed 
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(1000 - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = exp.keyboard.wait([constants.K_LEFT,constants.K_RIGHT])
        if b.get_factor("Response") == "Press the left arrow key if a goat is shown. Otherwise, press the right arrow key." and button == constants.K_LEFT and (stimuli == goat1 or goat2):
            correct_click = True
        elif b.get_factor("Response") == "Press the left arrow key if a sheep is shown. Otherwise, press the right arrow key." and button == constants.K_LEFT and (stimuli == sheep1 or sheep2):
            correct_click = True
        else: 
            correct_click = False 
        
        data = exp.data.add([trial.get_factor("Position"), correct_click, button, rt])


# End Experiment
control.end("Thank you for your participation. From now on, we hope you will be able to distinguish goats and sheep more easily:)", 3000)

#turning the data into a csv file
misc.data_preprocessing.write_concatenated_data('./data', 'basic_python_experiment', output_file="python_experiment_to_csv.csv", delimiter=',', to_R_data_frame=False, names_comprise_glob_pattern=False)
#creating a dataframe show_csv in pandas, so that we can evaluate our data in the following steps
show_csv = pd.read_csv("python_experiment_to_csv.csv", sep=',' ,index_col = None, names = ["Subject ID", "Position", "Correct Key", "Button", "RT"], header=0)
show_csv.drop([0], axis=0, inplace=True)
#changing RT data to be able to work with it
show_csv['RT']=show_csv['RT'].astype(float)
print(show_csv)
print(list(show_csv.columns))

#creating the mean and median of RT for the graph 
mean_of_RT = show_csv['RT'].mean()
print(show_csv["RT"].median())
print(show_csv['RT'].mean())
print(show_csv["RT"].describe())
print(show_csv.describe())

#plotting our graph
plot = show_csv["RT"].plot(title="Needed Reaction Time throughout the experiment", xlabel="stimuli occurrence", ylabel="time in milliseconds")
fig = plot.get_figure()
plot.axhline(y=show_csv['RT'].mean(), color ='r', linestyle= '--',lw=2)
fig.savefig("output.png") # saving graph into documents 
fig.show()
#other possible graph:
#plot2= show_csv.plot(x="Correct Key", y = "RT", kind = "bar")
#fig2 = plot2.get_figure()
#fig2.savefig("output2.png")

