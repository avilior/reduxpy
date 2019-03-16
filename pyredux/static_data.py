from pyredux.actions import create_action_type


class NoSubscriptionFoundError(Exception):
    pass


class WrongFormattedReducerArgs(Exception):
    pass


initial_action_type = "__INTERNAL_INIT_REDUX_STORE"
StoreInitAction = create_action_type(initial_action_type)