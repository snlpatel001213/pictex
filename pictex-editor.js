
import { PicTexCanvas, ImageNode, Text, Shadow, Group, LinearGradient } from './pictex.js';

export class PicTexEditor {
    constructor(options = {}) {
        this.options = {
            imageSrc: options.imageSrc || '',
            onSave: options.onSave || null, // (json, imageBase64) => {}
            serverUrl: options.serverUrl || null,
            modal: options.modal !== false, // Default to true
            container: options.container || document.body,
            ...options
        };

        this.baseImageNode = null;
        this.nodes = [];
        this.selectedNode = null;
        this.renderer = new PicTexCanvas();
        this.isDragging = false;
        this.dragStart = { x: 0, y: 0 };
        this.nodeStart = { x: 0, y: 0 };

        this.ui = {}; // Holds references to UI elements
        this.isOpen = false;
    }

    open() {
        if (this.isOpen) return;
        this._createUI();
        this._bindEvents();
        this._loadBaseImage();
        this.isOpen = true;
    }

    close() {
        if (!this.isOpen) return;
        if (this.ui.wrapper) {
            this.ui.wrapper.remove();
        }
        this.isOpen = false;
        this.nodes = [];
        this.baseImageNode = null;
        this.selectedNode = null;
    }

    async _loadBaseImage() {
        if (this.options.imageSrc) {
            this.baseImageNode = new ImageNode(this.options.imageSrc);
            await this.baseImageNode.load();
            this.render();
        }
    }

