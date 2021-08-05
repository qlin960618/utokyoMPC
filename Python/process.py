import numpy as np
import os, sys
import pandas as pd



# REPO_PARENT_DIR = "../run"
REPO_PARENT_DIR = "../run_FTDP"

# RESULT_LST = "run/core52.lst"

N_RUN=5


PD_FIELDS = ['thread', 'first_touch', 'compact', 'balanced', 'scattered',
            'config_ID', 'cnv_step', 'phi_final', 'matched',
            *['runtime_%d'%(i+1) for i in range(N_RUN)],  'runtime_avg']

SAVED_CSV = "./saved/result.csv"

def main():
    N_THREAD_LIST=[i*2 for i in range(4, 29)]

    for t in N_THREAD_LIST:
        RESULT_LOCATION = os.path.join(REPO_PARENT_DIR, "core%d.lst"%t)
        run_setting_cfg = {
            'thread': t,
            'first_touch': True,
            'compact':False,
            'balanced':False,
            'scattered':True,
            'config_ID':4,
        }

        read_file(run_setting_cfg, RESULT_LOCATION, override=True)
        # read_file(run_setting_cfg, RESULT_LOCATION, override=False)




def read_file(cfg, file_name, override=False):
    runtime = np.zeros(N_RUN, dtype=np.float64)
    cnv_step = np.zeros(N_RUN, dtype=np.int32)
    phi_final = np.zeros(N_RUN, dtype=np.float64)
    ind=0
    next_con=False
    with open(file_name, 'r') as f:
        line=f.readline()
        while line:
            lst=line.split()
            # print(lst)
            if(len(lst)==3 and lst[2]=='(solver)'):
                next_con=True
                runtime[ind]=float(lst[0])
            elif next_con:
                next_con=False
                phi_final[ind]=float(lst[1])
                ind+=1
            else:
                cnv_step[ind]=int(lst[0])

            line=f.readline()

    print("runtime: %s"%str(runtime))
    print("cnv_step: %s"%str(cnv_step))
    print("phi_final: %s"%str(phi_final))

    # runtime=np.array([2.3, 2.1, 2.0, 1.9, 2.1])
    # cnv_step=np.array([826, 826, 826, 826, 826])
    # phi_final=np.array([1.459831e+04, 1.459831e+04, 1.459831e+04, 1.459831e+04, 1.459831e+04])

    add_result(cfg, cnv_step, phi_final, runtime, override=override)


def add_result(cfg, cnv_step, phi_final, runtime, override=False):
    if os.path.isfile(SAVED_CSV):
        data_df = pd.read_csv(SAVED_CSV)
    else:
        data_df = pd.DataFrame(columns=PD_FIELDS)
        print("csv doesnot exist, creating new")


    #check for if run is consistance
    matched = True
    for i in range(1, cnv_step.size):
        if cnv_step[0]!=cnv_step[i]:
            print("convergence steps mismatched")
            matched = False
    for i in range(1, phi_final.size):
        if phi_final[0]!=phi_final[i]:
            print("Final Phi mismatched")
            matched = False

    ind_pre = np.array([i for i in range(data_df.shape[0])], dtype=np.int64)
    for key in cfg.keys():
        ind=data_df[cfg[key] == data_df[key]].index
        ind_pre=np.intersect1d(ind, ind_pre)

    ind=ind_pre.tolist()

    if ind and not override:
        print("DUPLICATED RUN: run result already exist, will not replace")
        return
    else:
        if override and ind:
            print("overridding enable, dropping selected row: %s"%str(ind))
            data_df = data_df.drop(ind)


        # PD_FIELDS = ['thread', 'first_touch', 'compact', 'cnv_step', 'phi_final', 'matched',
                    # 'runtime1',  'runtime2',  'runtime3',  'runtime4',  'runtime5',  'runtime_avg']
        data_df = data_df.append(pd.DataFrame([[*[cfg[key] for key in cfg.keys()],
                                cnv_step[0], phi_final[0], matched,
                                *runtime.tolist(),
                                np.average(runtime) ]], columns=PD_FIELDS))

    print(data_df)
    ##save data
    data_df.to_csv(SAVED_CSV, index=False)


if __name__=='__main__':
    main()
