import g2d
from boardgame import BoardGame
from time import time

W, H = 60,60
LONG_PRESS = 0.5
BLACK = -3
CIRCLE = -1

class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._downtime = 0
        self._valoriGriglia = [5,6,8]
        #inserimento grandezza lato del campo da gioco
        self._side = int((g2d.prompt(self._game.message("Inserisci la lunghezza del lato che deve essere 5 o 6 o 8 : "))))
        while (self._side != self._valoriGriglia[0] and self._side != self._valoriGriglia[1] and self._side != self._valoriGriglia[2]):
            self._side = int((g2d.prompt(self._game.message("Inserisci la lunghezza del lato che deve essere 5 o 6 o 8 : "))))

        g2d.alert(self._game.message("Premi la barra spaziatrice se vuoi attivare gli automatismi e la freccia verso il basso per disattivare.  "
                                     " Con gli automatismi verrano cerchiate le celle in automatico in base alla cella annerita,"
                                     " e verranno annerite in automatico le celle con un numero già cerchiato nella stessa riga o colonna. "))

    def tick(self):
        #per attivare i suggerimenti
        if g2d.key_pressed("ArrowUp") :
            self._game.suggerimenti()
            self._game.setValAutomatismi(1)
        #per attivare gli automatismi
        if g2d.key_pressed("Spacebar"):
            self._game.setValAutomatismi(1)
        #per disattivare gli automatismi
        if g2d.key_pressed("ArrowDown"):
            self._game.setValAutomatismi(0)
        if g2d.key_pressed("LeftButton"):
            self._downtime = time()
        #per cerchiare le celle
        elif g2d.key_released("LeftButton"):
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            #controllo per considere solo lo spazio cliccato dentro il canvas e non fuori
            if (x < self._game.rows() and x > -1) :
                if ( y < self._game.cols() and y > -1) :
                    if time() - self._downtime > LONG_PRESS:
                        self._game.flag_at(x, y)
                        center = x * W + W // 2, y * H + H // 2
                        #primo cerchio nero più grande
                        g2d.set_color((0, 0, 0))
                        g2d.fill_circle(center,H // 2)
                        #secondo cerchio bianco più piccolo
                        g2d.set_color((255, 255, 255))
                        g2d.fill_circle(center, H // 2 - 4)

                        value = self._game.getElement(x,y)
                        #scrivo il numero dentro il cerchio
                        g2d.set_color((0, 0, 0))
                        g2d.draw_text_centered(value, center, H // 2)

                    else:
                        value = self._game.value_at(y, x)
                        #per togliere una cella nera
                        if value == BLACK :
                            mouse = g2d.mouse_position()
                            x, y = mouse[0] // W, mouse[1] // H
                            val = self._game.returnOldValue(x, y)
                            self.update_buttons(x, y, val)
                        #per togliere un cella cerchiata
                        elif value == CIRCLE :
                            mouse = g2d.mouse_position()
                            x, y = mouse[0] // W, mouse[1] // H
                            val = self._game.returnOldValue(x, y)
                            self.update_buttons(x, y, val)
                        #per annerire una cella
                        else :
                            self._game.play_at(x, y, 0)
                            center = x * W + W // 2, y * H + H // 2
                            g2d.set_color((0,0,0))
                            g2d.fill_rect((x*W+1, y*H+1, W-1, H-1))
                            self.update_buttons(-1,-1,0)

                    if self._game.finished():
                        g2d.alert(self._game.message("hitori finito!!!"))
                        g2d.close_canvas()


    def update_buttons(self,x1: int, y1: int, val: int):
         self._game.initMatriceGui(self._side)
         g2d.clear_canvas()
         g2d.set_color((0, 0, 0))
         self._game.setCols(int(self._side))
         self._game.setRows(int(self._side))
         cols, rows = self._game.cols(), self._game.rows()
         for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
         for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
            for y in range(rows):
                for x in range(cols):
                    value = self._game.value_at(y, x)
                    center = x * W + W // 2, y * H + H // 2
                    #per scrivere il valore numerico originario della cella
                    if y == y1 and x == x1 :
                        if val != 0:
                            g2d.draw_text_centered(val, center, H // 2)
                    else :
                        #riscrivo le celle nere che non ho cancellato
                        if value == BLACK :
                            g2d.set_color((0, 0, 0))
                            g2d.fill_rect((x * W + 1, y * H + 1, W - 1, H - 1))
                        #riscrivo le celle cerchiate che non ho cancellato
                        elif value == CIRCLE :
                            g2d.set_color((0, 0, 0))
                            g2d.fill_circle(center, H // 2)

                            g2d.set_color((255, 255, 255))
                            g2d.fill_circle(center, H // 2 - 4)

                            g2d.set_color((0, 0, 0))
                            element = self._game.getElement(x,y)
                            g2d.draw_text_centered(element, center, H // 2)
                        #riscrivo i numeri delle celle
                        else :
                            g2d.draw_text_centered(value, center, H // 2)
         g2d.update_canvas()


def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    ui.update_buttons(-1,-1,0)
    g2d.main_loop(ui.tick)