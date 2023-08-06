import numpy, pyatomdb, pylab

T = 10**6.4

Z = 14

iT = 24
ihdu=iT+2

Elo=2
Ehi=10

ebins = numpy.linspace(Elo, Ehi, 10000)
en = (ebins[1:]+ebins[:-1])/2
  
linedata = pyatomdb.pyfits.open('/export1/atomdb_latest/apec_line.fits')

lineneidata = pyatomdb.pyfits.open('/export1/atomdb_latest/apec_nei_line.fits')
coconeidata = pyatomdb.pyfits.open('/export1/atomdb_latest/apec_nei_comp.fits')

ldat = linedata[ihdu].data.data
lndat = lineneidata[ihdu].data.data

dcache = {}
ionbaleq = pyatomdb.apec.solve_ionbal_eigen(Z, T, teunit='K', datacache=dcache)

init_pop = numpy.zeros(Z+1)
init_pop[0] = 1.0
ionbalnei = pyatomdb.apec.solve_ionbal_eigen(Z, T, teunit='K', datacache=dcache,\
                                             init_pop=  init_pop, tau=1e20)

for z1 in range(1,Z+2):
  ib = ionbalnei[z1-1]
  if ib < 1e-10:
    continue
    
  else:
    spec = pyatomdb.spectrum.make_ion_spectrum(ebins, ihdu, Z, z1, \
                                               linefile=lineneidata,\
                                               cocofile=coconeidata) * ib
