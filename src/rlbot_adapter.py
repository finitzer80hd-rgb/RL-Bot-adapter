from __future__ import annotations

import os
import subprocess
import sys
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None

TITLE = "RLBot Epic Adapter"
DOCS_URL = "https://wiki.rlbot.org/v5/botmaking/config-files/"


def load_toml(path: Path) -> dict:
    if tomllib is not None:
        with path.open("rb") as stream:
            return tomllib.load(stream)
    try:
        import tomli
        with path.open("rb") as stream:
            return tomli.load(stream)
    except ImportError as exc:
        raise RuntimeError("Install Python 3.11+ or run: py -m pip install tomli") from exc


def resolve_from(base: Path, value: str | None) -> Path | None:
    if not value:
        return None
    candidate = Path(os.path.expandvars(os.path.expanduser(value)))
    return (candidate if candidate.is_absolute() else base / candidate).resolve()


class AdapterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.geometry("820x620")
        self.minsize(700, 520)
        self.config_path = tk.StringVar()
        self.status = tk.StringVar(value="Choose an RLBot v5 bot.toml file.")
        self._make_ui()

    def _make_ui(self):
        outer = ttk.Frame(self, padding=16)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text=TITLE, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(outer, text="Inspect bot configuration and prepare a supported offline/private-match workflow.", wraplength=760).pack(anchor="w", pady=(4, 12))
        selector = ttk.Frame(outer)
        selector.pack(fill="x")
        ttk.Entry(selector, textvariable=self.config_path).pack(side="left", fill="x", expand=True)
        ttk.Button(selector, text="Browse…", command=self._browse).pack(side="left", padx=(8, 0))
        ttk.Label(outer, text="Compatibility report", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(16, 4))
        self.report = tk.Text(outer, height=17, wrap="word", state="disabled")
        self.report.pack(fill="both", expand=True)
        self._append("This tool uses the official RLBot framework for game state and controller output.\nIt does not inject into the retail client or automate ranked/public matchmaking.\nA successful config check does not prove that the bot's dependencies are installed.")
        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(12, 0))
        ttk.Button(controls, text="Inspect config", command=self.inspect).pack(side="left")
        ttk.Button(controls, text="Open bot folder", command=self.open_folder).pack(side="left", padx=8)
        ttk.Button(controls, text="Save report…", command=self.save_report).pack(side="left")
        ttk.Button(controls, text="RLBot docs", command=lambda: webbrowser.open(DOCS_URL)).pack(side="right")
        ttk.Label(outer, textvariable=self.status).pack(anchor="w", pady=(9, 0))

    def _append(self, text: str):
        self.report.configure(state="normal")
        self.report.insert("end", text + "\n")
        self.report.see("end")
        self.report.configure(state="disabled")

    def _replace_report(self, text: str):
        self.report.configure(state="normal")
        self.report.delete("1.0", "end")
        self.report.insert("end", text)
        self.report.configure(state="disabled")

    def _browse(self):
        filename = filedialog.askopenfilename(title="Select an RLBot v5 bot config", filetypes=[("RLBot config", "*.toml"), ("All files", "*.*")])
        if filename:
            self.config_path.set(filename)
            self.inspect()

    def inspect(self):
        raw = self.config_path.get().strip().strip('"')
        if not raw:
            messagebox.showinfo("Select a bot", "Choose bot.toml or a file ending in .bot.toml.")
            return
        path = Path(raw).expanduser().resolve()
        try:
            if not path.is_file():
                raise ValueError("The selected file does not exist.")
            if path.name != "bot.toml" and not path.name.endswith(".bot.toml"):
                raise ValueError("Choose bot.toml or a file ending in .bot.toml.")
            data = load_toml(path)
            settings = data.get("settings", {})
            details = data.get("details", {})
            if not isinstance(settings, dict):
                raise ValueError("The [settings] section must be a TOML table.")
            name = settings.get("name")
            agent_id = settings.get("agent_id")
            command = settings.get("run_command")
            root_value = settings.get("root_dir", ".")
            root = resolve_from(path.parent, root_value)
            issues = []
            if not name:
                issues.append("Missing settings.name.")
            if not agent_id:
                issues.append("Missing settings.agent_id.")
            if not command:
                issues.append("Missing settings.run_command; the bot may require manual startup.")
            if root is None or not root.exists():
                issues.append(f"Configured root_dir does not exist: {root_value!r}")
            lines = [f"Config: {path}", f"Bot name: {name or '(missing)'}", f"Agent ID: {agent_id or '(missing)'}", f"Language: {details.get('language', 'not specified')}", f"Run command (Windows): {command or '(missing)'}", f"Root directory: {root or '(not configured)'}", f"Root directory exists: {'yes' if root and root.exists() else 'NO'}", "", "Checks:"]
            if issues:
                lines.extend("  [WARN] " + issue for issue in issues)
                self.status.set(f"Inspection finished with {len(issues)} warning(s).")
            else:
                lines.append("  [OK] Basic required fields and root directory look present.")
                self.status.set("Inspection finished. Runtime dependencies still need testing.")
            lines.extend(["", "Limits:", "- This is a structural config check, not a bot execution test.", "- Review the run command before launching anything.", "- Use the official RLBot GUI for supported offline/private matches.", "- No ranked/public matchmaking automation is provided."])
            self._replace_report("\n".join(lines))
        except Exception as exc:
            self.status.set("Inspection failed.")
            self._replace_report(f"Could not inspect config:\n{exc}")
            messagebox.showerror("Config inspection failed", str(exc))

    def open_folder(self):
        raw = self.config_path.get().strip().strip('"')
        if not raw:
            messagebox.showinfo("Select a bot", "Choose a bot config first.")
            return
        path = Path(raw).expanduser().resolve()
        folder = path.parent if path.is_file() else path
        if not folder.exists():
            messagebox.showerror("Folder not found", str(folder))
            return
        try:
            if sys.platform == "win32":
                os.startfile(str(folder))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(folder)])
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except Exception as exc:
            messagebox.showerror("Could not open folder", str(exc))

    def save_report(self):
        content = self.report.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("No report", "Inspect a bot config first.")
            return
        target = filedialog.asksaveasfilename(title="Save compatibility report", defaultextension=".txt", initialfile="rlbot-compatibility-report.txt", filetypes=[("Text file", "*.txt")])
        if target:
            Path(target).write_text(content + "\n", encoding="utf-8")
            self.status.set(f"Report saved: {target}")


if __name__ == "__main__":
    AdapterApp().mainloop()
