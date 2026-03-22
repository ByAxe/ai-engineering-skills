---
name: figma-to-flutter
description: Converts Figma designs to pixel-perfect Flutter code using figma-console-mcp for direct Figma Desktop access. Use when user says "convert this Figma design to Flutter", "run Figma workflow", "implement this Figma screen", provides Figma links requesting Flutter implementation, or asks to "build this screen from Figma". Requires figma-console-mcp server connected to Figma Desktop.
license: MIT
metadata:
  author: ByAxe
  version: 2.0.0
  mcp-server: figma-console
  category: workflow
  tags: [figma, flutter, design-to-code, ui-implementation, mcp, pixel-perfect]
---

# Figma to Flutter

Convert Figma designs into pixel-perfect Flutter code via figma-console-mcp. Extracts design metadata directly from Figma Desktop, generates reference values, exports assets, implements UI, and iteratively validates until implementation matches design.

## Important

- CRITICAL: Verify figma-console-mcp connection before starting any workflow
- Always use `figma_get_status` first to confirm Figma Desktop is connected and the correct file is open
- Never copy generated/reference code directly into production — use it for values only (colors, sizes, spacing)
- Write Flutter code following the app's existing conventions
- Test incrementally, not at the end

## Instructions

### Step 1: Verify Connection and Prepare Workspace

1. Check figma-console-mcp connection:
   - Call `figma_get_status` — must show `Connected` status and correct file name
   - If not connected, ask user to open the Figma file and run the Figma Console MCP plugin
   - If connection fails, consult `references/troubleshooting.md`

2. Determine feature name from branch name, conversation context, or ask user

3. Create workspace at git repo root:
   ```bash
   mkdir -p .ui-workspace/$FEATURE/{figma_screenshots,app_screenshots,design_data}
   ```

4. Exclude workspace from git:
   ```bash
   grep -q "^\.ui-workspace/$" .git/info/exclude || echo ".ui-workspace/" >> .git/info/exclude
   ```

### Step 2: Extract Design Metadata from Figma

Run these figma-console-mcp calls to gather all design information. Execute independent calls in parallel.

**2a. Navigate to the target frame/page:**
- Call `figma_navigate` with the Figma URL or node ID the user provided
- Call `figma_get_selection` to confirm the correct node is selected

**2b. Capture design screenshot (visual reference):**
- Call `figma_take_screenshot` with `scale: 2` for high quality
- Save the returned image URL to `.ui-workspace/$FEATURE/figma_screenshots/`

**2c. Extract design data (run in parallel):**
- Call `figma_get_file_data` to get the full node tree with layout, constraints, and hierarchy
- Call `figma_get_styles` to extract all text styles, color styles, and effect styles used
- Call `figma_get_design_system_summary` to understand the design system context
- If specific components are used, call `figma_search_components` then `figma_get_component_details` for each

**2d. Extract development-ready specs for key components:**
- Call `figma_get_component_for_development` on components that need implementation
- This returns dimensions, padding, colors, typography, and constraints in a dev-friendly format

**2e. Extract design tokens (if available):**
- Call `figma_get_variables` to get design tokens (colors, spacing, typography scales)
- Call `figma_get_token_values` for resolved token values across modes (light/dark)

Save all extracted data to `.ui-workspace/$FEATURE/design_data/` as JSON for reference.

### Step 3: Implement Flutter UI

**3a. Analyze asset requirements first:**
- Check existing `assets/` directory structure in the Flutter project
- Search for `Image.asset` calls to identify the scaling strategy used
- Consult `references/flutter-implementation.md` for asset management patterns

**3b. Export and organize image assets:**
- Call `figma_get_component_image` for each image asset needed, specifying `scale` and `format`
- Copy exported images to the app's asset directory following existing conventions
- Update `pubspec.yaml` asset declarations
- Maintain an asset mapping in `.ui-workspace/$FEATURE/design_data/asset_mapping.json`

**3c. Implement the Flutter code:**
- Use extracted data as reference for exact values:
  - **Colors**: hex values from `figma_get_styles` and `figma_get_variables`
  - **Typography**: font family, size, weight, line height, letter spacing from styles
  - **Layout**: dimensions, padding, margins, constraints from `figma_get_file_data`
  - **Components**: widget hierarchy from node tree structure
- Follow app conventions for state management, navigation, and theming
- Consult `references/flutter-implementation.md` for coding patterns

### Step 4: Visual Validation

**4a. Run design parity check:**
- Call `figma_check_design_parity` to automatically compare implementation against the Figma design
- Review the parity report for discrepancies in layout, colors, typography, spacing

**4b. Run design lint:**
- Call `figma_lint_design` to check the Figma design itself for consistency issues
- Address any flagged issues that affect implementation

**4c. Capture app screenshots for comparison:**

iOS Simulator:
```bash
xcrun simctl io booted screenshot .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

Android Emulator:
```bash
adb shell screencap -p > .ui-workspace/$FEATURE/app_screenshots/ss_$(date +%Y-%m-%d_%H-%M-%S)_$description.png
```

**4d. Create golden tests:**
- Write golden tests matching Figma design dimensions
- Consult `references/testing-comparison.md` for golden test patterns and device sizes

### Step 5: Iterate Until Pixel-Perfect

1. Compare Figma screenshot side-by-side with app screenshot
2. Check for discrepancies in: layout, text, colors, spacing, assets, borders/shadows
3. Fix highest-impact differences first (layout > styling > details)
4. Take new screenshot after fixes
5. Repeat until screenshots match exactly

Consult `references/testing-comparison.md` for the detailed comparison checklist.

## Common Issues

### figma-console-mcp not connected
1. Verify Figma Desktop is open with the target file
2. Ensure the Figma Console MCP plugin is running (green "MCP ready" indicator)
3. Call `figma_reconnect` to re-establish connection
4. See `references/troubleshooting.md` for detailed diagnostics

### Wrong file connected
- Call `figma_list_open_files` to see all connected files
- Call `figma_navigate` with the correct file URL

### Asset export fails
- Use `figma_get_component_image` with explicit `nodeId`, `scale`, and `format`
- Verify the node exists with `figma_get_selection` after navigating to it

## Performance Notes

- Take your time with visual comparison — pixel-perfect matters
- Run `figma_get_file_data` once and reuse the data rather than calling repeatedly
- Use `figma_search_components` at session start to cache component node IDs
- Batch multiple independent figma-console-mcp calls in parallel when possible
