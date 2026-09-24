"""Cheat sheet: lists every shortcut in the User keymap (plus handy built-ins
and the Laravel palette commands) in a quick panel. Picking one runs it.

Labels come from the `//` comment directly above each binding in
`Default (OSX).sublime-keymap`, so new bindings show up automatically.
"""
import re

import sublime
import sublime_plugin

KEYMAP = "Packages/User/Default (OSX).sublime-keymap"
COMMANDS = "Packages/User/Laravel.sublime-commands"

MODIFIERS = [("ctrl", "⌃"), ("alt", "⌥"), ("shift", "⇧"), ("super", "⌘")]
NAMED_KEYS = {"escape": "Esc", "enter": "↩", "tab": "⇥", "space": "Space",
              "up": "↑", "down": "↓", "left": "←", "right": "→"}

# Built-in shortcuts worth remembering: (keys, label, command, args)
BUILTINS = [
    (["super+p"], "Goto Anything (open file)", "show_overlay", {"overlay": "goto", "show_files": True}),
    (["super+shift+p"], "Command Palette", "show_overlay", {"overlay": "command_palette"}),
    (["super+r"], "Goto symbol in file", "show_overlay", {"overlay": "goto", "text": "@"}),
    (["super+shift+r"], "Goto symbol in project", "goto_symbol_in_project", {}),
    (["ctrl+0"], "Focus file explorer", "focus_side_bar", {}),
    (["super+alt+down"], "Goto definition", "goto_definition", {}),
    (["ctrl+minus"], "Jump back", "jump_back", {}),
    (["super+d"], "Select next occurrence", None, None),
    (["ctrl+super+g"], "Select all occurrences", None, None),
    (["super+shift+l"], "Split selection into lines (multi-cursor)", None, None),
    (["super+l"], "Select line", None, None),
    (["super+shift+d"], "Duplicate line", None, None),
    (["ctrl+shift+k"], "Delete line", None, None),
    (["super+forward_slash"], "Toggle comment", None, None),
    (["super+k", "super+b"], "Toggle file explorer (default chord)", "toggle_side_bar", {}),
]


def pretty(keys):
    """["super+alt+shift+t"] -> "⌥⇧⌘T"; chords are joined with a space."""
    out = []
    for combo in keys:
        parts = combo.split("+")
        # "super++" style bindings for the plus key itself
        if combo.endswith("++"):
            parts = parts[:-2] + ["+"]
        mods = [sym for name, sym in MODIFIERS if name in parts[:-1]]
        key = parts[-1]
        key = NAMED_KEYS.get(key, {"minus": "-", "forward_slash": "/"}.get(key, key.upper()))
        out.append("".join(mods) + key)
    return " ".join(out)


def keymap_labels(text):
    """The comment above each `"keys"` line, in file order."""
    labels, comment = [], None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("//"):
            comment = stripped.lstrip("/ ").strip()
        elif '"keys"' in stripped:
            labels.append(comment)
            comment = None
        elif stripped:
            if not stripped.startswith(("\"", "}", "]", "[")):
                comment = None
    return labels


def clean(label):
    # Drop trailing "(…)" explanations to keep the list tidy
    return re.sub(r"\s*\([^)]*\)\s*$", "", label) if label else label


class ShowShortcutsCommand(sublime_plugin.WindowCommand):
    def run(self):
        entries = []

        try:
            text = sublime.load_resource(KEYMAP)
            bindings = sublime.decode_value(text)
            labels = keymap_labels(text)
            for i, b in enumerate(bindings):
                label = clean(labels[i] if i < len(labels) else None) or b["command"]
                entries.append((pretty(b["keys"]), label, b["command"], b.get("args", {}), "Mine"))
        except Exception as e:
            print("[shortcuts] could not read keymap:", e)

        try:
            for c in sublime.decode_value(sublime.load_resource(COMMANDS)):
                entries.append(("palette", c["caption"], c["command"], c.get("args", {}), "Laravel"))
        except Exception as e:
            print("[shortcuts] could not read commands:", e)

        for keys, label, cmd, args in BUILTINS:
            entries.append((pretty(keys), label, cmd, args, "Built-in"))

        kinds = {
            "Mine": (sublime.KIND_ID_NAVIGATION, "★", "mine"),
            "Laravel": (sublime.KIND_ID_FUNCTION, "L", "laravel"),
            "Built-in": (sublime.KIND_ID_KEYWORD, "·", "built-in"),
        }
        items = [
            sublime.QuickPanelItem(trigger=label, annotation=keys, kind=kinds[group])
            for keys, label, _, _, group in entries
        ]

        def on_select(index):
            if index < 0:
                return
            _, _, cmd, args, _ = entries[index]
            if cmd:
                self.window.run_command(cmd, args)

        self.window.show_quick_panel(items, on_select, placeholder="Search shortcuts…")
