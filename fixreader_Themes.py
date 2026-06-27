#!/usr/bin/env python3
"""
FIXReader theme manager.

Usage:
  python fixreader_Themes.py --list
  python fixreader_Themes.py --set "south_of_heaven"
  python fixreader_Themes.py --today
  python fixreader_Themes.py --preview "and_justice_for_all"
"""

import argparse
import json
import os
import sys
from datetime import date

THEMES_FILE       = os.path.join(os.path.dirname(__file__), 'fixreader_data', 'themes.json')
ACTIVE_THEME_FILE = os.path.join(os.path.dirname(__file__), 'fixreader_active_theme.json')

COLOR_RESET  = '\033[0m'
COLOR_BOLD   = '\033[1m'
COLOR_DIM    = '\033[2m'
COLOR_GREEN  = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_CYAN   = '\033[96m'
COLOR_RED    = '\033[91m'
COLOR_WHITE  = '\033[97m'


def load_themes():
    with open(THEMES_FILE) as f:
        themes = json.load(f)
    return {t['name']: t for t in themes}


def load_active_name():
    try:
        with open(ACTIVE_THEME_FILE) as f:
            return json.load(f).get('active_theme', 'default')
    except FileNotFoundError:
        return 'default'


def save_active_name(name):
    data = {'active_theme': name, 'manual_date': date.today().isoformat()}
    with open(ACTIVE_THEME_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def hex_to_ansi_bg(hex_color):
    """Convert a hex color to an ANSI 24-bit background escape."""
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f'\033[48;2;{r};{g};{b}m'
    except Exception:
        return ''


def hex_to_ansi_fg(hex_color):
    """Convert a hex color to an ANSI 24-bit foreground escape."""
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f'\033[38;2;{r};{g};{b}m'
    except Exception:
        return ''


def print_theme_preview(theme, active_name):
    name   = theme['name']
    dname  = theme['display_name']
    date_s = theme.get('date') or '—'
    desc   = theme.get('description', '')
    colors = theme.get('colors', {})
    is_active = name == active_name

    marker = f'{COLOR_GREEN}● active{COLOR_RESET}' if is_active else ''
    date_label = f'{COLOR_DIM}date: {date_s}{COLOR_RESET}' if date_s != '—' else ''

    header_parts = [f'{COLOR_BOLD}{dname}{COLOR_RESET}', f'{COLOR_DIM}({name}){COLOR_RESET}']
    if marker:
        header_parts.append(marker)
    if date_label:
        header_parts.append(date_label)

    print('  ' + '  '.join(header_parts))
    if desc:
        print(f'  {COLOR_DIM}{desc}{COLOR_RESET}')

    # Render color swatches inline
    swatch_vars = [
        ('--color-bg',         'bg'),
        ('--color-nav-bg',     'nav'),
        ('--color-sidebar-bg', 'sidebar'),
        ('--color-accent',     'accent'),
        ('--color-highlight',  'highlight'),
        ('--color-text',       'text'),
    ]
    swatch_line = '  '
    for var, label in swatch_vars:
        val = colors.get(var, '#888888')
        bg  = hex_to_ansi_bg(val)
        fg  = hex_to_ansi_fg(val)
        swatch_line += f'{bg}  {COLOR_RESET} {COLOR_DIM}{label}:{val}{COLOR_RESET}  '
    print(swatch_line)

    # Print all 8 vars
    for var, val in colors.items():
        print(f'    {COLOR_DIM}{var:<22}{COLOR_RESET} {val}')

    print()


def cmd_list(themes, active_name):
    print()
    print(f'{COLOR_BOLD}{COLOR_CYAN}FIXReader Themes{COLOR_RESET}')
    print(f'{COLOR_DIM}{"─" * 50}{COLOR_RESET}')
    print()
    for theme in themes.values():
        print_theme_preview(theme, active_name)


def cmd_set(themes, name):
    if name not in themes:
        close = [k for k in themes if name.lower() in k.lower()]
        print(f'{COLOR_RED}Theme "{name}" not found.{COLOR_RESET}')
        if close:
            print(f'Did you mean: {", ".join(close)}?')
        sys.exit(1)
    save_active_name(name)
    dname = themes[name]['display_name']
    print(f'{COLOR_GREEN}✓ Active theme set to:{COLOR_RESET} {COLOR_BOLD}{dname}{COLOR_RESET} ({name})')


def cmd_today(themes):
    today = date.today().strftime('%m-%d')
    matched = None
    for theme in themes.values():
        if theme.get('date') == today:
            matched = theme
            break

    if matched:
        name  = matched['name']
        dname = matched['display_name']
        save_active_name(name)
        print(f'{COLOR_CYAN}Today is {today} — matched theme:{COLOR_RESET} {COLOR_BOLD}{dname}{COLOR_RESET}')
        print(f'{COLOR_GREEN}✓ Active theme set to:{COLOR_RESET} {name}')
    else:
        fallback = 'default'
        save_active_name(fallback)
        print(f'{COLOR_DIM}No theme scheduled for {today}. Falling back to default.{COLOR_RESET}')
        print(f'{COLOR_GREEN}✓ Active theme set to:{COLOR_RESET} default')


def cmd_preview(themes, active_name, name):
    if name not in themes:
        close = [k for k in themes if name.lower() in k.lower()]
        print(f'{COLOR_RED}Theme "{name}" not found.{COLOR_RESET}')
        if close:
            print(f'Did you mean: {", ".join(close)}?')
        sys.exit(1)
    print()
    print(f'{COLOR_BOLD}{COLOR_CYAN}Preview — {themes[name]["display_name"]}{COLOR_RESET}')
    print(f'{COLOR_DIM}{"─" * 50}{COLOR_RESET}')
    print()
    print_theme_preview(themes[name], active_name)
    print(f'{COLOR_DIM}(Not activated — use --set "{name}" to apply){COLOR_RESET}')
    print()


def main():
    parser = argparse.ArgumentParser(
        description='FIXReader theme manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list',    action='store_true',  help='Show all available themes')
    group.add_argument('--set',     metavar='THEME',      help='Activate a theme by name')
    group.add_argument('--today',   action='store_true',  help='Auto-select theme based on today\'s date')
    group.add_argument('--preview', metavar='THEME',      help='Preview a theme without activating it')

    args = parser.parse_args()

    try:
        themes = load_themes()
    except FileNotFoundError:
        print(f'{COLOR_RED}themes.json not found at {THEMES_FILE}{COLOR_RESET}')
        sys.exit(1)

    active_name = load_active_name()

    if args.list:
        cmd_list(themes, active_name)
    elif args.set:
        cmd_set(themes, args.set)
    elif args.today:
        cmd_today(themes)
    elif args.preview:
        cmd_preview(themes, active_name, args.preview)


if __name__ == '__main__':
    main()
