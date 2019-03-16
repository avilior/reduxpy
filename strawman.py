import copy
import collections
from pyredux.static_data import WrongFormattedReducerArgs

# NOT THIS ONE ...source: https://github.com/rikbruil/pyredux

#https://github.com/peterpeter5/pyredux  this is the better one.

#https://github.com/tobgu/pyrsistent


###########################################################
# Store
###########################################################


class Store(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            raise RuntimeError("Class Store is already instantiated")

    def __init__(self, reducer, initial_state):
        if not callable(reducer):
            raise AttributeError("Reducer must not be null and must be callable")
        self._state = initial_state
        self._reducer = reducer
        self._clients = []

    def get_state(self):
        return self._state   # should we return a copy of the state?


    def subscribe(self, client):
        """
               Args:
                   client: Callable which will accept two callables
                       (dispatch, get_state). These can be used to dispatch new
                       actions and retrieve the current state.

        """
        if not callable(client):
            raise TypeError

        self._clients.append(client)  # should we make this a set to no allow the same listeners

    def unsubscribe(self, client):
        try:
            self._clients.remove(client)
        except ValueError:
            return False

        return True

    def dispatch(self, action):
        """
        Dispatch the given action by calling the reducer and firing the
        listeners when complete.
        Args:
            action: A dict(-like) with a type key.
                Can contain more keys, but type is required.
        Returns:
            The action that was passed to the dispatcher
        """

        if not isinstance(action, dict):
            raise TypeError

        if not action.get('type'):
            raise TypeError

        '''
           Do i need to check this.  It should be designed not to allow this to ever happen
           
        if _state["is_dispatching"]:
            raise RuntimeError
        '''

        try:
            # should we make a copy?  we should only dispatch the changes to the state to the listeners
            # the reducer makes a copy
            returned_state = self._reducer(self._state, action)
        finally:
            #_state["is_dispatching"] = False
            pass

        if returned_state != self._state:
            self._state = returned_state
            for client in self._clients:
                client()


        return action





###########################################################
# Reducer
####################################################

def counter(count = 0, action = None):
    # count is a primitive type
    if action is None:
        return count
    if action['type'] == 'INC_COUNTER':
        return count + 1
    if action['type'] == 'DEC_COUNTER':
        return count - 1
    if action['type'] == 'ADD_COUNTER':
        return count + action['value']


def todo(todos = {}, action = None):
    if action is None:
        return todos
    if action['type'] == 'ADD':
        todos = copy.deepcopy(todos)
        todos[action['id']] = {'todo': action['todo'], 'state' : 'active'}
        return todos
    if action['type'] == 'DONE':
        todos = copy.deepcopy(todos)
        todos[action['id']]['state'] = 'done'
        return todos

#######################################################
#  Managing Reducer complexity
#######################################################
def _get_reducer_name_from_func(func):
    return func.__name__

def _determine_reducer_names_and_funcs(reducers):
    if isinstance(reducers, (collections.Mapping,)):
        reducer_names = reducers.keys()
        reducer_funcs = reducers.values()

    elif isinstance(reducers, collections.Iterable):
        reducer_names = list(map(lambda red: _get_reducer_name_from_func(red), reducers))
        reducer_funcs = reducers
    else:
        raise WrongFormattedReducerArgs(
            "Reducer-Argument has to be dict(str, func) or an iterable of funcs! Found instead: <%s>" % str(reducers))

    return reducer_names, reducer_funcs

def _get_initial_reducer_state(reducer_func):
    return reducer_func(StoreInitAction())

def combine_reducers(reducers):

    reducer_names, reducer_funcs = _determine_reducer_names_and_funcs(reducers)

    combined_initial_state = pmap(
        list(map(
            lambda red_name, red_func: (red_name, _get_initial_reducer_state(red_func)),
            reducer_names, reducer_funcs
        ))
    )

    print("x")


reducer_func_list = [counter, todo]

reducers = combine_reducers(reducer_func_list)

def  rootReducer(state, action = None):

    if action['type'] == 'INC_COUNTER':
        _state = copy.deepcopy(state)
        _state['counter'] = _state['counter'] + 1
        return _state

    if action['type'] == 'ADD_COUNTER':
        _state = copy.deepcopy(state)
        _state['counter'] = _state['counter'] + action['value']
        return _state

    return state


###########################################################
# Listeners
####################################################

def subscriber():
    print(f"[subscriber] {store.get_state()}")


initialState = {
    'counter' : 0
}


store = Store(rootReducer, initialState)
store.subscribe(subscriber)

print(store.get_state())

store.dispatch({'type':'INC_COUNTER'})
store.dispatch({'type': 'ADD_COUNTER', 'value': 10})
store.dispatch({'type': 'RESET_COUNTER'})

print("Done")


