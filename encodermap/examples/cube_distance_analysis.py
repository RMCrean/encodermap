import encodermap as em
import matplotlib.pyplot as plt


data, ids = em.misc.random_on_cube_edges(100, sigma=0.05)

dist_sig_parameters = (0.2, 3, 6, 1, 2, 6)
periodicity = float("inf")

axe = em.plot.distance_histogram(data, periodicity, dist_sig_parameters)
plt.show()
