from pyrsistent import pmap, thaw
from pyredux.store import create_store
from pyredux.actions import create_action_type
from pyredux.static_data import StoreInitAction
from pyredux.reducer import default_reducer, combine_reducer
from pprint import pprint

"""
Using two reducers  counter application  and todo

"""

ADD_TODO  = create_action_type("ADD_TODO")
DONE_TODO = create_action_type("DONE")


@default_reducer
def todo_reducer(action, state=None):
    return state

@todo_reducer.register(StoreInitAction)
def _(action, state = None):
    return pmap({'seq' : 0, 'todos' : {} })

@todo_reducer.register(ADD_TODO)
def _(action, state):
    # { 'id' : id, 'state': "done|active", 'todo': "" }
    next_seq = state['seq'] + 1
    state.set('seq', next_seq)

    next_seq = state.get('seq') + 1

    e = state.evolver()

    e['todos'][next_seq] = {'id': next_seq, 'todo': action.payload, 'state' : 'active'}
    e['seq'] = next_seq

    m1 = e.persistent()
    return e.persistent()


@todo_reducer.register(DONE_TODO)
def _(action, state):
    return state.set('count', state['count'] - 1)



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


mystore = create_store(combine_reducer([counter_reducer, todo_reducer]))

def subscriber(s):
    pprint(thaw(s.state), indent=2)


mystore.subscribe(subscriber)


s1 = mystore.dispatch(SET_COUNTER(0))

s1 = mystore.dispatch(ADD_COUNTER(100))


for _ in range(10):
    s1 = mystore.dispatch(INC_COUNTER())
    s2 = mystore.dispatch(ADD_TODO("Say hello to the world"))




print("Done")
