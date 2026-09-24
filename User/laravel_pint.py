import os
import subprocess
import threading

import sublime
import sublime_plugin

HERD_BIN = os.path.expanduser("~/.config/herd-lite/bin")


def find_pint(path):
    """Walk up from the file to the nearest project that has vendor/bin/pint."""
    folder = os.path.dirname(path)
    while True:
        pint = os.path.join(folder, "vendor", "bin", "pint")
        if os.path.isfile(pint):
            return folder, pint
        parent = os.path.dirname(folder)
        if parent == folder:
            return None, None
        folder = parent


class LaravelPintOnSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        path = view.file_name()
        if not path or not path.endswith(".php") or path.endswith(".blade.php"):
            return
        root, pint = find_pint(path)
        if not pint or os.sep + "vendor" + os.sep in path:
            return
        threading.Thread(target=self.run, args=(view, root, pint, path)).start()

    def run(self, view, root, pint, path):
        env = os.environ.copy()
        env["PATH"] = HERD_BIN + os.pathsep + env.get("PATH", "")
        env["PHP_INI_SCAN_DIR"] = HERD_BIN
        try:
            proc = subprocess.run(
                ["php", pint, path], cwd=root, env=env,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30,
            )
        except Exception as e:
            sublime.status_message("Pint failed: {}".format(e))
            return
        if proc.returncode != 0:
            sublime.status_message("Pint failed, see console")
            print("[pint]", proc.stdout.decode("utf-8", "replace"))
            return
        # Pick up Pint's changes (no-op if the file didn't change)
        sublime.set_timeout(lambda: view.run_command("revert") if not view.is_dirty() else None, 0)
