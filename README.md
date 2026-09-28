# streamstats

Auto-updating Twitch panel image showing hours played on Bloons TD 6
in the last 2 weeks, pulled from the Steam Web API every 6 hours via
GitHub Actions.

## One-time setup

1. In repo **Settings → Secrets and variables → Actions**, add two secrets:
   - `STEAM_API_KEY`
   - `STEAM_ID`
2. In repo **Settings → Pages**, set Source to "Deploy from a branch",
   branch `main`, folder `/docs`. Save.
3. In repo **Actions** tab, run "Update stream stats" once manually
   (workflow_dispatch) to generate the first image.
4. Copy the Pages URL GitHub shows you, and use `<that URL>/hours.png`
   as the image URL in your Twitch panel.

After that it updates itself every 6 hours, no further action needed.
