import  traceanalyzer as tr
import matplotlib.pyplot as plt

#end-to-end delay
eedelay1=tr.Eedelay('renoTrace.tr','0')
eedelay2=tr.Eedelay('vrgasTrace.tr','0')
# eedelay1=tr.Eedelay('renoTrace.tr','0')
# eedelay1=tr.Eedelay('renoTrace.tr','0')
eedelay2.sample()#eedelay2.sample(1.5) for sampling with step=1.5
eedelay1.plot()
eedelay2.plot()
plt.show()
#getting data
time=eedelay2.time_sample
eedelay=eedelay2.eedelay_sample
idx=0
for instant in time:
    print(instant,' ',eedelay[idx]) 
    idx+=1
