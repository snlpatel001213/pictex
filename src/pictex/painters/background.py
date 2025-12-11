import skia
from .painter import Painter
from ..utils import create_composite_shadow_filter
from ..models import Style, BackgroundImageSizeMode

class BackgroundPainter(Painter):

    def __init__(self, style: Style, box_bounds: skia.Rect, is_svg: bool):
        super().__init__(style)
        self._box_bounds = box_bounds
        self._is_svg = is_svg

    def paint(self, canvas: skia.Canvas) -> None:
        rounded_box_rect = self._build_rounded_box_rect()
        self._paint_box_shadows(canvas, rounded_box_rect)
        self._paint_background_color(canvas, rounded_box_rect)
        self._paint_background_image(canvas, rounded_box_rect)

    def _build_rounded_box_rect(self) -> skia.RRect:
        box_radius = self._style.border_radius.get()
        if not box_radius:
            return skia.RRect.MakeRect(self._box_bounds)

        return box_radius.apply_corner_radius(self._box_bounds)

    def _paint_box_shadows(self, canvas: skia.Canvas, box_rect: skia.RRect):
        if self._is_svg:
            return

        paint = skia.Paint(AntiAlias=True)
        shadow_filter = create_composite_shadow_filter(
            self._style.box_shadows.get(), 
            should_remove_content=True,
            element_width=self._box_bounds.width(),
            element_height=self._box_bounds.height()
        )
        if shadow_filter:
            paint.setImageFilter(shadow_filter)
            canvas.drawRRect(box_rect, paint)

    def _paint_background_color(self, canvas: skia.Canvas, box_rect: skia.RRect) -> None:
        background_color = self._style.background_color.get()
        if not background_color:
            return

        paint = skia.Paint(AntiAlias=True)
        background_color.apply_to_paint(paint, self._box_bounds)
        canvas.drawRRect(box_rect, paint)

    def _paint_background_image(self, canvas: skia.Canvas, box_rect: skia.RRect):
        background_image_info = self._style.background_image.get()
        if not background_image_info:
            return

        original_image = background_image_info.get_skia_image()
        if not original_image:
            return

        sampling_options = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
        canvas.save()
        canvas.clipRRect(box_rect, doAntiAlias=True)

        paint = skia.Paint(AntiAlias=True)
        
        # Apply Image Effects
        effects = self._style.image_effects.get()
        if effects:
            filters = []
            
            # Brightness (scale)
            # JS brightness(150%) -> 1.5 multiplier
            if effects.brightness != 100:
                b = effects.brightness / 100.0
                matrix = [
                    b, 0, 0, 0, 0,
                    0, b, 0, 0, 0,
                    0, 0, b, 0, 0,
                    0, 0, 0, 1, 0
                ]
                filters.append(skia.ColorFilters.Matrix(matrix))

            # Contrast
            # v' = (v - 0.5) * c + 0.5
            if effects.contrast != 100:
                c = effects.contrast / 100.0
                t = (1.0 - c) / 2.0
                matrix = [
                    c, 0, 0, 0, t,
                    0, c, 0, 0, t,
                    0, 0, c, 0, t,
                    0, 0, 0, 1, 0
                ]
                filters.append(skia.ColorFilters.Matrix(matrix))

            # Saturation
            if effects.saturation != 100:
                s = effects.saturation / 100.0
                # Skia has MakeLumaColorFilter? No, ColorMatrix usually.
                # Standard RGB to Luminance constants: 0.2126, 0.7152, 0.0722
                # sat matrix:
                # [ r + (1-r)*s,  g*(1-s),    b*(1-s),    0, 0 ]
                # [ r*(1-s),      g + (1-g)*s,b*(1-s),    0, 0 ]
                # etc.
                # Actually skia module usually exposes skia.ColorMatrix or similar?
                # skia-python binding check: skia.ColorFilters.Matrix(list)
                
                # Simplified Saturation Matrix generator
                rw, gw, bw = 0.2126, 0.7152, 0.0722
                invS = 1.0 - s
                R = invS * rw
                G = invS * gw
                B = invS * bw
                
                matrix = [
                    R + s, G,     B,     0, 0,
                    R,     G + s, B,     0, 0,
                    R,     G,     B + s, 0, 0,
                    0,     0,     0,     1, 0
                ]
                filters.append(skia.ColorFilters.Matrix(matrix))
                
            # Warmth (Sepia)
            if effects.warmth > 0:
                # Sepia is usually a specific matrix. 
                # Can blend between normal and sepia based on percentage.
                amount = effects.warmth / 100.0
                invAmount = 1.0 - amount
                
                # Standard Sepia Matrix
                # R = 0.393 + 0.769 + 0.189
                # But we valid mix with identity.
                # Identity:
                # 1 0 0 0 0
                # 0 1 0 0 0
                # ...
                
                # Sepia:
                # 0.393 0.769 0.189 0 0 
                # 0.349 0.686 0.168 0 0
                # 0.272 0.534 0.131 0 0
                
                matrix = [
                    0.393*amount + 1*invAmount, 0.769*amount, 0.189*amount, 0, 0,
                    0.349*amount, 0.686*amount + 1*invAmount, 0.168*amount, 0, 0,
                    0.272*amount, 0.534*amount, 0.131*amount + 1*invAmount, 0, 0,
                    0, 0, 0, 1, 0
                ]
                filters.append(skia.ColorFilters.Matrix(matrix))

            # Compose Filters
            if filters:
                # Compose from last to first (outer to inner)?
                # Skia compose(outer, inner).
                # If we apply brightness then contrast, it means contrast(brightness(pixel)).
                # So brightness is inner.
                # Order in list: brightness, contrast, saturation, warmth.
                # We iterate and compose.
                # F = filters[0]
                # F = input -> brightness -> output
                # Next is contrast. input -> contrast -> output.
                # We want input -> brightness -> contrast -> ...
                # So combined = compose(contrast, brightness)
                
                final_filter = filters[0]
                for f in filters[1:]:
                    final_filter = skia.ColorFilters.Compose(f, final_filter)
                    
                paint.setColorFilter(final_filter)

        if background_image_info.size_mode == BackgroundImageSizeMode.TILE:
            shader = original_image.makeShader(
                skia.TileMode.kRepeat,
                skia.TileMode.kRepeat,
                sampling_options
            )
            paint.setShader(shader)
            canvas.drawRect(self._box_bounds, paint)
            canvas.restore()
            return

        src_rect, dst_rect = self._calculate_cover_contain_rects(
            image_width=original_image.width(),
            image_height=original_image.height(),
            box_rect=self._box_bounds,
            mode=background_image_info.size_mode
        )

        image_to_resize = original_image.makeSubset(src_rect.roundOut())
        resized_image = image_to_resize.resize(
            width=int(dst_rect.width()),
            height=int(dst_rect.height()),
            options=sampling_options
        )

        if not resized_image:
            return

        canvas.drawImage(
            resized_image,
            dst_rect.left(),
            dst_rect.top(),
            sampling_options,
            paint
        )

        canvas.restore()

    def _calculate_cover_contain_rects(
            self, image_width: float, image_height: float, box_rect: skia.Rect, mode: BackgroundImageSizeMode):

        box_width = box_rect.width()
        box_height = box_rect.height()
        img_aspect = image_width / image_height
        box_aspect = box_width / box_height

        if mode == BackgroundImageSizeMode.COVER:
            if img_aspect > box_aspect:
                new_src_width = image_height * box_aspect
                src_x_offset = (image_width - new_src_width) / 2
                src_rect = skia.Rect.MakeXYWH(src_x_offset, 0, new_src_width, image_height)
                return src_rect, box_rect

            new_src_height = image_width / box_aspect
            src_y_offset = (image_height - new_src_height) / 2
            src_rect = skia.Rect.MakeXYWH(0, src_y_offset, image_width, new_src_height)
            return src_rect, box_rect

        elif mode == BackgroundImageSizeMode.CONTAIN:
            src_rect = skia.Rect.MakeWH(image_width, image_height)
            if img_aspect > box_aspect:
                new_dst_height = box_width / img_aspect
                dst_y_offset = (box_height - new_dst_height) / 2
                dst_rect = skia.Rect.MakeXYWH(box_rect.left(), box_rect.top() + dst_y_offset, box_width, new_dst_height)
                return src_rect, dst_rect

            new_dst_width = box_height * img_aspect
            dst_x_offset = (box_width - new_dst_width) / 2
            dst_rect = skia.Rect.MakeXYWH(box_rect.left() + dst_x_offset, box_rect.top(), new_dst_width, box_height)
            return src_rect, dst_rect

        raise ValueError(f"Unknown mode: {mode}")
