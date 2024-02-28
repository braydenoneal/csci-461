# Prolog Assignment

1. Using the structures `parent(X, Y)`, `male(X)`, and `female(X)`, write a Prolog structure that defines 
   `sister(X, Y)`.

```prolog
sibling(X, Y) :- 
    parent(Z, X),
    parent(Z, Y)
    
sister(X, Y) :- 
    sibling(X, Y),
    female(X)
```

2. Using the structures `parent(X, Y)`, `male(X)`, and `female(X)`, write a structure that defines `mother(X, Y)`.

```prolog
mother(X, Y) :- 
    parent(X, Y),
    female(X)
```

3. Complete the "permutation sort" discussed in the first Prolog lecture. (i.e., `sorted (X, Y)` is `permutation (X, Y)` 
   and `sorted(Y)`)

Code

```prolog
insert(X, L, [X | L]).
insert(X, [H | T], [H | U]) :-
	insert(X, T, U).

permute([], []).
permute([H | T], L) :-
	permute(T, U),
	insert(H, U, L).

sorted([_], _).
sorted([H, N | T], L) :-
    H =< N,
    sorted([N | T], L).

sort_list(L, S) :-
    permute(L, S),
    sorted(S, _).
```

Query

```prolog
?- sort_list([4, 8, 1, 3], X)
```

Output

```prolog
X = [1, 3, 4, 8]
```
