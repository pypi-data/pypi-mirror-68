import pylab, numpy

def getdata(fname):
  a = numpy.loadtxt(fname)
  kt = a[:,0]
  emiss = a[:,1:]
  sumemiss = emiss.sum(1)
  
  return(kt,sumemiss)
  

fig = pylab.figure()
fig.show()
ax = fig.add_subplot(111)

kt,d = getdata('output.txt')
kt,d11 = getdata('output_nei_1e11.txt')
kt,d12 = getdata('output_nei_1e12.txt')
kt,d13 = getdata('output_nei_1e13.txt')
kt,d20 = getdata('output_nei_1e20.txt')

ax.plot(kt, d, label='Equilibrium')
ax.plot(kt, d11, label='Tau=1e11')
ax.plot(kt, d12, label='Tau=1e12')
ax.plot(kt, d13, label='Tau=1e13')
ax.plot(kt, d20, label='Tau=1e20')
ax.legend(loc=0)

pylab.draw()
zzz=input()
