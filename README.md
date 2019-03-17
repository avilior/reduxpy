# Introduction

The purpose of this repo is to experiment with redux in python.


# Dependecies

The code is based on [pyredux](https://github.com/peterpeter5/pyredux)

Using [pyresistent](https://github.com/tobgu/pyrsistent/) for the store. Which is not well documented.

# Questions

- Using multiple reducers, how do we refrence state in another part of the store.
- Change notification come are sent even if there is no state change.
- Change notificaiton is global, can we register for a subtree

# Investigate

1 is this usefull on the server side?
2 On server side how do we distribute across many nodes
3 Async support using Asyncio

