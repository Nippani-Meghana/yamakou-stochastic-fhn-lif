import simulation
import visualization
import Models
import analysis

stats = analysis.ensemble_stats()
count, timing = stats.trials()

print("Trials and Spike Count: ",count)
