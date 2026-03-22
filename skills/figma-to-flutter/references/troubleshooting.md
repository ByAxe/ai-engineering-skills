# Troubleshooting

## Connection Issues

### figma_get_status returns disconnected

**Cause:** Figma Console MCP plugin is not running in Figma Desktop.

**Solution:**
1. Open Figma Desktop (not the web version — plugin requires desktop)
2. Open the target design file
3. Go to: Plugins > Development > Figma Console MCP
4. Click Run — wait for green "MCP ready" indicator
5. Call `figma_reconnect` from Claude

### figma_get_status shows wrong file

**Cause:** Multiple Figma files are open, and the plugin is connected to a different one.

**Solution:**
1. Call `figma_list_open_files` to see all connected files
2. Call `figma_navigate` with the correct Figma URL to switch
3. Or: in Figma Desktop, switch to the correct file tab and re-run the plugin

### WebSocket connection refused (port 9223)

**Cause:** MCP server process is not running or port conflict.

**Solution:**
1. Check if the figma-console-mcp server is running: `lsof -i :9223`
2. If not running, verify Claude Code MCP configuration includes figma-console
3. Restart Claude Code session to re-launch MCP servers
4. Check for port conflicts: `lsof -i :9223` — kill conflicting process if needed

### Plugin shows "MCP ready" but tools return errors

**Cause:** Plugin UI is open but WebSocket bridge is stale.

**Solution:**
1. In Figma, close the plugin window
2. Re-run: Plugins > Development > Figma Console MCP
3. Call `figma_reconnect` from Claude
4. Verify with `figma_get_status`

## Data Extraction Issues

### figma_get_file_data returns empty or partial data

**Cause:** Node ID is invalid, or the node is on a different page.

**Solution:**
1. Call `figma_navigate` to the correct page/frame first
2. Verify navigation with `figma_get_selection`
3. Use the node ID from the Figma URL (format: `123:456`)

### figma_get_styles returns no styles

**Cause:** Design uses local styles not published, or uses raw values without styles.

**Solution:**
1. Extract values directly from `figma_get_file_data` node properties
2. Use `figma_execute` with custom code to extract specific properties:
   ```javascript
   const node = figma.currentPage.selection[0];
   return { fills: node.fills, strokes: node.strokes, effects: node.effects };
   ```

### figma_search_components returns no results

**Cause:** Components may be in a different page, or named differently than expected.

**Solution:**
1. Try broader search terms
2. Call `figma_get_library_components` for shared library components
3. Navigate to the component page and use `figma_get_selection`

## Screenshot Issues

### figma_take_screenshot returns error

**Cause:** Node ID is invalid, or REST API authentication issue.

**Solution:**
1. Verify node exists: navigate to it with `figma_navigate`, then `figma_get_selection`
2. Try `figma_capture_screenshot` as an alternative (captures viewport)
3. If auth issue: ensure Figma access token is configured in the MCP server

### Screenshot quality is low

**Cause:** Default scale is too low.

**Solution:**
- Set `scale: 2` or `scale: 3` in `figma_take_screenshot` parameters
- Maximum scale is 4

### Screenshot shows wrong area

**Cause:** Not navigated to the correct node before capturing.

**Solution:**
1. Call `figma_navigate` with the target node ID
2. Wait for navigation to complete
3. Then call `figma_take_screenshot` with the specific `nodeId`

## Asset Export Issues

### figma_get_component_image fails

**Cause:** Node is not a component, or node ID is wrong.

**Solution:**
1. Verify the node type: it must be a COMPONENT, INSTANCE, or FRAME
2. Use `figma_take_screenshot` with `nodeId` as an alternative
3. For complex assets, use `figma_execute` to export programmatically

### Exported images have wrong dimensions

**Cause:** Scale factor doesn't match app expectations.

**Solution:**
1. Check app's asset scaling strategy (see flutter-implementation.md)
2. Export at the correct scale: 1x, 2x, 3x, or 4x
3. Verify with the asset mapping to ensure consistency

## Flutter Implementation Issues

### Colors don't match between Figma and Flutter

**Common causes:**
- Figma uses RGB, Flutter uses ARGB — ensure alpha channel is correct
- Opacity applied at layer level in Figma vs. color level in Flutter
- Color profile differences (Figma sRGB vs. device color space)

**Solution:**
- Extract exact hex from `figma_get_styles` or `figma_get_file_data`
- Convert: Figma `#RRGGBB` at 80% opacity = Flutter `Color(0xCCRRGGBB)`
- Alpha hex: multiply opacity (0-1) by 255, convert to hex

### Layout doesn't match

**Common causes:**
- Auto Layout direction mismatched (Row vs Column)
- "Fill container" not translated to Expanded/Flexible
- Padding applied to wrong widget in the hierarchy

**Solution:**
- Review `figma_get_file_data` for exact Auto Layout properties
- Check `layoutMode`, `primaryAxisSizingMode`, `counterAxisSizingMode`
- Match padding from `paddingLeft/Right/Top/Bottom` properties

### Text overflows or clips

**Common causes:**
- Missing `maxLines` or `overflow` property
- Fixed height container too small for text
- Line height calculation differs

**Solution:**
- Figma line height is absolute (e.g., 24px)
- Flutter `height` is a multiplier: `height = lineHeight / fontSize`
- Example: 24px line height with 16px font = `height: 1.5`
