import os, sys



REPO_PARENT_DIR = "../run_FTDP"
# REPO_PARENT_DIR = "../run"
# REPO_PARENT_DIR = "./test"
TEMPLATE='./go_.sh'



N_THREAD_LIST=[i*2 for i in range(4, 29)]
# N_THREAD_LIST=[2, 4]

job_cnter=0
for thread in N_THREAD_LIST:
    job_cnter+=1
    run_cfg = {
        # 'flags': 'granularity=fine,compact',
        # 'flags': 'granularity=fine,balanced',
        'flags': 'granularity=fine,scatter',
        'thread': thread,
    }

    _from = TEMPLATE
    if(job_cnter<10):
        _to = os.path.join(REPO_PARENT_DIR, 'go_0%d.sh'%(job_cnter))
    else:
        _to = os.path.join(REPO_PARENT_DIR, 'go_%d.sh'%(job_cnter))

    print(thread)

    with open(_from, 'r') as f_from, open(_to, 'w') as f_to:
        line_raw=f_from.readline()
        while line_raw:
            line=line_raw.split()
            #set thread
            if len(line)==3 and line[2]=='thread=':
                line_raw=line_raw.strip()+"%d\n"%run_cfg['thread']
            #set output
            if len(line)==2 and line[0]=='#PJM' and line[1]=='-o':
                line_raw=line_raw.strip()+" core%d.lst\n"%run_cfg['thread']
            #set omp flags
            if len(line)==2 and line[0]=='export' and line[1]=='KMP_AFFINITY=':
                line_raw=line_raw.strip()+"%s\n"%run_cfg['flags']


            f_to.write(line_raw)
            line_raw=f_from.readline()
