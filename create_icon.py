#!/usr/bin/env python3
"""
Generates a high-resolution Windows icon (.ico) for the Slave 1 Cockpit app.
Featuring the classic Firespray-31 silhouette, cockpit canopy, and Kuat targeting reticle.
"""

from PIL import Image, ImageDraw

def generate_slave1_icon(size=256):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    center = size / 2
    scale = size / 256.0

    # Palette
    DARK_BG = (15, 23, 42, 255)       # Outer space navy
    BORDER_CYAN = (6, 182, 212, 255)   # Kuat HUD Cyan
    MANDO_GREEN = (22, 101, 52, 255)   # Firespray Upper Hull Green
    MANDO_RED = (185, 28, 28, 255)     # Lower Skirt Rust Red
    GOLD_ACCENT = (234, 179, 8, 255)   # Lone Ranger Gold Accent
    CANOPY_BLUE = (147, 197, 253, 240) # Viewport Glass
    RETICLE_AMBER = (245, 158, 11, 255)# Targeting Reticle
    WHITE = (255, 255, 255, 255)

    # 1. Circular Outer HUD Badge
    margin = 8 * scale
    draw.ellipse([margin, margin, size - margin, size - margin], fill=DARK_BG, outline=BORDER_CYAN, width=int(6 * scale))

    # 2. Outer Reticle Ticks
    for angle_offset in [-45, 45, 135, 225]:
        r_inner = 100 * scale
        r_outer = 118 * scale
        import math
        rad = math.radians(angle_offset)
        x1 = center + r_inner * math.cos(rad)
        y1 = center + r_inner * math.sin(rad)
        x2 = center + r_outer * math.cos(rad)
        y2 = center + r_outer * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=RETICLE_AMBER, width=int(4 * scale))

    # 3. Lower Skirt / Stabilizer Base (Rust Red)
    skirt_points = [
        (center - 65 * scale, center + 75 * scale),
        (center + 65 * scale, center + 75 * scale),
        (center + 45 * scale, center + 30 * scale),
        (center - 45 * scale, center + 30 * scale),
    ]
    draw.polygon(skirt_points, fill=MANDO_RED, outline=GOLD_ACCENT)

    # 4. Upper Cockpit Tower Fuselage (Mandalorian Green)
    tower_points = [
        (center - 32 * scale, center + 32 * scale),
        (center + 32 * scale, center + 32 * scale),
        (center + 24 * scale, center - 60 * scale),
        (center, center - 78 * scale),
        (center - 24 * scale, center - 60 * scale),
    ]
    draw.polygon(tower_points, fill=MANDO_GREEN, outline=GOLD_ACCENT)

    # 5. Cockpit Dome Canopy Viewport (Curved Cyan/Blue Glass)
    canopy_box = [center - 18 * scale, center - 48 * scale, center + 18 * scale, center - 10 * scale]
    draw.ellipse(canopy_box, fill=CANOPY_BLUE, outline=WHITE, width=int(2 * scale))

    # 6. Central Kuat Vector Reticle Crosshair
    draw.line([(center - 15 * scale, center), (center + 15 * scale, center)], fill=BORDER_CYAN, width=int(2 * scale))
    draw.line([(center, center - 15 * scale), (center, center + 15 * scale)], fill=BORDER_CYAN, width=int(2 * scale))
    draw.ellipse([center - 6 * scale, center - 6 * scale, center + 6 * scale, center + 6 * scale], outline=RETICLE_AMBER, width=int(2 * scale))

    return img

def create_ico():
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = [generate_slave1_icon(s[0]) for s in sizes]

    repo_ico = r"C:\Users\ole_a\Slave1-Cockpit\slave1.ico"
    desktop_ico = r"C:\Users\ole_a\Desktop\Slave1.ico"

    images[0].save(repo_ico, format="ICO", sizes=sizes)
    images[0].save(desktop_ico, format="ICO", sizes=sizes)
    print(f"Icon generated: {repo_ico}")
    print(f"Icon saved to Desktop: {desktop_ico}")

if __name__ == "__main__":
    create_ico()
