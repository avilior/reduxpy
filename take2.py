from pyrsistent import pmap
from pyredux.store import create_store
from pyredux.actions import create_action_type
from pyredux.static_data import StoreInitAction
from pyredux.reducer import default_reducer

"""
Using singleton reducer style
"""

INC_COUNTER = create_action_type("INC")
DEC_COUNTER = create_action_type("DEC")
SET_COUNTER = create_action_type("SET")
ADD_COUNTER = create_action_type("ADD")


@default_reducer
def counter_reducer(action, state=None):
    return state

@counter_reducer.register(StoreInitAction)
def _(action, state = None):
    return pmap({'count': 0, 'enabled': True })

@counter_reducer.register(INC_COUNTER)
def _(action, state):
    return state.set('count', state['count'] + 1)


@counter_reducer.register(DEC_COUNTER)
def _(action, state):
    return state.set('count', state['count'] - 1)


@counter_reducer.register(SET_COUNTER)
def _(action,state):
    return state.set('count', action.payload)


@counter_reducer.register(ADD_COUNTER)
def _(action,state):
    return state.set('count', state['count'] + action.payload)


mystore = create_store(counter_reducer)

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
