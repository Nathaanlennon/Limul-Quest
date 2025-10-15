import curses

def charger_map(fichier):
    with open(fichier, "r") as f:
        lignes = [list(l.strip("\n")) for l in f.readlines()]
    return lignes

def trouver_joueur(carte):
    for y, ligne in enumerate(carte):
        for x, c in enumerate(ligne):
            if c == "P":
                return y, x
    return None, None

def afficher_carte(stdscr, carte):
    for y, ligne in enumerate(carte):
        stdscr.addstr(y, 0, "".join(ligne))

def main(stdscr):
    curses.curs_set(0)
    carte = charger_map("map.txt")
    y, x = trouver_joueur(carte)

    while True:
        stdscr.clear()
        afficher_carte(stdscr, carte)
        stdscr.addstr(len(carte), 0, "Utilise les flèches. 'q' pour quitter.")
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break

        new_y, new_x = y, x
        if key == curses.KEY_UP:
            new_y -= 1
        elif key == curses.KEY_DOWN:
            new_y += 1
        elif key == curses.KEY_LEFT:
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            new_x += 1

        # Vérifie les collisions
        if carte[new_y][new_x] != "#":
            carte[y][x] = "."
            carte[new_y][new_x] = "P"
            y, x = new_y, new_x

curses.wrapper(main)