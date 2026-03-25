# Flutter Architecture Principles

Use this file when the main issue is structural: layering, folder layout, data flow, ownership, or over-engineering.

## Core principles

Prefer these principles in order:

1. **Separation of concerns**
   - Widgets render UI and surface user intent.
   - Business-logic components interpret intent and produce state.
   - Repositories provide the app-facing source of truth for data.
   - Data providers talk to HTTP, database, cache, plugins, or platform APIs.

2. **Unidirectional data flow**
   - User action flows inward.
   - State flows outward.
   - Avoid hidden side channels where widgets, services, and repositories all mutate the same thing independently.

3. **One source of truth per data concern**
   - If a screen shows `UserProfile`, there should be one primary owner for current profile data.
   - Derived view state is fine. Duplicated authoritative state is not.

4. **Immutable state**
   - Prefer immutable state objects and explicit transitions.
   - Make it easy to compare old and new states, reason about rebuilds, and test the flow.

5. **Architecture should fit the app**
   - Small features do not need ceremonial layers.
   - Complex business rules, cross-feature orchestration, or shared policies may justify a domain/use-case layer.

## Recommended target shapes

### Pragmatic default

Use this by default for most Flutter features:

```text
feature/
  presentation/
    account_page.dart
    account_view.dart
    account_bloc.dart
    account_state.dart
    account_listener.dart
  data/
    account_repository.dart
    account_remote_data_source.dart
    account_local_data_source.dart
    dto/
      account_dto.dart
```

Flow:

```text
Widget -> Bloc/Cubit -> Repository -> Data source -> DTO mapping -> State -> Widget
```

This is usually enough when business rules are straightforward.

### Add a domain layer only when it pays rent

Add `domain/` or `use_cases/` only when at least one of these is true:

- business rules are substantial and reused across features
- orchestration spans multiple repositories
- the same policy must be tested without UI or transport concerns
- plugin/app boundaries require stable domain contracts
- the repository interface is growing into a mini service layer

A domain layer is a **tool**, not a moral requirement.

## Smells that signal structural problems

- Repositories are bypassed from widgets for convenience.
- Data providers return transport objects directly to widgets.
- Widgets know too much about API payload structure.
- A single global bloc owns unrelated feature state.
- Feature folders exist, but shared code is still dumped into `utils/`.
- Use cases only call one repository method and add no decision logic.
- Every layer depends on `BuildContext` or Flutter types.
- Every feature defines a new abstraction "just in case".

## Good boundaries

### Widget responsibilities

Widgets should:

- render state
- translate user input into actions or events
- compose child widgets
- host ephemeral UI-only state when it is local and harmless
  - tab index
  - temporary form field controller
  - animation controller
  - expansion toggle
- delegate meaningful application logic

Widgets should not:

- parse raw JSON
- decide caching policy
- implement retries or backoff
- own cross-screen source-of-truth state
- perform network calls in `build()`

### Business-logic responsibilities

Bloc, cubit, or equivalent should:

- accept user intent
- request data from repositories
- map outcomes to state
- coordinate loading, success, failure, and refresh flows
- stay independent from Flutter widgets where possible

Business logic should not:

- directly show dialogs or snackbars
- import Flutter UI packages
- depend on sibling blocs
- leak transport types into state

### Repository responsibilities

Repositories should:

- hide transport and storage details
- merge local and remote data when appropriate
- normalize data into app-facing models
- expose the right source of truth for the app

Repositories should not:

- know about widgets
- return raw JSON if the rest of the app wants typed models
- become giant god-services for unrelated features

## Feature-first vs layer-first

Prefer **feature-first** organization once the app is larger than a toy project. It reduces distance between the pieces that change together.

### Better

```text
lib/
  features/
    auth/
      presentation/
      data/
    profile/
      presentation/
      data/
  core/
    routing/
    theme/
    networking/
```

### Usually worse once the app grows

```text
lib/
  widgets/
  pages/
  cubits/
  blocs/
  models/
  services/
  utils/
```

The second shape tends to create hidden coupling, duplicated helpers, and giant catch-all files.

## When to simplify "clean architecture"

Collapse a domain/use-case layer when:

- use cases are thin wrappers over repository calls
- nearly every class is named `SomethingUseCase` but adds no policy
- a feature takes longer to navigate than to understand
- renaming or adding fields requires touching too many pass-through types
- there is no real boundary benefit between the layers

Keep a domain layer when:

- policies are genuinely independent from widgets and transport
- business rules are complex and tested in isolation
- multiple features or platforms share the same core behavior
- the layer clarifies the flow instead of obscuring it

## Example: move logic out of a widget

### Before

```dart
class CartPage extends StatefulWidget {
  const CartPage({super.key});

  @override
  State<CartPage> createState() => _CartPageState();
}

class _CartPageState extends State<CartPage> {
  bool isLoading = false;
  String? error;
  List<CartItem> items = const [];

  Future<void> refresh() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      items = await ApiClient().fetchCart();
    } catch (e) {
      error = 'Failed to load cart';
    } finally {
      if (mounted) {
        setState(() => isLoading = false);
      }
    }
  }

  @override
  void initState() {
    super.initState();
    refresh();
  }

  @override
  Widget build(BuildContext context) {
    // ...
  }
}
```

### After

```dart
class CartCubit extends Cubit<CartState> {
  CartCubit(this._repository) : super(const CartState.initial());

  final CartRepository _repository;

  Future<void> refresh() async {
    emit(state.copyWith(status: CartStatus.loading, errorMessage: null));

    try {
      final items = await _repository.fetchCart();
      emit(state.copyWith(status: CartStatus.success, items: items));
    } catch (error, stackTrace) {
      addError(error, stackTrace);
      emit(state.copyWith(
        status: CartStatus.failure,
        errorMessage: 'Failed to load cart',
      ));
    }
  }
}
```

```dart
class CartPage extends StatelessWidget {
  const CartPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => CartCubit(context.read<CartRepository>())..refresh(),
      child: const CartView(),
    );
  }
}
```

The UI becomes easier to test and the data flow becomes explicit.

## Review checklist

- Does each important data concern have one source of truth?
- Are layer boundaries obvious from imports and file placement?
- Does the architecture reflect actual complexity instead of aspirational complexity?
- Can a new teammate trace a feature vertically without jumping through ceremony?
- If a field changes in the API, is the blast radius constrained?

See also:

- `references/bloc-and-cubit-guidelines.md`
- `references/data-layer-and-error-handling.md`
- `references/refactoring-playbook.md`
