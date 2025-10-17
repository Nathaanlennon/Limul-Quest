import curses

def handle_input(key):
    """Traduit les touches en actions logiques."""
    if key == curses.KEY_RIGHT:
        return "NEXT"
    if key == curses.KEY_LEFT:
        return "PREV"
    if key == ord('q'):
        return "QUIT"
    return None
