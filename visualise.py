import numpy as np
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

### Количество наблюдений для события в виде логарифмического граифка
def number_of_events(data):
    fig = plt.figure(figsize=(10, 10))
    plot = fig.add_subplot(111)
    plot.set_yscale('log')
    plot.plot(data.index, data['count'], alpha=1)
    plot.set_ylabel('Количество записей для одного события',  fontsize = 18, color = 'black')
    plot.set_xlabel('Событие',  fontsize = 18, color = 'black')


### Визуализировать датасет

def visualise_dataset(dataset, param_x, param_y, color):
    fig = plt.figure(figsize=(10, 5))
    plot = fig.add_subplot(111)
    plot.scatter(dataset[param_x], dataset[param_y], c=dataset[color], alpha=0.1, cmap="magma")

#%%
