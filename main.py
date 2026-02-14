import simulation
from visualization.timeseries import timeseries as plot_timeseries
import Models
import analysis
import sys

while(True):
    print("====DASHBOARD====")
    print("1. Deterministic FHN")
    print("2. Stochastive Additive FHN")
    print("3. Stochastive Multiplicative FHN")
    print("4. Embedded LIF")
    print("5. Exit")
    ch = int(input('Please make your choice: '))
    #stats = analysis.ensemble_stats()

    if(ch == 5):
        print("Program Terminated!")
        sys.exit()

    #count, timing,isi,cv,fano_factor = stats.trials_stats(ch)
    s = float(input("Please enter sigma value:"))
    plot_timeseries(ch,s)

    #print("Trials and Spike Count: ",count)
    #print("ISI: ",isi)
    #print("CV:",cv)
    #print("Fano Factor: ",fano_factor)
