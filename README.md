# sublime-config

My Sublime Text 4 setup for Laravel (PHP, Blade, Tailwind, Vue/React via Inertia), with a Catppuccin Mocha look and a Spotlight-style Command Palette.

> **Forgot a shortcut?** Press **⌘⌥K** in Sublime. It lists every shortcut below, is searchable, and runs whatever you pick.

## Shortcuts

### Mine

| Keys | Action |
|---|---|
| ⌘⌥K | Show all shortcuts (cheat sheet) |
| ⌘B | Toggle file explorer (it's on the right) |
| ⌘⌥J | Toggle terminal panel (shell in project root) |
| ⌘⌥G | Laravel Goto: jump to the view / route / config / env key under the cursor |
| ⌘⌥T | Run all tests (`php artisan test`) |
| ⌘⌥⇧T | Run tests in current file |
| ⌘⌥I | Open Tinker |

### Laravel commands (⌘⇧P, type "Laravel")

| Command | Runs |
|---|---|
| Laravel: Dev Server | `composer run dev` |
| Laravel: Test Suite | `php artisan test` |
| Laravel: Test Current File | `php artisan test <file>` |
| Laravel: Tinker | `php artisan tinker` |
| Laravel: Migrate | `php artisan migrate` |
| Laravel: Fresh Migrate + Seed | `php artisan migrate:fresh --seed` |
| Laravel: Route List | `php artisan route:list` |
| Laravel: Clear All Caches | `php artisan optimize:clear` |
| Laravel: Pint Whole Project | `vendor/bin/pint` |
| Laravel: Artisan… | `php artisan list`, then a shell |

### Built-in ones worth knowing

| Keys | Action |
|---|---|
| ⌘P | Goto Anything (open file) |
| ⌘⇧P | Command Palette |
| ⌘R | Goto symbol in file |
| ⌘⇧R | Goto symbol in project |
| ⌘⌥↓ | Goto definition |
| ⌃- | Jump back |
| ⌃0 | Focus file explorer (Esc to go back) |
| ⌘D | Select next occurrence |
| ⌃⌘G | Select all occurrences |
| ⌘⇧L | Split selection into lines (multi-cursor) |
| ⌘L | Select line |
| ⌘⇧D | Duplicate line |
| ⌃⇧K | Delete line |
| ⌘/ | Toggle comment |

## What's in here

- **Language servers:** Intelephense (PHP 8.5), Laravel, TypeScript, Vue, Tailwind, ESLint, JSON
- **Formatting on save:** Laravel Pint for `.php` (via `User/laravel_pint.py`, only in projects with `vendor/bin/pint`), Prettier for JS/TS/Vue/CSS (only in projects with a Prettier config)
- **Syntax:** Blade, Vue, `.env`, plus EditorConfig, Emmet, AutoFileName
- **Terminal:** Terminus, used by the test/tinker/artisan shortcuts
- **Look:** Catppuccin Mocha on pure black, JetBrains Mono everywhere, square tabs, themed title bar, file explorer on the right
- **Spotlight palette:** `User/Adaptive.sublime-theme` + `User/theme/*.png` (rounded corners, accent border, bigger input)

## Files

| File | What it is |
|---|---|
| `Preferences.sublime-settings` | Editor settings |
| `Package Control.sublime-settings` | Package list (installed automatically) |
| `Default (OSX).sublime-keymap` | My shortcuts. The `//` comment above each one is its label in the ⌘⌥K cheat sheet |
| `Laravel.sublime-commands` | The "Laravel: …" palette commands |
| `Adaptive.sublime-theme`, `theme/` | Spotlight-style UI override. Accent color is at the top |
| `shortcuts.py` | The ⌘⌥K cheat sheet |
| `laravel_pint.py` | Pint on save |
| `LSP*.sublime-settings`, `JsPrettier…` | Language server / formatter settings |

## Setup on a new Mac

1. Install [Sublime Text 4](https://www.sublimetext.com/) and a font called **JetBrains Mono** (`brew install --cask font-jetbrains-mono`).
2. Install PHP with [Herd](https://herd.laravel.com/) (Pint on save expects `~/.config/herd-lite/bin`) and Node (for the language servers).
3. Quit Sublime, then:
   ```sh
   git clone <this repo> ~/projects/sublime-config
   ~/projects/sublime-config/install.sh
   ```
4. Open Sublime. If Package Control isn't there yet: ⌘⇧P → "Install Package Control". Restart once and all packages install.

`install.sh` symlinks `~/Library/Application Support/Sublime Text/Packages/User` to this repo's `User/` folder, so any setting you change in Sublime lands in the repo. Commit and push as usual.

## Adding a shortcut

Add it to `User/Default (OSX).sublime-keymap` with a comment on the line above:

```jsonc
// Open the routes file
{ "keys": ["super+alt+r"], "command": "open_file", "args": { "file": "${folder}/routes/web.php" } },
```

It shows up in ⌘⌥K automatically. Update the table above too if you want it on GitHub.
