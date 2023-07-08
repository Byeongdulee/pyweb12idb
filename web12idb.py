import matplotlib.pyplot as plt
import requests
import numpy as np
import re
import os

global data
global saxs
global waxs


def get(mydir, fileindex, extn=-1):
    global data
    data = _get(mydir, fileindex, extn)

def _get(mydir, fileindex, extn=-1):
    # when extn is -1, all files with the same fileindex will be downloaded, but it cannot be more than 38 files due to memory issue
    if type(extn) == int:
        if extn == -1:
            findex = str(fileindex)
        else:
            findex = "%i.%i"%(fileindex, extn)
    if type(extn) == list:
        findex = "%i.["% fileindex
        for ext in extn:
            findex = "%s%i;"%(findex, ext)
        findex = findex[0:-1]+"]"
        print(findex)
    url = f"https://12idb.xray.aps.anl.gov/PVapp/getdata:dir={mydir},findex={findex}"
    dt = requests.get(url)
    myd = dt.json()
    dt = myd["data"]
    return dt

def save(folder='', extn = -1):
    fn, saxs, waxs = splitdata(extn)   
    mypath = os.path.abspath(folder)
    for i in range(len(fn)):
        sfn = os.path.join(mypath, fn[i][:-3]+'dat')
        wfn = os.path.join(mypath, 'W'+fn[i][1:-3]+'dat')
        np.savetxt(sfn, saxs[i], fmt = '%.8e', delimiter=' ', newline='\n')
        np.savetxt(wfn, waxs[i], fmt = '%.8e', delimiter=' ', newline='\n')

def splitdata(extn = -1):
    global data
    global saxs
    global waxs    

    saxs = []
    waxs = []
    filename = []
    datanum = 0
    if type(extn) == int:
        if extn == -1:
            if len(data)>1:
                num = range(len(data))
                datanum = len(num)
            else:
                num = 0
                datanum = 1
        else:
            num = extn
            datanum = 1
    else:
        num = extn
        datanum = len(num)

    if datanum > 1:
        for k in range(len(num)):
            dt = data[num[k]]
            filename.append(dt['filename'])
            sd = dt['saxs']
            wd = dt['waxs']
            sdata = []
            wdata = []
            for i in range(len(sd['q'])):
                sdata.append([sd['q'][i],sd['intensity'][i],sd['errorbar'][i]])
            for i in range(len(wd['q'])):
                wdata.append([wd['q'][i],wd['intensity'][i],wd['errorbar'][i]])
            saxs.append(np.array(sdata))
            waxs.append(np.array(wdata))
        return filename, saxs, waxs
    sdata = []
    wdata = []
    dt = data[num]
    filename = [dt['filename']]
    sd = dt['saxs']
    wd = dt['waxs']
    for i in range(len(sd['q'])):
        sdata.append([sd['q'][i],sd['intensity'][i],sd['errorbar'][i]])
    for i in range(len(wd['q'])):
        wdata.append([wd['q'][i],wd['intensity'][i],wd['errorbar'][i]])
    saxs = [np.array(sdata)]
    waxs = [np.array(wdata)]
    return filename, saxs, waxs

def plot(extn = -1):
    global data
    fn, sd, wd = splitdata(extn)
    try:
        plotdata(sd, wd, fn)
    except:
        del(data[-1])
    plt.show()

def plotdata(saxs, waxs, fn, qmin=0, qmax=3):
    num_plots = len(saxs)
    colormap = plt.cm.gist_ncar
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0,1,num_plots))))
    labels = []
    m = 0
    for sd in saxs:
        # convert 0 values to nan so it does not show up in the plot
        res = np.where(sd[:,1]==0)
        sd[res[0][:], 1]=np.nan
        # plot
        plt.loglog(sd[:,0], sd[:,1])
        fnser = re.search('(.*)_(.*)_(.*).tif', fn[m])
        labels.append(int(fnser.group(3)))
        m = m+1
    for wd in waxs:
        # convert 0 values to nan so it does not show up in the plot
        res = np.where(wd[:,1]==0)
        wd[res[0][:], 1]=np.nan
        # plot
        plt.loglog(wd[:,0], wd[:,1])
    if qmin!=0:
        plt.gca().set_xlim([qmin, qmax])
    plt.legend(labels)
    plt.title('%s_%s'%(fnser.group(1), fnser.group(2)))
    return plt.gcf()