import sigil
import curses, curses.panel

class State():
    STATE_SELECT_CARD = 1
    STATE_SELECT_SLOT = 2

    def __init__(self):
        self.state = self.STATE_SELECT_CARD
        self.selectedCard = None
        self.selectedSlot = None


def make_card(h, w, y, x, card):
    CARD_COLOR = curses.color_pair(1)
    CARD_COLOR_HEART = curses.color_pair(3)

    win = curses.newwin(h, w, y, x)
    win.bkgd(' ',CARD_COLOR)
    win.attron(CARD_COLOR)

    win.erase()
    win.box()
    # cost symbol
    win.addstr(0, w-card.cost-1, '\u25CF'*card.cost, CARD_COLOR_HEART)
    # title
    win.addstr(1, 1, card.name.center(w-2).upper())
    # line under title
    win.addstr(2, 0, '\u251C' + '\u2500'*(w-2) + '\u2524')
    #sigil spots
    win.addch(3, 3, '\u2190')
    win.addch(3, 5, '\u263C')
    #win.addch(3, 1, '\uFB02')

    #win.addch(4, 3, '\u263A')
    #win.addch(4, 5, '\u00A4')

    # attack and heath values
    win.addstr(h-2, 1, str(card.attack))
    win.addstr(h-2, w-2, str(card.health))
    # attack and health symbols
    win.addstr(h-1, 1, '\u2191')  #21A5 didn't work
    win.addstr(h-1, w-2, '\u2665', CARD_COLOR_HEART)
    
    win.attroff(CARD_COLOR)

    panel = curses.panel.new_panel(win)
    return win, panel

def make_slot(h, w, y, x, t=None):
    DRAW_COLOR = curses.color_pair(5)
    win = curses.newwin(h, w, y, x)
    win.bkgd(' ', curses.COLOR_BLACK)
    win.erase()
    fill = '\u2593' 
    if t == 1:
        win.attron(DRAW_COLOR)
        win.addstr(1, 1, fill*7)
        win.addstr(2, 2, fill*5)
        win.addstr(3, 3, fill*3)
        win.addstr(4, 4, fill)
        win.attroff(DRAW_COLOR)
    panel = curses.panel.new_panel(win)
    return win, panel


def test(stdscr):

    CARD_HEIGHT = 6
    CARD_WIDTH = 9
    HAND_Y = 25
    FIELD_Y = 3
    FIELD_X = 5

    DARK_RED = 52
    ORANGE = 172 # or 208 or 214 or 3
    ORANGE2 = 208
    ORANGE3 = 214
    ORANGE4 = 3
    LIGHT_YELLOW = 188
    LIGHT_YELLOW = 11

    state = State()
    fulldeck = sigil.FullDeck()
    playerdeck = sigil.PlayerDeck(fulldeck.draw(2).cards)

    stdscr.keypad(1)
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.flushinp()
    curses.noecho()
    stdscr.clear()

    try:
        curses.curs_set(0)
    except:
        pass

    # test for custom palette.  works on mine
    if curses.has_colors() and curses.can_change_color():
        curses.init_color(curses.COLOR_CYAN, 800, 400, 8)

    curses.init_pair(1, 0, LIGHT_YELLOW)
    curses.init_pair(2, ORANGE, DARK_RED) 
    curses.init_pair(3, curses.COLOR_RED, LIGHT_YELLOW)
    curses.init_pair(4, DARK_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, DARK_RED)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)

    BACKGROUND_COLOR = curses.color_pair(4)
    FIELD_COLOR = curses.COLOR_BLACK
    COLOR_DEBUG= curses.color_pair(6)

    # background
    screensize = curses.LINES * curses.COLS
    stdscr.bkgd(curses.ACS_CKBOARD,BACKGROUND_COLOR)
    
    fieldwindows=[]
    panels = []

    # draw the field
    for y in range (3):
        for x in range(4):
            slotx = FIELD_X + x*CARD_WIDTH + x
            sloty = FIELD_Y + y*CARD_HEIGHT + y
            if y == 0:
                t = 1
            else:
                t = None
            w, p = make_slot(CARD_HEIGHT, CARD_WIDTH, sloty, slotx, t)
            panels.append(p)

    curses.panel.update_panels(); stdscr.refresh()

    # draw the hand
    c = 0
    for card in playerdeck.cards:
        w, p = make_card(CARD_HEIGHT, CARD_WIDTH, HAND_Y, c*CARD_WIDTH + c*1 + 1, card)
        panels.append(p)
        c += 1

    curses.panel.update_panels(); stdscr.refresh()

    # panel1.top(); curses.panel.update_panels(); stdscr.refresh()

    """
    for i in range(20):
        panel2.move(8, 8+i)
        curses.panel.update_panels(); stdscr.refresh()
        sleep(0.1)
    """

    while True:
        event = stdscr.getch()
        stdscr.addstr(1, 1, str(event), COLOR_DEBUG)
        if event == ord('q'): #quit
            break
        elif event == 27: #Esc or Alt
            stdscr.nodelay(True)
            n = stdscr.getch()
            stdscr.nodelay(False)
            if n == -1:
                # Escape was pressed
                break
        elif event == curses.KEY_MOUSE:
            _, mx, my, _, ms  = curses.getmouse()
            msg = '(%i,%i)' % (mx, my)
            stdscr.addstr(1, 1, msg, COLOR_DEBUG)


def colortest(stdscr):
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i, 0, i)
    try:
        for i in range(0, 255):
            stdscr.addstr(' ' + str(i), curses.color_pair(i))
    except curses.ERR:
        # End of screen reached
        pass
    stdscr.getch()


curses.wrapper(test)


