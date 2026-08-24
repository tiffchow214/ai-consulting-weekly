# Excalidraw Visuals — Style Guide

This is the locked visual specification for every generated image. Prepend it (or a summary of it) to every prompt sent to `generate-visual.js` so outputs stay consistent across generations.

## Shapes
Rounded rectangles with a slightly rough, hand-drawn stroke (Excalidraw's signature "sketchy" line quality — not perfectly straight or geometric). Solid fills, not hachure. Generous corner rounding on containers and labels.

## Color palette
Same 6-zone system used by the `excalidraw-diagram` skill, so generated PNGs and editable `.excalidraw` diagrams read as one family:

| Zone | Use for | Stroke | Fill |
|------|---------|--------|------|
| Blue | Input, source, external services | `#1971c2` | `#e7f5ff` |
| Yellow | Processing, transformation | `#f59f00` | `#fff9db` |
| Green | Output, containers, success | `#2f9e44` | `#d3f9d8` |
| Purple | Shared layers, infrastructure | `#862e9c` | `#f3d9fa` |
| Red | Alerts, warnings, errors | `#c92a2a` | `#ffe3e3` |
| Gray | Hardware, neutral containers | `#495057` | `#f8f9fa` |

One color per logical zone — the viewer should read structure from color before reading any label.

## Icons
Simple black-line icons, hand-drawn style, no fill: person (user), robot (agent/AI), document (data/file), gear (config/system), laptop (client/device), play triangle (action/trigger). Keep icons minimal — outline only, consistent stroke weight, no shading or gradients.

## Typography
Hand-written font throughout (Excalidraw's Virgil style).
- **Titles:** large, bold weight, used once per image as the main heading
- **Section/shape labels:** medium size, centered inside their shape
- **Annotations / small notes:** small size, muted gray, used sparingly for context that doesn't fit in a label

## Flow pattern
Default left-to-right flow for processes: `Input -> Process -> Output`, each stage as a rounded box in its zone color, connected by simple arrows with arrowheads. Label arrows only when the relationship isn't obvious from adjacent box names.

## Composition rules
- White background
- 15px+ minimum gap between sibling shapes, 40px+ between major sections
- Keep labels to 2-5 words; anything longer becomes a small annotation instead
- Don't overcrowd — fewer, clearer elements beat a dense diagram
