# Widget and UI Smells

Use this file when the main problems are in the presentation layer: giant widgets, rebuild sprawl, styling inconsistency, or hard-to-test screens.

## Primary goal

Make widgets:

- small enough to understand quickly
- cheap enough to rebuild confidently
- local in responsibility
- easy to test in isolation

## High-signal smells

### 1. Giant `build()` methods

Symptoms:

- hundreds of lines of conditional rendering
- inline loops, mapping, sorting, and filtering
- layout, styles, and business rules mixed together
- repeated sibling blocks with tiny variations

Fix:

- extract widgets with explicit inputs
- precompute view-friendly values before the widget tree or in state
- move business rules out of widgets
- keep only presentation-specific conditionals in the tree

#### Bad

```dart
Widget build(BuildContext context) {
  final state = context.watch<OrdersBloc>().state;

  return Scaffold(
    body: Column(
      children: [
        if (state.orders.isEmpty && !state.isLoading) ...[
          const Icon(Icons.inbox),
          Text('No orders for ${state.user?.name ?? 'unknown'}'),
        ] else ...[
          for (final order in state.orders)
            Card(
              child: ListTile(
                title: Text(order.title),
                subtitle: Text(order.createdAt.toIso8601String()),
                trailing: state.canCancel(order)
                    ? ElevatedButton(
                        onPressed: () {
                          context.read<OrdersBloc>().add(OrderCancelled(order.id));
                        },
                        child: const Text('Cancel'),
                      )
                    : null,
              ),
            ),
        ],
      ],
    ),
  );
}
```

#### Better

```dart
Widget build(BuildContext context) {
  return Scaffold(
    body: BlocBuilder<OrdersBloc, OrdersState>(
      builder: (context, state) {
        if (state.status == OrdersStatus.loading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (state.orders.isEmpty) {
          return const OrdersEmptyView();
        }

        return OrdersList(
          orders: state.orders,
          canCancel: state.canCancel,
          onCancel: (orderId) {
            context.read<OrdersBloc>().add(OrderCancelled(orderId));
          },
        );
      },
    ),
  );
}
```

### 2. Helper methods that return widgets instead of extracting widgets

Helper methods often close over too much parent state and make rebuild boundaries invisible.

#### Prefer this

```dart
class BillingSummary extends StatelessWidget {
  const BillingSummary({
    super.key,
    required this.total,
    required this.tax,
  });

  final Money total;
  final Money tax;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Tax: ${tax.formatted}'),
        Text('Total: ${total.formatted}'),
      ],
    );
  }
}
```

### 3. `setState()` too high in the tree

If a tiny interaction rebuilds a huge screen, the state probably lives too high.

Fix options:

- extract a local `StatefulWidget`
- keep ephemeral UI state local
- use `ValueNotifier` or controller for small widget-scoped state
- use `BlocSelector` or smaller child widgets when the source of truth is external

### 4. Controllers and subscriptions without disposal

Watch for:

- `TextEditingController`
- `AnimationController`
- `PageController`
- `ScrollController`
- `FocusNode`
- `StreamSubscription`

If the widget owns the lifecycle, it must dispose the object.

### 5. Hard-coded presentation values everywhere

Smells:

- repeated `EdgeInsets.symmetric(horizontal: 16)` across dozens of files
- ad-hoc text styles
- inline colors instead of theme tokens
- strings scattered through widgets instead of localization

Fix:

- centralize design tokens where appropriate
- use theme extensions or small shared UI primitives
- localize user-facing strings early

### 6. UI performs work that belongs elsewhere

Smells:

- filtering, sorting, formatting, and permission rules inside widgets
- widgets knowing transport or persistence details
- error normalization in the page

Keep presentation formatting in the UI if it is truly display-specific. Move cross-screen rules or business decisions out.

## Preferred widget cleanup moves

- extract sections into widgets with narrow props
- add `const` where possible
- replace broad `context.watch` with `BlocSelector` or a narrower widget boundary
- move user messages into localization
- replace imperative child assembly with small named widgets
- make loading, empty, success, and error states explicit

## Example: clean conditional rendering

### Before

```dart
Widget build(BuildContext context) {
  if (state.isLoading) {
    return const Center(child: CircularProgressIndicator());
  } else if (state.error != null) {
    return ErrorView(message: state.error!);
  } else if (state.items.isEmpty) {
    return const EmptyView();
  } else {
    return ListView(
      children: state.items.map((e) => Text(e.name)).toList(),
    );
  }
}
```

### After

```dart
Widget build(BuildContext context) {
  switch (state.status) {
    case ItemsStatus.loading:
      return const Center(child: CircularProgressIndicator());
    case ItemsStatus.failure:
      return ErrorView(message: state.errorMessage ?? 'Unknown error');
    case ItemsStatus.empty:
      return const EmptyView();
    case ItemsStatus.success:
      return ItemsList(items: state.items);
  }
}
```

## UI-only state vs app state

Keep state local when it is temporary, visual, and does not need app-wide coordination:

- selected tab
- local animation value
- temporary expansion or visibility toggle
- a controller tied to one widget

Elevate state when it affects:

- data fetching
- navigation flow
- cross-screen consistency
- persistence
- permission or policy decisions
- business outcomes

## Review checklist

- Can the screen be read top-to-bottom without jumping through helpers?
- Are rebuild boundaries obvious?
- Are all owned controllers disposed?
- Are strings localizable?
- Are layout tokens consistent?
- Does the UI only know what it needs to know?

See also:

- `references/performance-and-rebuilds.md`
- `references/accessibility-localization-and-adaptivity.md`
- `references/idiomatic-examples.md`