    _createUI() {
        // Styles
        const styleId = 'pictex-editor-styles';
        if (!document.getElementById(styleId)) {
            const style = document.createElement('style');
            style.id = styleId;
            style.textContent = `
                .pictex-overlay {
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); z-index: 10000;
                    display: flex; justify-content: center; align-items: center;
                }
                .pictex-editor-container {
                    background: white; width: 90%; height: 90%; display: flex;
                    border-radius: 8px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.5);
                    font-family: sans-serif;
                }
                .pictex-sidebar {
                    width: 300px; background: #f8f9fa; border-right: 1px solid #ddd;
                    padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;
                }
                .pictex-preview {
                    flex: 1; background: #e9ecef; display: flex;
                    justify-content: center; align-items: center; overflow: hidden;
                    position: relative;
                }
                .pictex-preview canvas {
                    max-width: 100%; max-height: 100%; box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                .pictex-control-group { margin-bottom: 10px; }
                .pictex-control-group label { display: block; font-size: 12px; font-weight: bold; margin-bottom: 4px; }
                .pictex-control-group input, .pictex-control-group select {
                    width: 100%; padding: 6px; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;
                }
                .pictex-row { display: flex; gap: 5px; }
                .pictex-btn {
                    padding: 8px 12px; border: none; border-radius: 4px; cursor: pointer;
                    font-size: 14px; font-weight: 500; text-align: center;
                }
                .pictex-btn-primary { background: #007bff; color: white; }
                .pictex-btn-secondary { background: #6c757d; color: white; }
                .pictex-btn-danger { background: #dc3545; color: white; }
                .pictex-btn-success { background: #28a745; color: white; }
                .pictex-hidden { display: none !important; }
                .pictex-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
                .pictex-close { cursor: pointer; font-size: 20px; font-weight: bold; }
            `;
            document.head.appendChild(style);
        }

        // HTML Structure
        const wrapper = document.createElement('div');
        if (this.options.modal) {
            wrapper.className = 'pictex-overlay';
        }

        wrapper.innerHTML = `
            <div class="pictex-editor-container" style="${!this.options.modal ? 'width:100%; height:100%; box-shadow:none;' : ''}">
                <div class="pictex-sidebar">
                    <div class="pictex-header">
                        <h3>PicTex Editor</h3>
                        ${this.options.modal ? '<span class="pictex-close">&times;</span>' : ''}
                    </div>
                    
                    <div class="pictex-row">
                        <button class="pictex-btn pictex-btn-secondary" id="pt-add-text" style="flex:1">+ Text</button>
                        <button class="pictex-btn pictex-btn-secondary" id="pt-add-image" style="flex:1">+ Image</button>
                        <button class="pictex-btn pictex-btn-secondary" id="pt-import-json" style="flex:1">Import JSON</button>
                        <input type="file" id="pt-image-input" accept="image/*" style="display:none">
                        <input type="file" id="pt-json-input" accept=".json" style="display:none">
                    </div>

                    <hr style="border:0; border-top:1px solid #ddd; width:100%">

                    <div id="pt-properties" class="pictex-hidden">
                        <div id="pt-text-props">
                            <div class="pictex-control-group">
                                <label>Content</label>
                                <input type="text" id="pt-content">
                            </div>
                            <div class="pictex-row">
                                <div class="pictex-control-group" style="flex:1">
                                    <label>Size</label>
                                    <input type="number" id="pt-fontsize">
                                </div>
                                <div class="pictex-control-group" style="flex:1">
                                    <label>Color</label>
                                    <input type="color" id="pt-color">
                                </div>
                            </div>
                            <div class="pictex-control-group">
                                <label>Font</label>
                                <select id="pt-font">
                                    <option value="Arial">Arial</option>
                                    <option value="Verdana">Verdana</option>
                                    <option value="Times New Roman">Times New Roman</option>
                                    <option value="Courier New">Courier New</option>
                                    <option value="Impact">Impact</option>
                                </select>
                            </div>
                        </div>

                        <div id="pt-image-props" class="pictex-hidden">
                            <div class="pictex-row">
                                <div class="pictex-control-group" style="flex:1">
                                    <label>Width</label>
                                    <input type="number" id="pt-width">
                                </div>
                                <div class="pictex-control-group" style="flex:1">
                                    <label>Height</label>
                                    <input type="number" id="pt-height">
                                </div>
                            </div>
                        </div>

                        <div class="pictex-control-group">
                            <label>Background</label>
                            <select id="pt-bg-type">
                                <option value="none">None</option>
                                <option value="solid">Solid</option>
                                <option value="gradient">Gradient</option>
                            </select>
                        </div>
                        <div id="pt-bg-solid" class="pictex-control-group pictex-hidden">
                            <input type="color" id="pt-bg-color">
                        </div>
                        <div id="pt-bg-grad" class="pictex-row pictex-hidden">
                            <input type="color" id="pt-grad-start" style="flex:1">
                            <input type="color" id="pt-grad-end" style="flex:1">
                        </div>

                        <div class="pictex-row">
                            <div class="pictex-control-group" style="flex:1">
                                <label>Radius</label>
                                <input type="number" id="pt-radius" value="0">
                            </div>
                            <div class="pictex-control-group" style="flex:1">
                                <label>Padding</label>
                                <input type="number" id="pt-padding" value="0">
                            </div>
                        </div>

                        <div class="pictex-control-group">
                            <label>Shadow</label>
                            <div class="pictex-row">
                                <input type="number" id="pt-shadow-blur" placeholder="Blur" style="flex:1">
                                <input type="color" id="pt-shadow-color" style="flex:1">
                            </div>
                        </div>

                        <button class="pictex-btn pictex-btn-danger" id="pt-delete" style="width:100%">Delete Selected</button>
                    </div>
                    
                    <div id="pt-no-selection" style="text-align:center; color:#888; padding:20px;">
                        Select an item to edit
                    </div>

                    <div style="margin-top:auto">
                        <button class="pictex-btn pictex-btn-success" id="pt-save" style="width:100%">Save & Export</button>
                    </div>
                </div>
                <div class="pictex-preview" id="pt-preview"></div>
            </div>
        `;

        if (this.options.modal) {
            document.body.appendChild(wrapper);
        } else {
            const container = typeof this.options.container === 'string'
                ? document.querySelector(this.options.container)
                : this.options.container;
            container.appendChild(wrapper);
        }

        this.ui.wrapper = wrapper;
        this.ui.preview = wrapper.querySelector('#pt-preview');
        this.ui.preview.appendChild(this.renderer.canvas);

        // Cache inputs
        this.ui.inputs = {
            content: wrapper.querySelector('#pt-content'),
            fontSize: wrapper.querySelector('#pt-fontsize'),
            color: wrapper.querySelector('#pt-color'),
            font: wrapper.querySelector('#pt-font'),
            width: wrapper.querySelector('#pt-width'),
            height: wrapper.querySelector('#pt-height'),
            bgType: wrapper.querySelector('#pt-bg-type'),
            bgColor: wrapper.querySelector('#pt-bg-color'),
            gradStart: wrapper.querySelector('#pt-grad-start'),
            gradEnd: wrapper.querySelector('#pt-grad-end'),
            radius: wrapper.querySelector('#pt-radius'),
            padding: wrapper.querySelector('#pt-padding'),
            shadowBlur: wrapper.querySelector('#pt-shadow-blur'),
            shadowColor: wrapper.querySelector('#pt-shadow-color'),
        };
    }

