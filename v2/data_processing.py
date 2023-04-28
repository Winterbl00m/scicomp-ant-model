import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

raw_data = pd.read_csv('data.csv')
visits_per_min =  raw_data.diff().abs()
minutes = np.arange(visits_per_min.shape[0])

colors = ['r', 'g', 'b']
for i, col in enumerate(visits_per_min.columns):
    plt.plot(minutes, visits_per_min[col], label=col, color=colors[i % len(colors)])

# add legend, labels and title
plt.legend()
plt.xlabel('X axis label')
plt.ylabel('Y axis label')
plt.title('Title of the graph')

# show the graph
plt.show()