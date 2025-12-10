# PicTex JS Usage Guide

PicTex JS is a powerful, component-based JavaScript library for creating styled images and compositions in the browser. It replicates the core functionality of the Python PicTex library, offering a fluent API for styling text, images, and layouts.

## Table of Contents
1.  [Installation](#installation)
2.  [Core Concepts](#core-concepts)
3.  [Basic Usage](#basic-usage)
4.  [Styling](#styling)
5.  [Layout](#layout)
6.  [PicTex Editor (Modular Component)](#pictex-editor)
7.  [JSON Export & Python Recreation](#json-export--python-recreation)

---

## Installation

PicTex JS is currently distributed as a set of ES6 modules. You can import them directly into your project.

```javascript
import { PicTexCanvas, Text, ImageNode, Column, Row, Shadow, LinearGradient } from './pictex.js';
import { PicTexEditor } from './pictex-editor.js';
```

---

## Core Concepts

-   **Nodes**: Everything is a `RenderNode`. `Text`, `ImageNode`, `Column`, and `Group` all inherit from this base class.
-   **Fluent API**: Methods for styling (e.g., `.color()`, `.fontSize()`) return the instance, allowing for method chaining.
-   **Canvas Renderer**: The `PicTexCanvas` class handles the rendering of the node tree to an HTML5 `<canvas>`.

---

## Basic Usage

### Rendering Text

```javascript
import { PicTexCanvas, Text } from './pictex.js';

// 1. Create a Text node
const text = new Text("Hello PicTex!")
    .fontSize(60)
    .fontFamily("Arial")
    .color("#333");

// 2. Create a Renderer
const renderer = new PicTexCanvas();
document.body.appendChild(renderer.canvas);

// 3. Render
renderer.render(text);
```

### Rendering an Image

```javascript
import { PicTexCanvas, ImageNode } from './pictex.js';

const img = new ImageNode("path/to/image.jpg");
await img.load(); // Wait for image to load

const renderer = new PicTexCanvas();
renderer.render(img);
```

---

## Styling

### Shadows
Apply shadows to text or boxes.

```javascript
import { Shadow } from './pictex.js';

text.textShadows(new Shadow({
    blurRadius: 10,
    color: "rgba(0,0,0,0.5)",
    offset: [5, 5]
}));
```

### Gradients
Use `LinearGradient` for backgrounds.

```javascript
import { LinearGradient } from './pictex.js';

node.backgroundColor(new LinearGradient({
    colors: ["#ff0000", "#0000ff"],
    start: [0, 0], // Top-left
    end: [1, 1]    // Bottom-right
}));
```

### Borders & Radius
Rounded corners and borders are supported on all nodes.

```javascript
node.borderRadius(20)
    .border(2, "black")
    .padding(20);
```

---

## Layout

### Group (Absolute Positioning)
Use `Group` to manually position elements.

```javascript
import { Group } from './pictex.js';

const group = new Group();

const text = new Text("Overlay").fontSize(30);
text._x = 100;
text._y = 50;

group.add(baseImage);
group.add(text);

renderer.render(group);
```

### Column / Row (Flex-like)
Use `Column` or `Row` for automatic layout (basic implementation).

```javascript
import { Column } from './pictex.js';

const col = new Column();
col.add(text1);
col.add(text2);
// Elements will stack vertically
```

---

## PicTex Editor

The `PicTexEditor` is a modular, self-contained component that provides a full UI for editing images. It supports modal operation, drag-and-drop, and property editing.

### Initialization

```javascript
import { PicTexEditor } from './pictex-editor.js';

const editor = new PicTexEditor({
    // Base image to load
    imageSrc: 'path/to/base.jpg',
    
    // Open in a modal overlay (default: true)
    modal: true, 
    
    // Callback when user clicks "Save"
    onSave: (json, imageBase64) => {
        console.log("JSON Data:", json);
        console.log("Image Data:", imageBase64);
    },
    
    // Optional: URL to POST data to
    serverUrl: '/api/save-image' 
});

// Open the editor
editor.open();
```

### Options

| Option | Type | Description |
| :--- | :--- | :--- |
| `imageSrc` | `string` | URL of the initial base image. |
| `modal` | `boolean` | If `true`, opens full-screen overlay. If `false`, appends to `container`. |
| `container` | `HTMLElement` | Container element for non-modal mode (default: `document.body`). |
| `onSave` | `function` | Callback `(json, imageBase64) => void`. |
| `serverUrl` | `string` | URL to automatically POST the saved data. |

---

## JSON Export & Python Recreation

PicTex JS can export the composition state as JSON, which can then be used to recreate the exact image using the Python PicTex library.

### JSON Structure
The exported JSON contains percentage-based coordinates to ensure the design scales with the image resolution.

```json
{
  "base_image": "url...",
  "elements": [
    {
      "type": "text",
      "content": "Hello",
      "x": "50.00%",
      "y": "20.00%",
      "font_size": "5.00%",
      ...
    }
  ]
}
```

### Python Recreation Script
Use the provided `recreate_from_json.py` script to render the JSON on the backend.

```bash
python recreate_from_json.py exported_data.json
```

This script requires the `pictex` Python package:
```bash
pip install pictex
```
