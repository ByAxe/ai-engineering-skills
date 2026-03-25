# Performance and Rebuilds

Use this file when the code smells include jank, broad rebuilds, expensive layout, or premature optimization.

## Primary rule

Fix the biggest obvious costs first:

1. work being repeated in `build()`
2. rebuild scope that is much larger than necessary
3. eager list construction
4. missing `const`
5. expensive render effects used casually

Do not jump to advanced caching or memoization before these are clean.

## Smells

- top-level widgets watch whole state objects
- sorting, filtering, parsing, or formatting happens inside `build()`
- lists use `children: items.map(...).toList()` for large collections
- widgets that could be `const` are not
- `Opacity`, clipping, or layer-heavy effects appear in scrolling hot paths
- a "performance fix" adds complexity but no measurement

## Keep `build()` cheap

### Bad

```dart
@override
Widget build(BuildContext context) {
  final state = context.watch<InventoryBloc>().state;
  final sorted = [...state.items]..sort((a, b) => a.name.compareTo(b.name));

  return ListView(
    children: sorted
        .map((item) => InventoryTile(item: item))
        .toList(),
  );
}
```

### Better

- sort once before emitting state, or
- store a view-friendly list in state, or
- compute only in a narrower widget if the work is truly presentation-specific

```dart
class InventoryList extends StatelessWidget {
  const InventoryList({super.key, required this.items});

  final List<InventoryItem> items;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        return InventoryTile(item: items[index]);
      },
    );
  }
}
```

## Use `const` aggressively but sanely

`const` improves intent and can reduce rebuild work for immutable widgets.

### Good

```dart
return const EmptyCartView();
```

### Also good

```dart
return Padding(
  padding: const EdgeInsets.all(16),
  child: const Text('Nothing here yet'),
);
```

Do not contort APIs just to make everything `const`, but add it wherever it is natural.

## Scope rebuilds intentionally

Prefer:

- `BlocSelector`
- smaller extracted widgets
- local `Builder`
- local state for local interactions

Avoid watching at the root of a big subtree when only one small leaf depends on the selected value.

## Use lazy list builders

Prefer:

- `ListView.builder`
- `GridView.builder`
- `SliverList`
- `SliverGrid`

Use eager `children` lists only when the item count is small and obviously bounded.

## Rendering costs

Be cautious with:

- `saveLayer`-heavy effects
- opacity on large, frequently changing subtrees
- clipping in hot paths
- large shadows or heavy blur in repeated list items

This does not mean "never use them." It means "use them intentionally and verify."

## Before optimizing deeply

Check:

- profile mode, not debug mode
- realistic device, not just emulator
- the exact interaction that feels slow
- whether the bottleneck is rebuild scope, layout, paint, image decode, or I/O

## Example: shrink rebuild scope

### Before

```dart
class CartPage extends StatelessWidget {
  const CartPage({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<CartBloc>().state;

    return Scaffold(
      body: Column(
        children: [
          Text('Items: ${state.items.length}'),
          Expanded(
            child: ListView.builder(
              itemCount: state.items.length,
              itemBuilder: (context, index) {
                return CartItemTile(item: state.items[index]);
              },
            ),
          ),
          CheckoutButton(enabled: state.canCheckout),
        ],
      ),
    );
  }
}
```

### After

```dart
class CartCountText extends StatelessWidget {
  const CartCountText({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<CartBloc, CartState, int>(
      selector: (state) => state.items.length,
      builder: (context, count) {
        return Text('Items: $count');
      },
    );
  }
}
```

```dart
class CheckoutEnabledButton extends StatelessWidget {
  const CheckoutEnabledButton({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<CartBloc, CartState, bool>(
      selector: (state) => state.canCheckout,
      builder: (context, enabled) {
        return CheckoutButton(enabled: enabled);
      },
    );
  }
}
```

Now the whole page does not need to rebuild just because one derived value changed.

## Review checklist

- Is any expensive work happening in `build()`?
- Are rebuild boundaries broader than needed?
- Are lists lazy where they should be?
- Could more widgets be `const`?
- Are render-heavy effects justified?
- Was performance work verified in profile mode?

See also:

- `references/widget-ui-smells.md`
- `references/bloc-and-cubit-guidelines.md`
- `references/testing-strategy.md`
