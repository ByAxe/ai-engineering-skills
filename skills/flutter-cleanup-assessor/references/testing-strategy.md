# Testing Strategy

Use this file when refactors are risky, tests are weak, or the codebase needs a cleanup safety net.

## Goal

Use tests to preserve behavior while making structure better.

A strong Flutter codebase usually has:

- many unit tests
- many widget tests
- enough integration tests to validate critical user flows

## What to test first during cleanup

Before moving structure, add characterization tests around:

- high-risk screens
- async loading and retry flows
- auth or session behavior
- navigation triggered by state changes
- repositories with mapping logic
- blocs or cubits with non-trivial transitions

## Test by layer

### Unit tests

Great for:

- repositories
- mapping and parsing
- use cases if they exist
- blocs or cubits
- small pure utilities

### Widget tests

Great for:

- rendering different states
- user interaction on a screen or reusable widget
- error, empty, loading, and success branches
- verifying localized labels, accessibility labels, and conditional UI

### Integration tests

Use for:

- app startup
- sign-in
- checkout
- critical end-to-end workflows
- flows involving navigation, plugins, or platform integration

## Bloc or cubit test example

```dart
blocTest<LoginCubit, LoginState>(
  'emits loading then success when login succeeds',
  build: () => LoginCubit(FakeAuthRepository(success: true)),
  act: (cubit) => cubit.submit(email: 'a@b.com', password: 'secret'),
  expect: () => [
    const LoginState(status: LoginStatus.loading),
    const LoginState(status: LoginStatus.success),
  ],
);
```

## Widget test example

```dart
testWidgets('shows retry button on failure', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider(
        create: (_) => FakeProductsCubit.failure(),
        child: const ProductsPage(),
      ),
    ),
  );

  expect(find.text('Retry'), findsOneWidget);
});
```

## Repository test example

```dart
test('maps DTOs into app-facing models', () async {
  final repository = OrdersRepository(FakeOrdersApi([
    {'id': '1', 'title': 'First', 'created_at': '2026-01-10T10:00:00Z'},
  ]));

  final orders = await repository.fetchOrders();

  expect(orders, hasLength(1));
  expect(orders.first.title, 'First');
});
```

## Test cleanup rules

- Add tests before large structural moves.
- Prefer deterministic tests over timing-heavy tests.
- Avoid testing implementation trivia.
- Test contracts and state transitions, not private helper names.
- Use fake repositories instead of mocking everything by default.
- Keep widget tests focused; do not turn them into brittle screenshot surrogates unless the team already uses goldens intentionally.

## Good refactor safety sequence

1. add characterization test
2. refactor one smell family
3. rerun format, analyze, tests
4. update or add one more test if the refactor clarifies a contract
5. continue

## Common gaps during Flutter cleanup

- no tests around `BlocListener`-driven navigation or messages
- widget tests that only verify "the page renders"
- repositories tested only through UI
- UI tests asserting deep implementation details
- integration tests covering trivial flows while critical flows have none

## Review checklist

- Which tests protect current behavior before refactoring?
- Is each non-trivial bloc or cubit covered?
- Are repository mappings covered?
- Do widget tests cover loading, empty, success, and failure states?
- Are critical end-to-end flows represented?
- Are tests deterministic and readable?

See also:

- `references/bloc-and-cubit-guidelines.md`
- `references/accessibility-localization-and-adaptivity.md`
- `references/refactoring-playbook.md`
