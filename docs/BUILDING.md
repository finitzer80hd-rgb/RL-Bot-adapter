# Build and use

## Automated Windows build

1. Open the repository's **Actions** tab.
2. Choose **Build Windows EXE** and select **Run workflow** (or push a commit to the main branch).
3. When the workflow completes successfully, open the run and download the RLBotEpicAdapter-windows artifact.
4. Extract the artifact ZIP to get RLBotEpicAdapter.exe.

The workflow builds on a Windows GitHub-hosted runner. No Windows executable is compiled inside this chat session.

## Local build

Install Python 3.11+ on Windows, then double-click build_windows_exe.bat. The executable appears in the dist folder.

## Use

1. Open the app and select bot.toml or a file ending in .bot.toml.
2. Review the compatibility report and any warnings.
3. Use Open bot folder to inspect dependencies and files.
4. Use the official RLBot GUI to configure and launch a supported offline/private match.

## Scope and limitations

- This application checks the basic RLBot v5 config structure; it does not execute a bot, install bot dependencies, or prove runtime compatibility.
- It does not control a retail online match or automate ranked/public matchmaking.
- RLBot's documented purpose is custom bots in supported offline modes. See https://wiki.rlbot.org/v5/ and https://wiki.rlbot.org/v5/botmaking/config-files/.
