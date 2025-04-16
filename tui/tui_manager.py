#!/usr/bin/env python3
"""
TUI Manager for the AI Ecosystem

A curses-based interface that displays the current configuration and recent log snippets.
Press 'q' to quit; press 'r' to trigger reconfiguration.
"""
import curses, json, time
from pathlib import Path
CONFIG_PATH = Path(__file__).parent.parent / "config/system_parameters.json"
LOG_PATH = Path(__file__).parent.parent / "logs/execution_engine.log"
def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)
def read_log(lines=10):
    with open(LOG_PATH) as f:
        return f.readlines()[-lines:]
def draw_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000)
    while True:
        stdscr.erase()
        config = load_config()
        log_entries = read_log(10)
        stdscr.addstr(0, 0, "AI Ecosystem TUI - Press 'q' to quit", curses.A_BOLD)
        stdscr.addstr(2, 0, "Current Configuration:")
        stdscr.addstr(3, 0, json.dumps(config, indent=4))
        stdscr.addstr(10, 0, "Recent Execution Log:")
        for idx, line in enumerate(log_entries):
            stdscr.addstr(12+idx, 0, line.strip())
        stdscr.addstr(24, 0, "Options: (r) Trigger Reconfiguration", curses.A_UNDERLINE)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('r'):
            stdscr.addstr(26, 0, "Reconfiguration triggered...", curses.A_BLINK)
            stdscr.refresh()
            time.sleep(2)
        stdscr.refresh()
curses.wrapper(draw_menu)
