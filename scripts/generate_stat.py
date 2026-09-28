#!/usr/bin/env python3
"""
Generates a small PNG panel image showing hours played on Bloons TD 6
in the last 2 weeks, pulled live from the Steam Web API.

Reads STEAM_API_KEY and STEAM_ID from environment variables (set as
GitHub Actions secrets). Writes output to docs/hours.png so GitHub
Pages can serve it at a stable URL.
"""
import os
import sys
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

STEAM_API_KEY = os.environ["STEAM_API_KEY"]
STEAM_ID = os.environ["STEAM_ID"]
APP_ID = 960090  # Bloons TD 6

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "hours.png")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Brand colors (Orange Rhino palette)
BG = (20, 24, 20, 255)
GREEN = (122, 156, 94, 255)
ORANGE = (224, 150, 95, 255)
WHITE = (240, 240, 235, 255)
MUTED = (170, 175, 165, 255)


def fetch_playtime_minutes():
    url = (
        "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        f"?key={STEAM_API_KEY}&steamid={STEAM_ID}&format=json"
        "&include_appinfo=true&include_played_free_games=true"
    )
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.load(resp)

    games = data.get("response", {}).get("games", [])
    for g in games:
        if g.get("appid") == APP_ID:
            return g.get("playtime_2weeks", 0)
    return 0


def render(hours_2weeks):
    W, H = 320, 200
    img = Image.new("RGBA", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Rounded card border accent
    d.rectangle([0, 0, W - 1, 6], fill=GREEN)

    label_font = ImageFont.truetype(FONT_REG, 20)
    num_font = ImageFont.truetype(FONT_BOLD, 64)
    sub_font = ImageFont.truetype(FONT_REG, 18)
    game_font = ImageFont.truetype(FONT_REG, 16)

    d.text((20, 28), "LAST 2 WEEKS", font=label_font, fill=MUTED)

    num_text = f"{hours_2weeks:.1f}"
    d.text((20, 55), num_text, font=num_font, fill=ORANGE)
    num_w = d.textlength(num_text, font=num_font)
    d.text((20 + num_w + 8, 95), "hrs", font=sub_font, fill=WHITE)

    d.text((20, 155), "Bloons TD 6", font=game_font, fill=GREEN)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    img.save(OUT_PATH)
    print(f"Wrote {OUT_PATH}: {hours_2weeks:.1f} hrs (2 weeks)")


def main():
    try:
        minutes = fetch_playtime_minutes()
    except Exception as e:
        print(f"ERROR fetching Steam data: {e}", file=sys.stderr)
        # Don't fail the whole workflow over a transient Steam API hiccup;
        # keep the previously published image in place.
        sys.exit(0)

    hours = minutes / 60.0
    render(hours)


if __name__ == "__main__":
    main()
