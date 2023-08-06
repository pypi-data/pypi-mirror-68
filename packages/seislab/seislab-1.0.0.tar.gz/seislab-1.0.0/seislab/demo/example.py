import seislab as sb
import numpy as np

# rea data from d a segy
segyfile = './seismic.segy'
npydata, info = sb.io.readSeis3DMatFromSegyNoInfo(segyfile=segyfile)
print(np.shape(npydata))


# write data into segy
refsegy = './seismic.segy'
optfile = './seismic_reverse.segy'
sb.io.writeSeis3DMatToSegyWithRef(seis3dmat=npydata * -1.0,
                                  seisfile=optfile,
                                  refsegy=refsegy)