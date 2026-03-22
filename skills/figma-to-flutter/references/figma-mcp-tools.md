# Figma Console MCP Tools Reference

Complete reference for figma-console-mcp tools used in the Figma-to-Flutter workflow.

## Connection and Status

### figma_get_status
Check connection to Figma Desktop. Always call first.
- Returns: mode, file name, file key, transport status, WebSocket port
- Use to verify correct file is open before starting work

### figma_reconnect
Re-establish lost connection to Figma Desktop.
- Use when `figma_get_status` shows disconnected state

### figma_list_open_files
List all Figma files with the plugin running.
- Returns: file name, file key, current page for each connected file
- Use when multiple files are open to identify the correct one

## Navigation and Selection

### figma_navigate
Navigate to a specific page, frame, or node in Figma.
- Parameters: `url` (Figma URL) or `nodeId`
- Figma URL format: `https://www.figma.com/design/{fileKey}?node-id={nodeId}`
- IMPORTANT: Always navigate before taking screenshots or reading selections

### figma_get_selection
Get details about the currently selected node(s) in Figma.
- Returns: node ID, name, type, dimensions, position, styles
- Use to confirm correct element is targeted before extraction

## Design Data Extraction

### figma_get_file_data
Get the full node tree for the current page or specific node.
- Returns: hierarchical structure with layout, constraints, styles, children
- This is the primary source for layout dimensions, padding, margins
- Call once and save — contains all structural information

### figma_get_styles
Extract all styles (text, color, effect) from the file.
- Returns: style name, type, properties (font, color hex, shadow, etc.)
- Primary source for typography and color values

### figma_get_variables
Get design token variables from the file.
- Returns: variable collections, variables with values per mode
- Use for design tokens: spacing scales, color palettes, typography tokens

### figma_get_token_values
Get resolved token values across all modes.
- Returns: variable values resolved for each mode (e.g., light/dark)
- Use when the app supports multiple themes

### figma_get_design_system_summary
Overview of the file's design system.
- Returns: summary of components, styles, variables, and their relationships
- Call early to understand design system context before implementation

## Component Inspection

### figma_search_components
Search for components by name across the file.
- Parameters: query string
- Returns: matching component names and node IDs
- IMPORTANT: Call at session start — node IDs are session-specific

### figma_get_component_details
Get detailed properties of a specific component.
- Parameters: `nodeId`
- Returns: variants, properties, constraints, styles, children
- Use for understanding component structure before Flutter implementation

### figma_get_component_for_development
Get dev-ready specs for a component.
- Parameters: `nodeId`
- Returns: dimensions, padding, colors, typography, constraints in dev format
- Most useful for direct translation to Flutter widget properties

### figma_get_library_components
List components from team/shared libraries.
- Returns: library name, component names, node IDs
- Use when design uses shared library components

## Visual Capture

### figma_take_screenshot
Export an image of the current page or specific node via REST API.
- Parameters: `nodeId` (optional), `scale` (0.01-4, default 2), `format` (png/jpg/svg/pdf)
- Returns: image URL (valid 30 days)
- Use for visual reference screenshots — prefer `scale: 2` for quality

### figma_capture_screenshot
Capture a screenshot of the Figma canvas viewport.
- Returns: screenshot image
- Use for capturing exactly what's visible in Figma

### figma_get_component_image
Export a specific component as an image.
- Parameters: `nodeId`, scale, format
- Use for exporting image assets (icons, illustrations) from the design

## Design Validation

### figma_check_design_parity
Compare implementation against Figma design.
- Automated comparison for layout, colors, typography, spacing discrepancies
- Use in Step 4 to validate Flutter implementation against design

### figma_lint_design
Check design for consistency and quality issues.
- Flags: inconsistent styles, detached instances, unused components
- Use to identify design issues that could affect implementation

## Advanced: Plugin Code Execution

### figma_execute
Execute arbitrary Figma plugin code in the file context.
- Parameters: JavaScript code string
- Returns: execution result
- Use for custom extraction logic not covered by other tools
- Example: extracting gradient definitions, complex layout calculations

### figma_get_console_logs
Retrieve console output from plugin code execution.
- Parameters: `count` (number of logs), `level` filter
- Use to debug figma_execute calls

## Tool Selection Guide

| Task | Primary Tool | Fallback |
|------|-------------|----------|
| Verify connection | `figma_get_status` | `figma_reconnect` |
| Navigate to design | `figma_navigate` | — |
| Get layout/structure | `figma_get_file_data` | `figma_execute` |
| Get colors/typography | `figma_get_styles` | `figma_get_variables` |
| Get design tokens | `figma_get_variables` | `figma_get_styles` |
| Inspect component | `figma_get_component_for_development` | `figma_get_component_details` |
| Find components | `figma_search_components` | `figma_get_library_components` |
| Capture screenshot | `figma_take_screenshot` | `figma_capture_screenshot` |
| Export image asset | `figma_get_component_image` | `figma_take_screenshot` with nodeId |
| Validate implementation | `figma_check_design_parity` | Manual screenshot comparison |
| Check design quality | `figma_lint_design` | — |