    _bindEvents() {
        const w = this.ui.wrapper;

        // Close
        const closeBtn = w.querySelector('.pictex-close');
        if (closeBtn) closeBtn.onclick = () => this.close();

        // Add Items
        w.querySelector('#pt-add-text').onclick = () => this.addText();
        w.querySelector('#pt-add-image').onclick = () => w.querySelector('#pt-image-input').click();
        w.querySelector('#pt-image-input').onchange = (e) => this._handleImageUpload(e);
        w.querySelector('#pt-import-json').onclick = () => w.querySelector('#pt-json-input').click();
        w.querySelector('#pt-json-input').onchange = (e) => this._handleMetadataImport(e);

        // Save
        w.querySelector('#pt-save').onclick = () => this.save();

        // Delete
        w.querySelector('#pt-delete').onclick = () => this.deleteSelected();

        // Canvas Interaction
        this.renderer.canvas.addEventListener('mousedown', (e) => this._handleMouseDown(e));
        window.addEventListener('mousemove', (e) => this._handleMouseMove(e));
        window.addEventListener('mouseup', () => this._handleMouseUp());

        // Input Changes
        Object.values(this.ui.inputs).forEach(input => {
            input.addEventListener('input', () => this._updateFromUI());
        });

        this.ui.inputs.bgType.addEventListener('change', () => {
            this._toggleBgControls();
            this._updateFromUI();
        });
    }

    addText() {
        const text = new Text("New Text")
            .fontSize(40).fontFamily('Arial').color('#000000');
        text._x = 50; text._y = 50;
        this.nodes.push(text);
        this.selectNode(text);
        this.render();
    }

