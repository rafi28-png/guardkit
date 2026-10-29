"""Generate a small README badge SVG showing CO2 saved."""


def badge_svg(saved_g: float, saved_pct: float) -> str:
    text = f"CO2 saved {saved_g:.0f}g ({saved_pct:.0f}%)"
    # Width scales roughly with text length; keep it simple and readable.
    width = 30 + len(text) * 7
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20">
  <rect width="{width}" height="20" rx="3" fill="#2da44e"/>
  <text x="{width//2}" y="14" font-family="sans-serif" font-size="11" fill="white" text-anchor="middle">🌱 {text}</text>
</svg>
"""
