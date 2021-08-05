import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


CSV_FILE = './saved/result_wo_FTDP.csv'
CSV_FILE = './saved/result.csv'
IM_SAVE_DIR = './plot'



data_df = pd.read_csv(CSV_FILE)

fig1 = plt.figure()
ax1= fig1.add_subplot(111)

entry = data_df[data_df.compact]
entry = entry[entry.first_touch==False]
entry = entry[entry.config_ID==3]
# entry = entry[entry.thread>7]
ax1.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'bo--', label="compact")

entry = data_df[data_df.balanced]
entry = entry[entry.first_touch==False]
entry = entry[entry.config_ID==3]
# entry = entry[entry.thread>7]
ax1.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'ro--', label="balanced")

entry = data_df[data_df.scattered]
entry = entry[entry.first_touch==False]
entry = entry[entry.config_ID==3]
# entry = entry[entry.thread>7]
ax1.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'go--', label="scattered")

ax1.set_yscale('log')
ax1.legend()
# ax1.set_yticks([i for i in range(1, 19)])
# ax1.set_yticks(minor=True)
ax1.grid()
ax1.set_xlabel("#threads")
ax1.set_ylabel("runtime (s)")
ax1.set_title("Runtime without First Touch Placement ($256^3$)")

fig1.savefig(os.path.join(IM_SAVE_DIR, "larger_size_original_with_dyn_init.jpg"))

fig2 = plt.figure()
ax2= fig2.add_subplot(111)

entry = data_df[data_df.compact]
entry = entry[entry.first_touch==False]
entry = entry[entry.config_ID==3]
entry = entry[entry.thread>7]
ax2.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'bo--', label="original w dyn. init.")

entry = data_df[data_df.compact]
entry = entry[entry.first_touch==True]
entry = entry[entry.config_ID==4]
entry = entry[entry.thread>7]
ax2.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'ro--', label="FTDP optimized")

ax2.set_yscale('log')
ax2.legend()
# ax1.set_yticks([i for i in range(1, 19)])
# ax1.set_yticks(minor=True)
ax2.grid()
ax2.set_xlabel("#threads")
ax2.set_ylabel("runtime (s)")
ax2.set_title("Runtime of original vs FTDP ($256^3$ on compact)")

fig2.savefig(os.path.join(IM_SAVE_DIR, "optimize_256_comp.jpg"))

fig3 = plt.figure()
ax3= fig3.add_subplot(111)

entry = data_df[data_df.balanced]
entry = entry[entry.first_touch==False]
entry = entry[entry.config_ID==3]
entry = entry[entry.thread>7]
ax3.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'bo--', label="original w dyn. init.")

entry = data_df[data_df.balanced]
entry = entry[entry.first_touch==True]
entry = entry[entry.config_ID==4]
entry = entry[entry.thread>7]
ax3.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'ro--', label="FTDP optimized")

ax3.set_yscale('log')
ax3.legend()
# ax3.set_yticks([i for i in range(1, 19)])
# ax3.set_yticks(minor=True)
ax3.grid()
ax3.set_xlabel("#threads")
ax3.set_ylabel("runtime (s)")
ax3.set_title("Runtime of original vs FTDP ($256^3$ on balanced)")

fig3.savefig(os.path.join(IM_SAVE_DIR, "optimize_256_bala.jpg"))

fig4 = plt.figure()
ax4 = fig4.add_subplot(111)

entry = data_df[data_df.scattered]
entry = entry[entry.first_touch==False]
entry = entry[entry.config_ID==3]
entry = entry[entry.thread>7]
ax4.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'bo--', label="original w dyn. init.")

entry = data_df[data_df.scattered]
entry = entry[entry.first_touch==True]
entry = entry[entry.config_ID==4]
entry = entry[entry.thread>7]
ax4.plot(entry.thread.to_numpy(), entry.runtime_avg.to_numpy(),
        'ro--', label="FTDP optimized")

ax4.set_yscale('log')
ax4.legend()
# ax3.set_yticks([i for i in range(1, 19)])
# ax3.set_yticks(minor=True)
ax4.grid()
ax4.set_xlabel("#threads")
ax4.set_ylabel("runtime (s)")
ax4.set_title("Runtime of original vs FTDP ($256^3$ on scatter)")

fig4.savefig(os.path.join(IM_SAVE_DIR, "optimize_256_scat.jpg"))

plt.show()
