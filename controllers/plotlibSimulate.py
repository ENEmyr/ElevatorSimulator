import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

array = np.array(range(1, 30))

labels = ["x1"]

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9,4))

bplot1 = axes.boxplot(array, labels=labels)
axes.set_title("Rectangular box plot")

plt.show()