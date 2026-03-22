# Flutter Implementation Patterns

## Asset Management

### 1. Analyze Existing Asset Structure

Before exporting or copying assets, examine the app's current asset organization.

Check directory structure:
```bash
ls -la assets/
```

**Common patterns:**

**Pattern A: Multi-directory (Flutter resolution-aware)**
```
assets/
assets/2x/
assets/3x/
assets/4x/
```
Flutter automatically picks the appropriate resolution based on device pixel ratio.

**Pattern B: Single directory with explicit scale**
```
assets/
```
Code uses explicit `scale` parameter:
```dart
Image.asset('assets/image.png', scale: 4)
```

**Pattern C: No standard structure**
New project or inconsistent. Establish 3x as default.

### 2. Determine Required Scales

Search for scale usage in code:
```bash
grep -r "Image\.asset.*scale:" lib/
```

**Decision matrix:**
- `scale: 4` found frequently: app uses 4x assets
- `scale: 3` found: app uses 3x assets
- No scale parameter found: likely multi-directory approach
- Mixed values: understand context per use case

### 3. Export Assets via figma-console-mcp

Use `figma_get_component_image` for each image asset:
- Specify `nodeId` of the image element
- Set `scale` matching the app's convention
- Set `format` to png (or svg for vector icons)

### 4. Organize and Rename Assets

**Multi-directory structure:**
```bash
# Save each scale to corresponding directory
cp exported_2x.png assets/2x/profile_avatar.png
cp exported_3x.png assets/3x/profile_avatar.png
```

**Single directory with scale:**
```bash
# Save only the required scale
cp exported_4x.png assets/profile_avatar.png
# Code: Image.asset('assets/profile_avatar.png', scale: 4)
```

**Naming conventions:**
- Use snake_case: `profile_avatar.png`, not `ProfileAvatar.png`
- Be descriptive: `feed_empty_state.png`, not `image1.png`
- Include context when needed: `onboarding_step_1_illustration.png`

### 5. Maintain Asset Mapping

Track Figma-to-app asset mapping in `.ui-workspace/$FEATURE/design_data/asset_mapping.json`:
```json
{
  "123:456_user_avatar": {
    "figma_node_id": "123:456",
    "figma_name": "user_avatar",
    "app_path": "assets/profile_avatar.png",
    "scale": "3x"
  }
}
```

### 6. Update pubspec.yaml

**Multi-directory:**
```yaml
flutter:
  assets:
    - assets/
    - assets/2x/
    - assets/3x/
```

**Single directory:**
```yaml
flutter:
  assets:
    - assets/
```

## Translating Figma Properties to Flutter

### Colors
- Figma hex `#FF5733` with opacity 80% becomes:
  ```dart
  Color(0xCCFF5733) // alpha = 0.8 * 255 = 204 = 0xCC
  ```
- Prefer app theme colors when they match design tokens

### Typography
Map Figma text properties to Flutter TextStyle:
```dart
TextStyle(
  fontFamily: 'Inter',         // from figma_get_styles
  fontSize: 16,                 // font size in dp
  fontWeight: FontWeight.w600,  // Figma "Semi Bold" = w600
  height: 1.5,                  // line height / font size
  letterSpacing: -0.2,          // letter spacing in dp
  color: Color(0xFF1A1A1A),
)
```

**Figma weight mapping:**
| Figma Weight | Flutter FontWeight |
|---|---|
| Thin | w100 |
| Extra Light | w200 |
| Light | w300 |
| Regular | w400 |
| Medium | w500 |
| Semi Bold | w600 |
| Bold | w700 |
| Extra Bold | w800 |
| Black | w900 |

### Layout and Spacing
- Figma Auto Layout `horizontal` = `Row`
- Figma Auto Layout `vertical` = `Column`
- Figma "Hug contents" = default sizing (no explicit size)
- Figma "Fill container" = `Expanded` or `Flexible`
- Figma "Fixed" = explicit `width`/`height`
- Figma padding = `EdgeInsets.fromLTRB(left, top, right, bottom)`
- Figma item spacing = `MainAxisAlignment.spaceBetween` or `SizedBox` gaps

### Constraints and Responsive Layout
- Figma "Scale" constraint: use `FractionallySizedBox` or `LayoutBuilder`
- Figma "Center" constraint: `Center` or `Alignment.center`
- Figma "Left & Right" (stretch): `Expanded` in a Row, or explicit width with constraints

### Borders and Effects
- Figma border radius = `BorderRadius.circular(value)` or `.only()`
- Figma drop shadow = `BoxShadow(color, offset, blurRadius, spreadRadius)`
- Figma inner shadow = not directly supported; use gradient overlay or custom painter
- Figma stroke = `Border` or `BoxDecoration` border property

### Component Patterns
- Figma Component = Flutter StatelessWidget or StatefulWidget
- Figma Variant = Flutter widget with constructor parameters
- Figma Instance = Flutter widget instantiation with specific props
- Figma Component Property = Flutter constructor parameter
