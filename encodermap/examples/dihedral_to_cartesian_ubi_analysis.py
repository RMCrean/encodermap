import encodermap as em
import MDAnalysis as md
import os
import numpy as np
import matplotlib.pyplot as plt


structure_path = "/home/andrejb/Research/SIMS/2017_10_20_monoUb_nat/start.pdb"
traj_path = "/home/andrejb/Research/SIMS/2017_10_20_monoUb_nat/traj.xtc"
run_id = 2
main_path = "runs/run{}".format(run_id)
step = 20000

uni = md.Universe(structure_path, traj_path)
selected_atoms = uni.select_atoms("resid 0:72 and (backbone or name O1 or name H or name CB)")
moldata = em.MolData(selected_atoms, cache_path=em.misc.create_dir("data/ubi_without_tail_bb"))

parameters = em.Parameters.load(os.path.join(main_path, "parameters.json"))
parameters.gpu_memory_fraction = 0.4
e_map = em.DihedralCartesianEncoder(parameters, moldata,
                                    checkpoint_path=os.path.join(main_path, "checkpoints",
                                                                 "step{}.ckpt".format(step)))

projected = e_map.encode(moldata.dihedrals)

fig, axe = plt.subplots()
hist, xedges, yedges = np.histogram2d(projected[:, 0], projected[:, 1], bins=300)
caxe = axe.imshow(-np.log(hist.T), origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], aspect="auto")
cbar = fig.colorbar(caxe)
cbar.set_label("-ln(p)", labelpad=0)


pdb_path = "/home/tobias/machine_learning/encodermap/pulling/runs_ubi_andrej/1ubq.pdb"
generator = em.plot.PathGenerateCartesians(axe, e_map, moldata, vmd_path="/home/soft/bin/vmd")

plt.show()