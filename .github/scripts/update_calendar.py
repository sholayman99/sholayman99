#!/usr/bin/env python3
import urllib.request
import re
import sys

def main():
    username = "sholayman99"
    url = f"https://ghchart.rshah.org/4ade80/{username}"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; GitHubAction/1.0)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw_svg = resp.read().decode("utf-8")
    except Exception as e:
        print(f"Error fetching from ghchart: {e}", file=sys.stderr)
        sys.exit(1)

    # Color palette matching #0a0f0d / #1f2e27 / #4ade80
    SCORE_COLORS = {
        "0": "#15201b",  # Dark empty square
        "1": "#195837",  # Level 1 activity
        "2": "#23864a",  # Level 2 activity
        "3": "#34d399",  # Level 3 activity
        "4": "#4ade80",  # Level 4 activity
    }

    content_match = re.search(r"<svg[^>]*>(.*?)</svg>", raw_svg, re.DOTALL)
    if not content_match:
        print("Failed to parse SVG content", file=sys.stderr)
        sys.exit(1)

    inner_content = content_match.group(1)

    rect_pattern = re.compile(r"<rect([^>]+)/>")
    def replace_rect(match):
        attrs = match.group(1)
        score_match = re.search(r'data-score="(\d+)"', attrs)
        score = score_match.group(1) if score_match else "0"
        color = SCORE_COLORS.get(score, "#15201b")
        attrs = re.sub(r"fill:[^;]+;", f"fill:{color};", attrs)
        if "rx=" not in attrs:
            attrs += ' rx="2" ry="2"'
        return f"<rect{attrs}/>"

    inner_content = rect_pattern.sub(replace_rect, inner_content)
    # Replace label text color (#767676 -> #8b949e)
    inner_content = re.sub(r"fill:#767676;", "fill:#8b949e;", inner_content)

    card_w = 710
    card_h = 136
    offset_x = 24
    offset_y = 16

    final_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_w} {card_h}" width="100%" role="img" aria-label="{username} GitHub contributions">
  <defs>
    <style>
      text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji'; }}
    </style>
  </defs>
  <rect width="{card_w}" height="{card_h}" rx="10" fill="#0a0f0d" stroke="#1f2e27" stroke-width="1"/>
  <g transform="translate({offset_x}, {offset_y})">
{inner_content}
  </g>
</svg>"""

    with open("assets/calendar.svg", "w", encoding="utf-8") as f:
        f.write(final_svg)

    print("Updated assets/calendar.svg successfully.")

if __name__ == "__main__":
    main()
