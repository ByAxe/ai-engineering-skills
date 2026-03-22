# Testing and Visual Comparison

## Golden Tests

Golden tests capture widget screenshots for visual regression testing.

### Test Structure

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('FeatureName screen golden test', (WidgetTester tester) async {
    // Match Figma design dimensions
    await tester.binding.setSurfaceSize(Size(375, 812));

    await tester.pumpWidget(
      MaterialApp(
        home: YourImplementedScreen(),
      ),
    );

    await expectLater(
      find.byType(MaterialApp),
      matchesGoldenFile('goldens/feature_name.png'),
    );
  });
}
```

### Common Figma Frame Sizes

| Device | Width | Height |
|--------|-------|--------|
| iPhone SE | 375 | 667 |
| iPhone X / 11 / 12 / 13 | 375 | 812 |
| iPhone 12/13 Pro Max | 428 | 926 |
| iPhone 14 Pro | 393 | 852 |
| iPhone 15 Pro Max | 430 | 932 |
| Pixel 5 | 393 | 851 |
| Samsung Galaxy S21 | 360 | 800 |
| iPad Mini | 744 | 1133 |
| iPad Pro 11" | 834 | 1194 |
| iPad Pro 12.9" | 1024 | 1366 |

Match the test surface size to the Figma frame dimensions.

### Scrollable Content

**Finite height (scrollable but bounded):**
```dart
// Capture complete scrollable area
await tester.binding.setSurfaceSize(Size(375, 2000)); // Extend height
```

**Infinite/long lists — capture multiple scroll states:**
```dart
// Initial state
await expectLater(find.byType(MaterialApp), matchesGoldenFile('screen_top.png'));

// Scroll and capture
await tester.drag(find.byType(ListView), Offset(0, -300));
await tester.pumpAndSettle();
await expectLater(find.byType(MaterialApp), matchesGoldenFile('screen_scrolled.png'));
```

### Running Golden Tests

```bash
# Generate golden files
flutter test --update-goldens

# Run tests against golden files
flutter test
```

## App Screenshots

### iOS Simulator
```bash
xcrun simctl io booted screenshot .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

### Android Emulator
```bash
adb shell screencap -p > .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

### Screenshot Naming Convention
- Prefix: `ss_`
- Timestamp: `YYYY-MM-DD_HH-MM-SS`
- Description: brief snake_case label (e.g., `Feed_View`, `Profile_Edit`)

## Visual Comparison Checklist

### Layout (check first — highest impact)
- [ ] Widget positioning matches Figma frame positions
- [ ] Alignment (left, center, right, stretch) is correct
- [ ] Constraints (Expanded/Flexible) behave as expected
- [ ] Scroll behavior matches (if applicable)

### Typography
- [ ] Font family matches exactly
- [ ] Font size matches (check Figma uses dp, not pt)
- [ ] Font weight is correct (see weight mapping in flutter-implementation.md)
- [ ] Line height matches (`height` property = lineHeight / fontSize)
- [ ] Letter spacing matches
- [ ] Text color matches hex value exactly

### Colors
- [ ] Background colors match hex values
- [ ] Text colors match
- [ ] Border/stroke colors match
- [ ] Opacity values are correct (Figma % to Flutter 0.0-1.0)
- [ ] Gradient stops and directions match (if applicable)

### Spacing
- [ ] Padding values match (top, right, bottom, left)
- [ ] Margins match
- [ ] Gap/spacing between items matches Auto Layout spacing
- [ ] Container dimensions match

### Assets
- [ ] Images render at correct resolution
- [ ] Image aspect ratio matches
- [ ] Icons are correct size and color
- [ ] Asset paths resolve correctly

### Effects
- [ ] Border radius matches
- [ ] Box shadows match (color, offset, blur, spread)
- [ ] Opacity matches
- [ ] Blur effects applied correctly

## Iteration Strategy

1. **Round 1**: Fix major layout and positioning issues
2. **Round 2**: Address typography and colors
3. **Round 3**: Fine-tune spacing and dimensions
4. **Round 4**: Polish effects (shadows, borders, radius)
5. **Round 5**: Final pixel-perfect pass

After each round:
- Take new app screenshot
- Compare side-by-side with Figma screenshot
- Use `figma_check_design_parity` for automated comparison
- Continue until no visible differences remain

## Using figma_check_design_parity

Call `figma_check_design_parity` to get an automated comparison report. The tool analyzes:
- Layout alignment and positioning
- Color accuracy
- Typography matching
- Spacing consistency

Review the report and prioritize fixes by severity.
