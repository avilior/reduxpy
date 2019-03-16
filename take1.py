from pyrsistent import pmap
from pyredux import create_store
from pyredux import create_action_type
from pyredux.static_data import initial_action_type

"""
Using a single reducer
"""

INC_COUNTER = create_action_type("INC")
DEC_COUNTER = create_action_type("DEC")
SET_COUNTER = create_action_type("SET")
ADD_COUNTER = create_action_type("ADD")


def reducer(action, state=pmap({})):

    if action.type == initial_action_type:
        new_state = pmap({'count': 0})
        return new_state
    if isinstance(action, INC_COUNTER):
        new_state = state.set('count', state['count'] + 1)
        return new_state
    if isinstance(action, DEC_COUNTER):
        new_state = state.set('count', state['count'] - 1)
        return new_state
    if isinstance(action, SET_COUNTER):
        new_state = state.set('count', action.payload)
        return new_state
    if isinstance(action, ADD_COUNTER):
        new_state = state.set('count', state['count'] + action.payload)
        return new_state
    return state

mystore = create_store(reducer)

def subscriber(s):
    print(s.state)

mystore.subscribe(subscriber)


s = mystore.dispatch(SET_COUNTER(10))

s = mystore.dispatch(ADD_COUNTER(100))

for _ in range(10):
    s = mystore.dispatch(INC_COUNTER())

for _ in range(10):
    s = mystore.dispatch(DEC_COUNTER())

print("Done")
