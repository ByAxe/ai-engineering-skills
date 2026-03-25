# Async, Concurrency, and Side Effects

Use this file when the problems involve `Future`, streams, lifecycle timing, stale requests, isolate work, or misplaced effects.

## Core rules

- Prefer `async` and `await` when they make control flow clearer.
- Avoid side effects in `build()`.
- Make loading, refresh, retry, and cancellation behavior explicit.
- Keep heavy compute off the UI isolate when it can cause jank.
- Model one-off UI reactions separately from render state.

## Smells

- `Future` chains are nested for simple sequential work.
- `Completer` appears with no strong reason.
- The same request is fired repeatedly from rebuilds.
- Request A completes after request B and overwrites newer state.
- Widgets mutate state after disposal or after losing relevance.
- JSON parsing or heavy transforms run on the main isolate during frames.
- Dialogs or navigation happen during rendering.

## Prefer `async` and `await`

### Before

```dart
Future<void> save() {
  emit(state.copyWith(status: SaveStatus.loading));

  return repository
      .save(state.form)
      .then((_) => emit(state.copyWith(status: SaveStatus.success)))
      .catchError((error) {
    emit(state.copyWith(status: SaveStatus.failure));
  });
}
```

### After

```dart
Future<void> save() async {
  emit(state.copyWith(status: SaveStatus.loading));

  try {
    await repository.save(state.form);
    emit(state.copyWith(status: SaveStatus.success));
  } catch (error, stackTrace) {
    addError(error, stackTrace);
    emit(state.copyWith(status: SaveStatus.failure));
  }
}
```

## Avoid `Completer` unless you really need to bridge callback-style APIs

A `Completer` is often a smell when plain `Future`, `async`, `await`, or a controller would be simpler.

## Do not start side effects in `build()`

### Bad

```dart
@override
Widget build(BuildContext context) {
  context.read<ProductsCubit>().loadProducts();
  return const ProductsView();
}
```

### Better

Trigger once from:

- cubit or bloc creation
- `initState`
- an explicit user action
- a lifecycle-aware coordinator

```dart
BlocProvider(
  create: (context) => ProductsCubit(context.read<ProductsRepository>())..load(),
  child: const ProductsView(),
)
```

## Stale request protection

When multiple requests can overlap, guard against late arrivals overwriting fresh data.

### Example

```dart
class SearchCubit extends Cubit<SearchState> {
  SearchCubit(this._repository) : super(const SearchState.initial());

  final SearchRepository _repository;
  int _requestId = 0;

  Future<void> search(String query) async {
    final requestId = ++_requestId;
    emit(state.copyWith(status: SearchStatus.loading, query: query));

    try {
      final results = await _repository.search(query);
      if (requestId != _requestId) return;
      emit(state.copyWith(
        status: SearchStatus.success,
        results: results,
      ));
    } catch (error, stackTrace) {
      if (requestId != _requestId) return;
      addError(error, stackTrace);
      emit(state.copyWith(
        status: SearchStatus.failure,
        errorMessage: 'Search failed',
      ));
    }
  }
}
```

## Main isolate vs helper isolate

All normal Flutter UI work happens on the main isolate. If parsing or transformation is large enough to cause visible jank, move it off the UI isolate.

Good candidates:

- large JSON parsing
- image or document processing
- long-running data transforms

Bad candidates:

- tiny lists
- quick local formatting
- logic that is only slow because it is repeated unnecessarily in `build()`

## Side effects belong in effect handlers

Good side effects include:

- navigation
- dialogs
- snackbars
- toasts
- analytics
- haptics

Place them in:

- `BlocListener`
- a dedicated effect stream
- a thin UI coordinator layer

Do not place them in pure builders or reducers.

## Async cleanup moves

- replace nested `then` chains with `async` and `await`
- remove unnecessary `Completer`
- trigger initial loads once, not from `build()`
- add stale-request protection for search or rapid refresh flows
- separate render state from one-off effect handling
- move heavy transforms off the UI isolate only when needed

## Review checklist

- Are side effects separated from rendering?
- Can requests race and overwrite each other?
- Does any async work start from `build()`?
- Is heavy work happening on the UI isolate?
- Is control flow clearer with `async` and `await`?
- Are lifecycle-sensitive operations safe?

See also:

- `references/performance-and-rebuilds.md`
- `references/bloc-and-cubit-guidelines.md`
- `references/refactoring-playbook.md`
