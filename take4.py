from pyrsistent import pmap, thaw, ny
from pyredux.store import create_store
from pyredux.actions import create_action_type, create_typed_action_creator
from pyredux.static_data import StoreInitAction
from pyredux.reducer import default_reducer, combine_reducer
from pprint import pprint

"""
Using two reducers  counter application  and todo
Using create action type
"""

TodoBaseType, todo_action_creator = create_typed_action_creator("TodoAction")



@default_reducer
def todo_reducer(action, state=None):
    return state

@todo_reducer.register(StoreInitAction)
def _(action, state = None):
    return pmap({'seq' : 0, 'todos' : pmap({}) })


@todo_reducer.register(TodoBaseType)
def _(action, state):

    if action.type == "ADD":
        # { 'id' : id, 'state': "done|active", 'todo': "" }
        # get the sequence and increment it

        """
        next_seq = state['seq'] + 1

        e_state = state.evolver()
        e_state['seq'] = next_seq

        e_todos = e_state['todos'].evolver()
        e_todos[next_seq] = pmap({'id': next_seq, 'todo': action.payload, 'state': 'active'})
        e_state['todos'] = e_todos.persistent()

        return e_state.persistent()
        """
        next_seq = state['seq'] + 1
        return state.transform(
            ['seq'], next_seq,
            ['todos', next_seq], pmap({'id': next_seq, 'todo': action.payload, 'state': 'active'})
        )

    if action.type == "DONE":
        return state.transform(['todos',action.payload,'state'], 'done')


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
    pprint("subscriber: Dummping state")
    pprint(thaw(s.state), indent=2)


mystore.subscribe(subscriber)


s1 = mystore.dispatch(SET_COUNTER(0))

s1 = mystore.dispatch(ADD_COUNTER(100))


for _ in range(10):
    s1 = mystore.dispatch(INC_COUNTER())


class TodoApplication(object):
    def __init__(self, store, action_creator):
        self.__store = store
        self.__action_creator = action_creator

    def addTodo(self, todo_text):
        if todo_text is not None and len(todo_text) > 0:
            action = self.__action_creator(todo_text, "ADD")
            s = self.__store.dispatch(action)

    def markAllTodosDone(self):
        # store.state rreturns all the state
        todos = self.__store.state.get('todo_reducer').get('todos')
        for id, todo in todos.items():
            if todo['state'] == 'active':
                action = self.__action_creator(id,"DONE")
                s = self.__store.dispatch(action)



todoApplication = TodoApplication(mystore, todo_action_creator)

for i in range(100):
    todoApplication.addTodo(F"Todo: item {i+1}")

todoApplication.markAllTodosDone()


print("Done")