    _handleImageUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (evt) => {
            const img = new ImageNode(evt.target.result);
            await img.load();
            if (img._width > 300) {
                const ratio = img._height / img._width;
                img._width = 300; img._height = 300 * ratio;
            }
            img._x = 50; img._y = 50;
            this.nodes.push(img);
            this.selectNode(img);
            this.render();
        };
        reader.readAsDataURL(file);
        e.target.value = '';
    }

    _handleMetadataImport(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (evt) => {
            try {
                const data = JSON.parse(evt.target.result);
                if (data.elements && Array.isArray(data.elements)) {
                    await this._restoreFromJSON(data.elements);
                }
            } catch (err) {
                console.error("Failed to parse JSON", err);
                alert("Invalid JSON file");
            }
        };
        reader.readAsText(file);
        e.target.value = '';
    }

    async _restoreFromJSON(elements) {
        const baseWidth = this.baseImageNode ? this.baseImageNode._computedWidth : 800;
        const baseHeight = this.baseImageNode ? this.baseImageNode._computedHeight : 600;

        for (const el of elements) {
            let node;

            // Helper to parse percentage
            const parsePct = (val, base) => {
                if (typeof val === 'string' && val.endsWith('%')) {
                    return (parseFloat(val) / 100) * base;
                }
                return parseFloat(val) || 0;
            };

            if (el.type === 'text') {
                node = new Text(el.content || "Text");
                node.fontSize(parsePct(el.font_size, baseHeight));
                node.fontFamily(el.font_family || 'Arial');
                node.color(el.color || '#000000');

                if (el.shadow) {
                    node._textShadows = [new Shadow({
                        blurRadius: el.shadow.blur,
                        color: el.shadow.color,
                        offset: el.shadow.offset || [2, 2]
                    })];
                }
            } else if (el.type === 'image') {
                node = new ImageNode(el.src);
                await node.load();
                node._width = parsePct(el.width, baseWidth);
                node._height = parsePct(el.height, baseHeight); // Height relative to base height usually? Or aspect ratio? 
                // The export logic used baseHeight for height percentage.

                if (el.shadow) {
                    node._shadows = [new Shadow({
                        blurRadius: el.shadow.blur,
                        color: el.shadow.color,
                        offset: el.shadow.offset || [2, 2]
                    })];
                }
            }

            if (node) {
                node._x = parsePct(el.x, baseWidth);
                node._y = parsePct(el.y, baseHeight);
                node.padding(el.padding || 0);
                node.borderRadius(el.border_radius || 0);

                if (el.background) {
                    if (el.background.type === 'linear_gradient') {
                        node.backgroundColor(new LinearGradient({
                            colors: el.background.colors
                        }));
                    } else {
                        node.backgroundColor(el.background);
                    }
                }

                this.nodes.push(node);
            }
        }
        this.render();
    }

    deleteSelected() {
        if (this.selectedNode) {
            this.nodes = this.nodes.filter(n => n !== this.selectedNode);
            this.selectedNode = null;
            this._updateUI();
            this.render();
        }
    }

    selectNode(node) {
        this.selectedNode = node;
        this._updateUI();
        this.render();
    }

    _updateUI() {
        const props = this.ui.wrapper.querySelector('#pt-properties');
        const noSel = this.ui.wrapper.querySelector('#pt-no-selection');

        if (!this.selectedNode) {
            props.classList.add('pictex-hidden');
            noSel.style.display = 'block';
            return;
        }

        props.classList.remove('pictex-hidden');
        noSel.style.display = 'none';

        const n = this.selectedNode;
        const i = this.ui.inputs;

        // Type specific
        const textProps = this.ui.wrapper.querySelector('#pt-text-props');
        const imgProps = this.ui.wrapper.querySelector('#pt-image-props');

        if (n instanceof Text) {
            textProps.classList.remove('pictex-hidden');
            imgProps.classList.add('pictex-hidden');
            i.content.value = n.content;
            i.fontSize.value = n._fontSize;
            i.color.value = n._color;
            i.font.value = n._fontFamily;
        } else {
            textProps.classList.add('pictex-hidden');
            imgProps.classList.remove('pictex-hidden');
            i.width.value = Math.round(n._computedWidth);
            i.height.value = Math.round(n._computedHeight);
        }

        // Common
        i.radius.value = n._borderRadius;
        i.padding.value = n._padding;

        // Background
        if (n._backgroundColor instanceof LinearGradient) {
            i.bgType.value = 'gradient';
            i.gradStart.value = n._backgroundColor.colors[0];
            i.gradEnd.value = n._backgroundColor.colors[n._backgroundColor.colors.length - 1];
        } else if (n._backgroundColor) {
            i.bgType.value = 'solid';
            i.bgColor.value = n._backgroundColor;
        } else {
            i.bgType.value = 'none';
        }
        this._toggleBgControls();

        // Shadow
        const shadow = (n._shadows && n._shadows[0]) || (n._textShadows && n._textShadows[0]);
        if (shadow) {
            i.shadowBlur.value = shadow.blurRadius;
            i.shadowColor.value = shadow.color;
        } else {
            i.shadowBlur.value = 0;
            i.shadowColor.value = '#000000';
        }
    }

    _toggleBgControls() {
        const type = this.ui.inputs.bgType.value;
        const solid = this.ui.wrapper.querySelector('#pt-bg-solid');
        const grad = this.ui.wrapper.querySelector('#pt-bg-grad');

        solid.classList.add('pictex-hidden');
        grad.classList.add('pictex-hidden');

        if (type === 'solid') solid.classList.remove('pictex-hidden');
        if (type === 'gradient') grad.classList.remove('pictex-hidden');
    }

    _updateFromUI() {
        if (!this.selectedNode) return;
        const n = this.selectedNode;
        const i = this.ui.inputs;

        if (n instanceof Text) {
            n.content = i.content.value;
            n.fontSize(parseInt(i.fontSize.value));
            n.color(i.color.value);
            n.fontFamily(i.font.value);
        } else {
            n._width = parseInt(i.width.value);
            n._height = parseInt(i.height.value);
        }

        n.borderRadius(parseInt(i.radius.value));
        n.padding(parseInt(i.padding.value));

        // Background
        const bgType = i.bgType.value;
        if (bgType === 'none') n.backgroundColor(null);
        else if (bgType === 'solid') n.backgroundColor(i.bgColor.value);
        else if (bgType === 'gradient') n.backgroundColor(new LinearGradient({
            colors: [i.gradStart.value, i.gradEnd.value]
        }));

        // Shadow
        const blur = parseInt(i.shadowBlur.value);
        if (blur > 0) {
            const s = new Shadow({ blurRadius: blur, color: i.shadowColor.value, offset: [2, 2] });
            if (n instanceof Text) n._textShadows = [s];
            else n._shadows = [s];
        } else {
            if (n instanceof Text) n._textShadows = [];
            else n._shadows = [];
        }

        this.render();
    }

    _handleMouseDown(e) {
        const rect = this.renderer.canvas.getBoundingClientRect();
        const scaleX = this.renderer.canvas.width / rect.width;
        const scaleY = this.renderer.canvas.height / rect.height;
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;

        let hit = null;
        for (let i = this.nodes.length - 1; i >= 0; i--) {
            if (this.nodes[i].hitTest(x, y)) {
                hit = this.nodes[i];
                break;
            }
        }

        if (hit) {
            this.selectNode(hit);
            this.isDragging = true;
            this.dragStart = { x, y };
            this.nodeStart = { x: hit._x, y: hit._y };
        } else {
            this.selectedNode = null;
            this._updateUI();
            this.render();
        }
    }

    _handleMouseMove(e) {
        if (!this.isDragging || !this.selectedNode) return;
        const rect = this.renderer.canvas.getBoundingClientRect();
        const scaleX = this.renderer.canvas.width / rect.width;
        const scaleY = this.renderer.canvas.height / rect.height;
        const x = (e.clientX - rect.left) * scaleX;
        const y = (e.clientY - rect.top) * scaleY;

        const dx = x - this.dragStart.x;
        const dy = y - this.dragStart.y;
        this.selectedNode._x = this.nodeStart.x + dx;
        this.selectedNode._y = this.nodeStart.y + dy;
        this.render();
    }

    _handleMouseUp() {
        this.isDragging = false;
    }

    async render() {
        const root = new Group();
        if (this.baseImageNode) root.add(this.baseImageNode);
        this.nodes.forEach(n => root.add(n));
        await this.renderer.render(root);

        if (this.selectedNode) {
            const ctx = this.renderer.ctx;
            ctx.save();
            ctx.strokeStyle = '#007bff';
            ctx.lineWidth = 2;
            ctx.setLineDash([5, 5]);
            ctx.strokeRect(this.selectedNode._x, this.selectedNode._y,
                this.selectedNode._computedWidth, this.selectedNode._computedHeight);
            ctx.restore();
        }
    }

    async save() {
        // Deselect for clean render
        const tempSel = this.selectedNode;
        this.selectedNode = null;
        await this.render();

        const baseWidth = this.baseImageNode ? this.baseImageNode._computedWidth : 800;
        const baseHeight = this.baseImageNode ? this.baseImageNode._computedHeight : 600;

        // Generate JSON
        const exportData = {
            base_image: this.options.imageSrc,
            elements: this.nodes.map(node => {
                let shadowObj = null;
                if (node instanceof Text) {
                    shadowObj = node._textShadows && node._textShadows[0];
                } else {
                    shadowObj = node._shadows && node._shadows[0];
                }

                const common = {
                    type: node instanceof Text ? 'text' : 'image',
                    x: (node._x / baseWidth * 100).toFixed(2) + '%',
                    y: (node._y / baseHeight * 100).toFixed(2) + '%',
                    padding: node._padding,
                    border_radius: node._borderRadius,
                    background: node._backgroundColor instanceof LinearGradient ? {
                        type: 'linear_gradient',
                        colors: node._backgroundColor.colors
                    } : node._backgroundColor,
                    shadow: shadowObj ? {
                        blur: shadowObj.blurRadius,
                        color: shadowObj.color,
                        offset: shadowObj.offset
                    } : null
                };

                if (node instanceof Text) {
                    return {
                        ...common,
                        content: node.content,
                        font_size: (node._fontSize / baseHeight * 100).toFixed(2) + '%',
                        font_family: node._fontFamily,
                        color: node._color
                    };
                } else {
                    return {
                        ...common,
                        src: node.src,
                        width: (node._computedWidth / baseWidth * 100).toFixed(2) + '%',
                        height: (node._computedHeight / baseHeight * 100).toFixed(2) + '%'
                    };
                }
            })
        };

        const imageBase64 = this.renderer.canvas.toDataURL('image/png');

        // Restore selection
        this.selectedNode = tempSel;
        this.render();

        // Handle Output
        if (this.options.onSave) {
            this.options.onSave(exportData, imageBase64);
        }

        if (this.options.serverUrl) {
            try {
                await fetch(this.options.serverUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ json: exportData, image: imageBase64 })
                });
                alert('Saved to server!');
            } catch (e) {
                console.error('Save failed', e);
                alert('Failed to save to server');
            }
        }
    }
}
