from pyrsistent import pmap, pvector, thaw, ny, inc, freeze
from pprint import pprint
import json


def add(state, payload):
    next_seq = state['seq'] + 1

    e_state = state.evolver()
    e_state['seq'] = next_seq

    e_todos = e_state['todos'].evolver()
    e_todos[next_seq] = pmap({'id': next_seq, 'todo': payload, 'state': 'active'})
    e_state['todos'] = e_todos.persistent()

    next_state = e_state.persistent()
    return next_state


#m1 = freeze({'seq' : 0, 'todos' : {} }

m1 = pmap({'seq' : 0, 'todos' : pmap({}) })

pprint(thaw(m1), indent=2)

# add a todo

m2 = add(m1, "hello")

pprint(thaw(m2), indent=2)


#m3 = m2.transform(['seq'], inc)

m3 = m2.transform(['todos',1,'state'], 'done')

#m3 = m2.transform(['todos',1,'state'], 'done')

pprint(thaw(m3), indent=2)


exit()


m3 = add(m2, "world")

pprint(thaw(m3), indent=2)


m4 = m3.transform(['todos',1,'state'], 'done')

pprint(thaw(m4), indent=2)

exit()

m2 = m1.transform(['data'],pvector([]), ['map'], pmap({'f':'foo'}))

pprint(thaw(m2), indent=2)

m3 = m2.transform(['map','b'],'bar')

pprint(thaw(m3), indent=2)

m4 = m3.transform(['data',0],'a', ['data',1],'b')

pprint(thaw(m4), indent=2)





