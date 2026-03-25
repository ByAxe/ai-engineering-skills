# Bloc and Cubit Guidelines

Use this file when the codebase uses `bloc`, `flutter_bloc`, or a bloc-like structure.

## The role of bloc or cubit

Bloc and cubit belong to the business-logic layer. They should translate user intent and repository output into immutable state that the UI can render.

Keep them:

- focused
- typed
- testable
- UI-agnostic where possible

## Hard rules

- Do not put one-off side effects in `BlocBuilder`.
- Do not import Flutter into business-logic components unless there is a very deliberate reason and the tradeoff is accepted.
- Do not make sibling blocs depend on each other directly.
- Do not expose custom public methods on a bloc when an event should express the intent.
- Do not let a cubit become a mini service locator or a data-access object.
- Do not emit mutable collections that are later changed in place.

## Preferred patterns

### Use `BlocBuilder` for pure rendering

The builder should be a pure function of state.

#### Bad

```dart
BlocBuilder<LoginBloc, LoginState>(
  builder: (context, state) {
    if (state is LoginSuccess) {
      Navigator.of(context).pushReplacementNamed('/home');
    }
    if (state is LoginFailure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.message)),
      );
    }
    return LoginForm(state: state);
  },
)
```

#### Better

```dart
BlocListener<LoginBloc, LoginState>(
  listenWhen: (previous, current) =>
      previous.status != current.status && current.status != LoginStatus.loading,
  listener: (context, state) {
    if (state.status == LoginStatus.success) {
      Navigator.of(context).pushReplacementNamed('/home');
    } else if (state.status == LoginStatus.failure) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.errorMessage ?? 'Login failed')),
      );
    }
  },
  child: BlocBuilder<LoginBloc, LoginState>(
    builder: (context, state) {
      return LoginForm(
        isSubmitting: state.status == LoginStatus.loading,
      );
    },
  ),
)
```

### Scope rebuilds intentionally

Use `BlocSelector`, smaller widgets, or a local `Builder` when only part of the tree depends on state.

#### Bad

```dart
class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<ProfileBloc>().state;

    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: Column(
        children: [
          Text(state.name),
          Avatar(url: state.avatarUrl),
          ExpensiveChart(data: state.statistics),
        ],
      ),
    );
  }
}
```

#### Better

```dart
class ProfileHeader extends StatelessWidget {
  const ProfileHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<ProfileBloc, ProfileState, ({String name, String avatarUrl})>(
      selector: (state) => (name: state.name, avatarUrl: state.avatarUrl),
      builder: (context, header) {
        return Column(
          children: [
            Avatar(url: header.avatarUrl),
            Text(header.name),
          ],
        );
      },
    );
  }
}
```

### Prefer `MultiBlocProvider` when it improves readability

Nested providers are easy to lose track of. Keep dependency wiring readable.

```dart
MultiBlocProvider(
  providers: [
    BlocProvider(create: (context) => AuthBloc(context.read<AuthRepository>())),
    BlocProvider(create: (context) => ThemeCubit(context.read<SettingsRepository>())),
  ],
  child: const AppView(),
)
```

### Keep bloc-to-bloc communication out of sibling business-logic components

#### Bad

```dart
class OrdersBloc extends Bloc<OrdersEvent, OrdersState> {
  OrdersBloc(this.authBloc) : super(const OrdersState.initial()) {
    _subscription = authBloc.stream.listen((authState) {
      if (authState.status == AuthStatus.signedOut) {
        add(const OrdersResetRequested());
      }
    });
  }

  final AuthBloc authBloc;
  late final StreamSubscription _subscription;
}
```

#### Better: push the interaction up to the UI layer

```dart
BlocListener<AuthBloc, AuthState>(
  listenWhen: (previous, current) => previous.status != current.status,
  listener: (context, state) {
    if (state.status == AuthStatus.signedOut) {
      context.read<OrdersBloc>().add(const OrdersResetRequested());
    }
  },
  child: const OrdersView(),
)
```

#### Better: or share a reactive repository underneath

If two features react to the same underlying stream of truth, let both blocs depend on that repository instead of each other.

## Event and state naming

Use names that describe intent and state clearly.

### Event naming

Prefer events in past tense or intent-focused phrases.

Good examples:

- `ProfileStarted`
- `SearchSubmitted`
- `RefreshRequested`
- `TodoDeleted`

Avoid vague names:

- `DoStuff`
- `Click`
- `Change`
- `Handle`

### State naming

Use nouns and well-defined variants.

Two common shapes are both valid:

1. **Single state class + status enum**
   - compact
   - easy when many fields are shared
   - less type-safe if many combinations are invalid

2. **Sealed state hierarchy**
   - more type-safe
   - clearer for mutually exclusive states
   - can become noisy if the screen has many shared fields

Choose the smallest state model that makes illegal combinations hard to represent.

## Example: status enum state

```dart
enum CheckoutStatus { initial, loading, success, failure }

class CheckoutState {
  const CheckoutState({
    this.status = CheckoutStatus.initial,
    this.summary,
    this.errorMessage,
  });

  final CheckoutStatus status;
  final CheckoutSummary? summary;
  final String? errorMessage;

  CheckoutState copyWith({
    CheckoutStatus? status,
    CheckoutSummary? summary,
    String? errorMessage,
  }) {
    return CheckoutState(
      status: status ?? this.status,
      summary: summary ?? this.summary,
      errorMessage: errorMessage,
    );
  }
}
```

## Example: sealed state hierarchy

```dart
sealed class SearchState {
  const SearchState();
}

final class SearchInitial extends SearchState {
  const SearchInitial();
}

final class SearchLoading extends SearchState {
  const SearchLoading();
}

final class SearchSuccess extends SearchState {
  const SearchSuccess(this.results);

  final List<SearchResult> results;
}

final class SearchFailure extends SearchState {
  const SearchFailure(this.message);

  final String message;
}
```

## Public API hygiene

### Bloc

A bloc should usually be driven through `add`.

#### Bad

```dart
class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0);

  void increment() => add(const CounterIncrementPressed());
}
```

#### Better

```dart
context.read<CounterBloc>().add(const CounterIncrementPressed());
```

### Cubit

A cubit may expose public methods, but those methods should be about state transitions and usually return `void` or `Future<void>`.

#### Better

```dart
class ThemeCubit extends Cubit<ThemeMode> {
  ThemeCubit() : super(ThemeMode.system);

  void setTheme(ThemeMode mode) => emit(mode);
}
```

Avoid using cubit methods as getters, repositories, or ad-hoc services.

## Common cleanup moves

- move snackbars, dialogs, navigation, analytics, and haptics from builder to listener
- split oversized state into smaller widgets and selectors
- remove direct Flutter imports from bloc or cubit
- replace one giant bloc with per-feature blocs only if the current one is clearly over-broad
- collapse over-engineered event hierarchies that provide no clarity
- add `bloc_test` coverage before changing event/state structure

## Review checklist

- Is the builder pure?
- Is the listener reserved for one-off effects?
- Is rebuild scope intentional?
- Is state immutable?
- Are event and state names meaningful?
- Do blocs depend on repositories instead of other blocs?
- Are cubit public methods narrow and state-focused?
- Are there any Flutter imports inside business logic?

See also:

- `references/flutter-architecture-principles.md`
- `references/performance-and-rebuilds.md`
- `references/testing-strategy.md`
- `references/refactoring-playbook.md`
