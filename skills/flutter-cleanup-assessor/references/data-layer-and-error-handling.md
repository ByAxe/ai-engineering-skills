# Data Layer and Error Handling

Use this file when the code smells relate to repositories, DTOs, raw maps, caching, nulls, exceptions, or leaky boundaries.

## Desired shape

```text
UI -> Bloc/Cubit -> Repository -> Data source(s)
                           |
                           +-> maps transport/storage types into app-facing models
```

## Rules

- Widgets and state objects should not depend on raw transport maps when typed models are feasible.
- Repositories should return the shape the app actually wants to consume.
- Data providers should be simple and generic.
- Business-logic components should not understand HTTP codes, SQL, or plugin response quirks.
- Expected failures should be modeled consistently.
- Preserve stack traces when rethrowing.

## Smells

- `Map<String, dynamic>` moves through the entire app.
- Repositories return DTOs directly to widgets.
- DTOs are mutated after parsing.
- `null`, `false`, or `''` indicate failure.
- `catch (e) { return null; }`
- `throw e`
- Repositories fetch the same remote/local combination in many places instead of owning it once.

## DTO vs app model

### DTO

Use for:

- JSON serialization
- database row mapping
- plugin response normalization

### App-facing model

Use for:

- repository output
- state payloads
- UI consumption
- domain rules if a domain layer exists

Keep DTOs at the transport or storage boundary.

## Example: raw map leak

### Before

```dart
class OrdersRepository {
  OrdersRepository(this._api);

  final ApiClient _api;

  Future<List<Map<String, dynamic>>> fetchOrders() async {
    final response = await _api.get('/orders');
    return List<Map<String, dynamic>>.from(response['items'] as List);
  }
}
```

```dart
class OrdersState {
  const OrdersState(this.orders);

  final List<Map<String, dynamic>> orders;
}
```

### After

```dart
class OrderDto {
  const OrderDto({
    required this.id,
    required this.title,
    required this.createdAt,
  });

  factory OrderDto.fromJson(Map<String, dynamic> json) {
    return OrderDto(
      id: json['id'] as String,
      title: json['title'] as String,
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  final String id;
  final String title;
  final DateTime createdAt;

  Order toModel() => Order(
        id: id,
        title: title,
        createdAt: createdAt,
      );
}
```

```dart
class OrdersRepository {
  OrdersRepository(this._api);

  final ApiClient _api;

  Future<List<Order>> fetchOrders() async {
    final response = await _api.get('/orders');
    final items = response['items'] as List<dynamic>;
    return items
        .map((item) => OrderDto.fromJson(item as Map<String, dynamic>).toModel())
        .toList(growable: false);
  }
}
```

```dart
class OrdersState {
  const OrdersState({required this.orders});

  final List<Order> orders;
}
```

## Error modeling

Pick one consistent approach per boundary.

### Option A: throw exceptions, map them at the boundary above

Good when:

- failures are exceptional
- repository callers already normalize state
- the app has a consistent exception policy

```dart
Future<User> loadUser() async {
  try {
    return await _repository.loadUser();
  } on SessionExpiredException {
    rethrow;
  } on ApiException catch (error, stackTrace) {
    addError(error, stackTrace);
    throw UserLoadException('Unable to load user', error);
  }
}
```

### Option B: typed result object

Good when failures are expected and part of normal control flow.

```dart
sealed class LoadProfileResult {
  const LoadProfileResult();
}

final class LoadProfileSuccess extends LoadProfileResult {
  const LoadProfileSuccess(this.profile);

  final Profile profile;
}

final class LoadProfileFailure extends LoadProfileResult {
  const LoadProfileFailure(this.message);

  final String message;
}
```

Choose one pattern consistently. Mixed patterns across one feature make control flow harder to follow.

## Caching and persistence

Repository owns cache strategy when the rest of the app should not care how data is loaded.

Bad signs:

- every caller decides whether to hit cache or network
- repository consumers re-implement stale-data checks
- local and remote merging happens in multiple screens

## Null and optional data

- Do not use nullable fields when the state machine can express absence more clearly.
- Do not encode three states in one nullable field if an enum or sealed state would be clearer.
- Do not default invalid data just to avoid handling failure.

## Preserve stack traces

### Bad

```dart
try {
  await _client.fetch();
} catch (e) {
  throw e;
}
```

### Better

```dart
try {
  await _client.fetch();
} catch (_) {
  rethrow;
}
```

Or catch a specific exception and wrap with context while keeping the cause accessible.

## Review checklist

- Are DTOs contained at the boundary?
- Does the repository expose typed, app-facing models?
- Is there one obvious source of truth for each persisted concern?
- Are failures modeled consistently?
- Are exceptions swallowed anywhere?
- Are nullable values carrying too much state meaning?

See also:

- `references/dart-language-and-api-design.md`
- `references/async-concurrency-and-side-effects.md`
- `references/idiomatic-examples.md`
