# PicText JavaScript Library

A JavaScript port of the Python pictext library for creating styled images with effects. Templates generated from JavaScript are fully compatible with the Python version and vice versa.

## Features

- ✅ Full compatibility with Python pictext templates
- ✅ All styling effects (shadows, borders, colors, gradients, etc.)
- ✅ Canvas-based rendering for HTML
- ✅ Template export in JSON format
- ✅ Easy to use in HTML pages

## Quick Start

### 1. Include the Library

```html
<script src="pictext.js"></script>
```

### 2. Basic Usage

```html
<!DOCTYPE html>
<html>
<head>
    <script src="pictext.js"></script>
</head>
<body>
    <canvas id="myCanvas"></canvas>
    <script>
        async function init() {
            // Load an image
            const img = new Image();
            img.src = 'path/to/image.jpg';
            
            await img.decode();
            
            // Create PicText instance
            const pictext = await PicText.create(img.src, document.getElementById('myCanvas'));
            
            // Create a composition
            const canvas = pictext.getCanvas();
            const text = pictext.getText('Hello World!');
            
            const composition = canvas
                .fontFamily('Arial')
                .fontSize(60)
                .color('white')
                .padding(20)
                .textShadows(
                    new Shadow(['2%', '2%'], 10, '#000000A0')
                )
                .render(text);
            
            // Render and export template
            pictext.render(composition);
            const templateJSON = pictext.exportTemplate();
            console.log(templateJSON);
            
            // Download template
            pictext.downloadTemplate('my_template.json');
        }
        
        init();
    </script>
</body>
</html>
```

## API Reference

### PicText Class

Main entry point for creating compositions.

#### `PicText.create(imageSource, canvasElement)`

Creates a new PicText instance.

- `imageSource`: Image URL, Image element, or data URL
- `canvasElement`: HTML canvas element (optional, creates one if not provided)
- Returns: Promise<PicText>

#### `getCanvas()`

Returns a new Canvas builder.

#### `getText(text)`

Returns a new Text element.

#### `getImage(path)`

Returns a new Image element.

#### `getRow(...children)`

Returns a new Row container.

#### `getColumn(...children)`

Returns a new Column container.

#### `getShadow(offset, blurRadius, color)`

Creates a Shadow effect.

#### `render(composition)`

Renders a composition to the canvas.

#### `exportTemplate()`

Exports the current composition as a JSON template string.

#### `downloadTemplate(filename)`

Downloads the template as a JSON file.

### Canvas Builder

The main container for compositions.

```javascript
const canvas = pictext.getCanvas();

canvas
    .fontFamily('Arial')
    .fontSize(50)
    .color('blue')
    .padding(20)
    .backgroundColor('white')
    .borderRadius(10)
    .boxShadows(new Shadow([5, 5], 10, 'black'))
    .render(textElement);
```

### Text Element

```javascript
const text = pictext.getText('Hello World!');

text
    .fontSize(30)
    .color('red')
    .fontWeight(FontWeight.BOLD)
    .textShadows(new Shadow([2, 2], 5, 'black'))
    .underline(2, 'blue')
    .padding(10)
    .backgroundColor('yellow');
```

### Image Element

```javascript
const img = pictext.getImage('path/to/image.jpg');

img
    .size(200, 200)
    .borderRadius('50%')
    .border(3, 'white')
    .boxShadows(new Shadow([0, 0], 10, 'rgba(0,0,0,0.5)'));
```

### Styling Methods

All elements support these styling methods:

#### Typography
- `.fontFamily(family)` - Set font family
- `.fontSize(size)` - Set font size in points
- `.fontWeight(weight)` - Set font weight (FontWeight enum or number)
- `.fontStyle(style)` - Set font style (FontStyle.NORMAL or FontStyle.ITALIC)
- `.lineHeight(multiplier)` - Set line height multiplier
- `.textAlign(alignment)` - Set text alignment (TextAlign enum)
- `.textWrap(wrap)` - Set text wrap (TextWrap enum)
- `.color(color)` - Set text color (string or SolidColor)

