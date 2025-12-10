
/**
 * PicTex JS - A modular JavaScript library for creating visual compositions.
 */

export class Shadow {
    constructor({ offset = [0, 0], blurRadius = 0, color = 'black' } = {}) {
        this.offset = offset;
        this.blurRadius = blurRadius;
        this.color = color;
    }
}

export class LinearGradient {
    constructor({ colors = [], start = [0, 0], end = [0, 1] } = {}) {
        this.colors = colors;
        this.start = start; // Normalized coordinates 0-1
        this.end = end;
    }
}

class RenderNode {
    constructor() {
        this._padding = 0;
        this._margin = 0;
        this._backgroundColor = null;
        this._borderColor = 'black';
        this._borderWidth = 0;
        this._shadows = [];
        this._width = null;
        this._height = null;
        this._x = 0;
        this._y = 0;
        this._computedWidth = 0;
        this._computedHeight = 0;
    }

    padding(value) { this._padding = value; return this; }
    margin(value) { this._margin = value; return this; }
    backgroundColor(value) { this._backgroundColor = value; return this; }
    borderRadius(value) { this._borderRadius = value; return this; }
    border(width, color = 'black') { this._borderWidth = width; this._borderColor = color; return this; }
    boxShadows(shadow) { this._shadows.push(shadow); return this; }
    width(value) { this._width = value; return this; }
    height(value) { this._height = value; return this; }

    async layout(ctx, maxWidth) {
        // Base layout logic
        this._computedWidth = this._width || 0;
        this._computedHeight = this._height || 0;
    }

    render(ctx) {
        ctx.save();
        ctx.translate(this._x, this._y);

        // Shadows
        if (this._shadows.length > 0) {
            this._shadows.forEach(shadow => {
                ctx.shadowColor = shadow.color;
                ctx.shadowBlur = shadow.blurRadius;
                ctx.shadowOffsetX = shadow.offset[0];
                ctx.shadowOffsetY = shadow.offset[1];
            });
        }

        // Background & Border Radius
        if (this._backgroundColor || this._borderRadius > 0 || this._borderWidth > 0) {
            ctx.beginPath();
            if (this._borderRadius > 0) {
                ctx.roundRect(0, 0, this._computedWidth, this._computedHeight, this._borderRadius);
            } else {
                ctx.rect(0, 0, this._computedWidth, this._computedHeight);
            }

            if (this._backgroundColor) {
                if (this._backgroundColor instanceof LinearGradient) {
                    const grad = this._backgroundColor;
                    const gradient = ctx.createLinearGradient(
                        grad.start[0] * this._computedWidth, grad.start[1] * this._computedHeight,
                        grad.end[0] * this._computedWidth, grad.end[1] * this._computedHeight
                    );
                    grad.colors.forEach((color, index) => {
                        gradient.addColorStop(index / (grad.colors.length - 1), color);
                    });
                    ctx.fillStyle = gradient;
                } else {
                    ctx.fillStyle = this._backgroundColor;
                }
                ctx.fill();
            }

            if (this._borderWidth > 0) {
                ctx.lineWidth = this._borderWidth;
                ctx.strokeStyle = this._borderColor;
                ctx.stroke();
            }
        }

        // Reset shadows for content
        ctx.shadowColor = 'transparent';
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;

        this.renderContent(ctx);

        ctx.restore();
    }

    renderContent(ctx) {
        // To be implemented by subclasses
    }

    hitTest(x, y) {
        // Simple bounding box check
        // Assumes x, y are in the same coordinate space as this._x, this._y
        return (
            x >= this._x &&
            x <= this._x + this._computedWidth &&
            y >= this._y &&
            y <= this._y + this._computedHeight
        );
    }
}

export class Text extends RenderNode {
    constructor(content) {
        super();
        this.content = content;
        this._fontSize = 40;
        this._fontFamily = 'Arial';
        this._fontWeight = 'normal';
        this._color = 'black';
        this._textShadows = [];
        this._textAlign = 'left';
    }

    fontSize(value) { this._fontSize = value; return this; }
    fontFamily(value) { this._fontFamily = value; return this; }
    fontWeight(value) { this._fontWeight = value; return this; }
    color(value) { this._color = value; return this; }
    textShadows(shadow) { this._textShadows.push(shadow); return this; }
    textAlign(value) { this._textAlign = value; return this; }

    async layout(ctx, maxWidth) {
        ctx.font = `${this._fontWeight} ${this._fontSize}px ${this._fontFamily}`;
        const metrics = ctx.measureText(this.content);
        // Improve height calculation
        const actualHeight = metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent;

        this._computedWidth = this._width || (metrics.width + this._padding * 2);
        this._computedHeight = this._height || (actualHeight + this._padding * 2 + 10); // Add some buffer
    }

