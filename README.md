# RLBot Epic Offline Adapter

A Windows helper for inspecting RLBot v5 bot configurations and preparing offline exhibition matches through the official RLBot framework.

This project does not inject inputs into the retail client or automate ranked/public matchmaking. See `docs/BUILDING.md` for setup and build instructions.

## Windows build

GitHub Actions builds a Windows executable and uploads it as a workflow artifact. Open the repository's **Actions** tab, select **Build Windows EXE**, and download the artifact from a successful run.

## Compatibility

Targets RLBot v5 `bot.toml` / `*.bot.toml` configuration files. The utility performs structural checks only; it does not guarantee every bot's dependencies or runtime are compatible.

Official documentation: https://wiki.rlbot.org/v5/