#### Effects
- `.textShadows(...shadows)` - Add text shadows
- `.boxShadows(...shadows)` - Add box shadows
- `.textStroke(width, color)` - Add text outline stroke
- `.underline(thickness, color)` - Add underline decoration
- `.strikethrough(thickness, color)` - Add strikethrough decoration

#### Layout
- `.padding(...args)` - Set padding (1, 2, or 4 values)
- `.margin(...args)` - Set margin (1, 2, or 4 values)
- `.size(width, height)` - Set element size
- `.absolutePosition(x, y, xOffset, yOffset)` - Absolute positioning
- `.position(x, y, xOffset, yOffset)` - Relative positioning

#### Background & Borders
- `.backgroundColor(color)` - Set background color
- `.backgroundImage(path, sizeMode)` - Set background image
- `.border(width, color, style)` - Set border
- `.borderRadius(...args)` - Set border radius (1, 2, or 4 values)

### Shadow

```javascript
new Shadow(offset, blurRadius, color)

// Examples:
new Shadow([2, 2], 5, 'black')                    // Pixel offset
new Shadow(['2%', '2%'], 10, '#000000A0')         // Percentage offset
new Shadow([5, 5], 3, new SolidColor(0, 0, 0, 128)) // With SolidColor
```

### Colors

Colors can be specified as:
- Named colors: `'red'`, `'blue'`, `'white'`, etc.
- Hex strings: `'#FF0000'`, `'#FF0000FF'` (with alpha)
- SolidColor objects: `new SolidColor(255, 0, 0, 255)`
- LinearGradient objects: `new LinearGradient(['red', 'blue'])`

## Template Format

Templates are exported as JSON and can be used with the Python pictext library:

```json
{
  "version": "1.0",
  "imageSource": "path/to/image.jpg",
  "composition": {
    "type": "Canvas",
    "canvasStyle": {
      "fontSize": 60,
      "color": {
        "type": "SolidColor",
        "r": 255,
        "g": 255,
        "b": 255,
        "a": 255
      },
      "textShadows": [
        {
          "type": "Shadow",
          "offset": ["2%", "2%"],
          "blurRadius": 10,
          "color": {
            "type": "SolidColor",
            "r": 0,
            "g": 0,
            "b": 0,
            "a": 160
          }
        }
      ]
    },
    "elements": [
      {
        "type": "Text",
        "text": "Hello World!",
        "style": {}
      }
    ]
  }
}
```

## Using Templates in Python

Templates exported from JavaScript can be loaded and used in Python:

```python
import json
from pictex import Canvas, Shadow, Text

# Load template
with open('template.json', 'r') as f:
    template = json.load(f)

# Recreate composition
canvas = Canvas()
canvas_style = template['composition']['canvasStyle']

# Apply canvas styles
if 'fontSize' in canvas_style:
    canvas.font_size(canvas_style['fontSize'])
if 'color' in canvas_style:
    color_data = canvas_style['color']
    if color_data['type'] == 'SolidColor':
        from pictex import SolidColor
        canvas.color(SolidColor(color_data['r'], color_data['g'], color_data['b'], color_data['a']))
if 'textShadows' in canvas_style:
    shadows = []
    for shadow_data in canvas_style['textShadows']:
        offset = shadow_data['offset']
        blur_radius = shadow_data['blurRadius']
        color_data = shadow_data['color']
        color = SolidColor(color_data['r'], color_data['g'], color_data['b'], color_data['a'])
        shadows.append(Shadow(offset=tuple(offset), blur_radius=blur_radius, color=color))
    canvas.text_shadows(*shadows)

# Render elements
elements = []
for elem_data in template['composition']['elements']:
    if elem_data['type'] == 'Text':
        text = Text(elem_data['text'])
        # Apply element styles if needed
        elements.append(text)

# Render and save
image = canvas.render(*elements)
image.save('output.png')
```

## Examples

See `pictext-demo.html` for a complete interactive demo with examples.

## Compatibility

- ✅ Templates generated in JavaScript work with Python pictext
- ✅ Templates generated in Python work with JavaScript pictext
- ✅ All styling properties are preserved
- ✅ Percentage-based coordinates are supported
- ✅ All effect types are supported

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

Same as the Python pictext library.