    renderContent(ctx) {
        ctx.font = `${this._fontWeight} ${this._fontSize}px ${this._fontFamily}`;
        ctx.fillStyle = this._color;
        ctx.textAlign = this._textAlign;
        ctx.textBaseline = 'middle';

        if (this._textShadows.length > 0) {
            this._textShadows.forEach(shadow => {
                ctx.shadowColor = shadow.color;
                ctx.shadowBlur = shadow.blurRadius;
                ctx.shadowOffsetX = shadow.offset[0];
                ctx.shadowOffsetY = shadow.offset[1];
            });
        }

        // Adjust drawing position based on padding and alignment
        // We draw relative to (0,0) of the node's box
        const x = this._padding + (this._textAlign === 'center' ? (this._computedWidth - this._padding * 2) / 2 : 0);
        const y = this._computedHeight / 2;

        ctx.fillText(this.content, x, y);
    }
}

export class ImageNode extends RenderNode {
    constructor(src) {
        super();
        this.src = src;
        this.image = null;
        this.loaded = false;
    }

    async load() {
        if (this.loaded) return;
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.crossOrigin = "Anonymous";
            img.onload = () => {
                this.image = img;
                this.loaded = true;
                if (!this._width) this._width = img.width;
                if (!this._height) this._height = img.height;
                resolve();
            };
            img.onerror = (e) => {
                console.error("Failed to load image", this.src, e);
                reject(e);
            };
            img.src = this.src;
        });
    }

    async layout(ctx, maxWidth) {
        await this.load();
        this._computedWidth = this._width;
        this._computedHeight = this._height;
    }

    renderContent(ctx) {
        if (this.image) {
            // Clip for border radius if needed
            if (this._borderRadius > 0) {
                ctx.save();
                ctx.beginPath();
                ctx.roundRect(0, 0, this._computedWidth, this._computedHeight, this._borderRadius);
                ctx.clip();
                ctx.drawImage(this.image, 0, 0, this._computedWidth, this._computedHeight);
                ctx.restore();
            } else {
                ctx.drawImage(this.image, 0, 0, this._computedWidth, this._computedHeight);
            }
        }
    }
}

export class Column extends RenderNode {
    constructor(...children) {
        super();
        this.children = children;
        this._gap = 0;
        this._alignItems = 'start'; // start, center, end
    }

    gap(value) { this._gap = value; return this; }
    alignItems(value) { this._alignItems = value; return this; }

    async layout(ctx, maxWidth) {
        let totalHeight = this._padding * 2;
        let maxWidthChild = 0;

        for (const child of this.children) {
            await child.layout(ctx, maxWidth); // Pass constraint if needed
            totalHeight += child._computedHeight;
            maxWidthChild = Math.max(maxWidthChild, child._computedWidth);
        }

        totalHeight += Math.max(0, this.children.length - 1) * this._gap;

        this._computedWidth = this._width || (maxWidthChild + this._padding * 2);
        this._computedHeight = this._height || totalHeight;

        // Position children
        let currentY = this._padding;
        for (const child of this.children) {
            let childX = this._padding;
            if (this._alignItems === 'center') {
                childX = (this._computedWidth - child._computedWidth) / 2;
            } else if (this._alignItems === 'end') {
                childX = this._computedWidth - child._computedWidth - this._padding;
            }

            child._x = childX;
            child._y = currentY;

            currentY += child._computedHeight + this._gap;
        }
    }

    renderContent(ctx) {
        for (const child of this.children) {
            child.render(ctx);
        }
    }
}

export class Group extends RenderNode {
    constructor(...children) {
        super();
        this.children = children;
    }

    add(child) {
        this.children.push(child);
        return this;
    }

    async layout(ctx, maxWidth) {
        // No auto-layout, just ensure children are ready
        // We assume children have their _x and _y set manually
        for (const child of this.children) {
            await child.layout(ctx, maxWidth);
        }
        // Size is determined by content or manually set
        if (!this._width || !this._height) {
            // Calculate bounds if not set
            let maxX = 0;
            let maxY = 0;
            for (const child of this.children) {
                maxX = Math.max(maxX, child._x + child._computedWidth);
                maxY = Math.max(maxY, child._y + child._computedHeight);
            }
            this._computedWidth = this._width || maxX;
            this._computedHeight = this._height || maxY;
        } else {
            this._computedWidth = this._width;
            this._computedHeight = this._height;
        }
    }

    renderContent(ctx) {
        for (const child of this.children) {
            child.render(ctx);
        }
    }
}

export class PicTexCanvas {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
    }

    async render(node) {
        // 1. Layout Pass
        // We need a temporary context for measuring text if canvas size isn't set yet
        await node.layout(this.ctx);

        // 2. Resize Canvas
        this.canvas.width = node._computedWidth;
        this.canvas.height = node._computedHeight;

        // 3. Render Pass
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        node.render(this.ctx);

        return this.canvas;
    }
}
