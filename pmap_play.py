from pyrsistent import pmap, pvector, thaw, ny
from pprint import pprint
import json

m1 = pmap({'seq' : 0})

m2 = m1.transform(['data'],pvector([]), ['map'], pmap({'f':'foo'}))

pprint(thaw(m2), indent=2)

m3 = m2.transform(['map','b'],'bar')

pprint(thaw(m3), indent=2)

m4 = m3.transform(['data',0],'a', ['data',1],'b')

pprint(thaw(m4), indent=2)





