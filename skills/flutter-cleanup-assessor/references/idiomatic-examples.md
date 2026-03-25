# Idiomatic Flutter and Dart Examples

Use these examples when the user wants concrete before-and-after guidance.

## Example 1: Move side effects out of `BlocBuilder`

### Before

```dart
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    if (state.status == AuthStatus.authenticated) {
      Navigator.of(context).pushReplacementNamed('/home');
    }

    return LoginForm(isLoading: state.status == AuthStatus.loading);
  },
)
```

### After

```dart
BlocListener<AuthBloc, AuthState>(
  listenWhen: (previous, current) => previous.status != current.status,
  listener: (context, state) {
    if (state.status == AuthStatus.authenticated) {
      Navigator.of(context).pushReplacementNamed('/home');
    }
  },
  child: BlocBuilder<AuthBloc, AuthState>(
    builder: (context, state) {
      return LoginForm(
        isLoading: state.status == AuthStatus.loading,
      );
    },
  ),
)
```

## Example 2: Scope rebuilds with `BlocSelector`

### Before

```dart
class CartSummary extends StatelessWidget {
  const CartSummary({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<CartBloc>().state;

    return Column(
      children: [
        Text('Items: ${state.items.length}'),
        Text('Total: ${state.total.formatted}'),
      ],
    );
  }
}
```

### After

```dart
class CartItemCountText extends StatelessWidget {
  const CartItemCountText({super.key});

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
class CartTotalText extends StatelessWidget {
  const CartTotalText({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<CartBloc, CartState, Money>(
      selector: (state) => state.total,
      builder: (context, total) {
        return Text('Total: ${total.formatted}');
      },
    );
  }
}
```

## Example 3: Replace raw map state with typed models

### Before

```dart
class UserState {
  const UserState({required this.user});

  final Map<String, dynamic>? user;
}
```

### After

```dart
class UserProfile {
  const UserProfile({
    required this.id,
    required this.name,
    required this.email,
  });

  final String id;
  final String name;
  final String email;
}
```

```dart
class UserState {
  const UserState({this.profile});

  final UserProfile? profile;
}
```

## Example 4: Simple, explicit cubit state

```dart
enum ProfileStatus { initial, loading, success, failure }

class ProfileState {
  const ProfileState({
    this.status = ProfileStatus.initial,
    this.profile,
    this.errorMessage,
  });

  final ProfileStatus status;
  final UserProfile? profile;
  final String? errorMessage;

  ProfileState copyWith({
    ProfileStatus? status,
    UserProfile? profile,
    String? errorMessage,
  }) {
    return ProfileState(
      status: status ?? this.status,
      profile: profile ?? this.profile,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }
}
```

## Example 5: Sealed result object for repository outcome

```dart
sealed class SaveSettingsResult {
  const SaveSettingsResult();
}

final class SaveSettingsSucceeded extends SaveSettingsResult {
  const SaveSettingsSucceeded();
}

final class SaveSettingsFailed extends SaveSettingsResult {
  const SaveSettingsFailed(this.message);

  final String message;
}
```

```dart
Future<void> submit() async {
  emit(state.copyWith(status: SettingsStatus.saving));

  final result = await _repository.saveSettings(state.form);

  switch (result) {
    case SaveSettingsSucceeded():
      emit(state.copyWith(status: SettingsStatus.success));
    case SaveSettingsFailed(message: final message):
      emit(state.copyWith(
        status: SettingsStatus.failure,
        errorMessage: message,
      ));
  }
}
```

## Example 6: Trigger initial load once

### Before

```dart
@override
Widget build(BuildContext context) {
  context.read<FeedCubit>().load();
  return const FeedView();
}
```

### After

```dart
BlocProvider(
  create: (context) => FeedCubit(context.read<FeedRepository>())..load(),
  child: const FeedView(),
)
```

## Example 7: Better repository mapping

```dart
class TodoDto {
  const TodoDto({
    required this.id,
    required this.title,
    required this.completed,
  });

  factory TodoDto.fromJson(Map<String, dynamic> json) {
    return TodoDto(
      id: json['id'] as String,
      title: json['title'] as String,
      completed: json['completed'] as bool,
    );
  }

  final String id;
  final String title;
  final bool completed;

  Todo toModel() => Todo(
        id: id,
        title: title,
        completed: completed,
      );
}
```

```dart
class TodoRepository {
  TodoRepository(this._api);

  final TodoApi _api;

  Future<List<Todo>> fetchTodos() async {
    final jsonList = await _api.fetchTodos();
    return jsonList
        .map((json) => TodoDto.fromJson(json).toModel())
        .toList(growable: false);
  }
}
```

## Example 8: Clean extracted widget instead of helper method

### Before

```dart
Widget _buildHeader() {
  return Row(
    children: [
      CircleAvatar(backgroundImage: NetworkImage(user.avatarUrl)),
      const SizedBox(width: 12),
      Text(user.name),
    ],
  );
}
```

### After

```dart
class ProfileHeader extends StatelessWidget {
  const ProfileHeader({
    super.key,
    required this.avatarUrl,
    required this.name,
  });

  final String avatarUrl;
  final String name;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        CircleAvatar(backgroundImage: NetworkImage(avatarUrl)),
        const SizedBox(width: 12),
        Text(name),
      ],
    );
  }
}
```

## Example 9: `async` and `await` with preserved error context

```dart
Future<void> refresh() async {
  emit(state.copyWith(status: OrdersStatus.loading));

  try {
    final orders = await _repository.fetchOrders();
    emit(state.copyWith(
      status: OrdersStatus.success,
      orders: orders,
    ));
  } on SessionExpiredException {
    rethrow;
  } catch (error, stackTrace) {
    addError(error, stackTrace);
    emit(state.copyWith(
      status: OrdersStatus.failure,
      errorMessage: 'Unable to refresh orders',
    ));
  }
}
```

## Example 10: Widget test for a render branch

```dart
testWidgets('shows empty state when there are no orders', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: BlocProvider(
        create: (_) => FakeOrdersCubit.empty(),
        child: const OrdersPage(),
      ),
    ),
  );

  expect(find.text('No orders yet'), findsOneWidget);
});
```

## Example 11: Sample feature layout

```text
lib/
  features/
    orders/
      presentation/
        orders_page.dart
        orders_view.dart
        orders_bloc.dart
        orders_state.dart
        widgets/
          orders_list.dart
          orders_empty_view.dart
      data/
        orders_repository.dart
        orders_remote_data_source.dart
        dto/
          order_dto.dart
```

## Example 12: Localization-friendly button label

```dart
ElevatedButton(
  onPressed: onRetry,
  child: Text(context.l10n.retryButtonLabel),
)
```
