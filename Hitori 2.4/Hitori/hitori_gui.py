from boardgame import BoardGame
from boardgamegui import BoardGameGui, gui_play
from random import randrange
import g2d

CIRCLE = -1
BLACK = -3

class Hitori(BoardGame):

	def __init__(self, side=8):
		#di partenza la matrice è 8x8
		self._cols, self._rows = side,side
		self._matriceOriginale = [[' ' for x in range(self._cols)] for y in range(self._rows)] #matrice per assegnare i valori numerici originari delle celle
		self._valoriGui = [] #matrice che verrà successivamente inizializzata
		self._valori = [[0 for x in range(self._cols)] for y in range(self._rows)] #matrice per assegnare soli valori black e circle
		self._automatismi = 0 #variabile per impostare l'automatismo
		self._regioniChiuse = 0 #variabile per segnare il numero di regioni chiuse

	#metodo per inizializzare la matrice e decidere la sua grandezza
	def initMatriceGui(self, side: int):
		num = randrange(0, 4)
		val = 0
		contRows = 0
		with open("esempi"+str(side)+".txt", "r") as file:
			for linea in file:
				if val >= num * 10 and contRows < int(side):
					rigaNum = linea.strip().split(",")
					self._valoriGui.append(rigaNum)
					contRows += 1
				val += 1

	def getRegioniChiuse(self) -> int:
		return self._regioniChiuse

	def setRegioniChiuse(self, numRegioniChiuse: int):
		self._regioniChiuse = numRegioniChiuse

	def getValAutomatismi(self) -> int:
		return self._automatismi

	def setValAutomatismi(self, valAutomatismo: int):
		self._automatismi = valAutomatismo

	#metodo per tornare un valore numerico originale
	def getElement(self, x: int, y: int) -> int:
		return self._valoriGui[y][x]

	def getMatriceOriginale(self):
		return self._matriceOriginale

	def setMatriceOriginale(self, matrice):
		self._matriceOriginale = matrice

	def getMatriceGui(self):
		return self._valoriGui

	def setMatriceGui(self, matrice):
		self._valoriGui = matrice

	def getMatrice(self):
		return self._valori

	def setMatrice(self, matrice):
		self._valori = matrice

	def cols(self) -> int:
		return self._cols

	def rows(self) -> int:
		return self._rows

	def setCols(self, valCols: int):
		self._cols = valCols

	def setRows(self, valRows: int):
		self._rows = valRows

	#metodo per controllare se ci sono delle regioni di celle bianche non contigue : NON funzionante
	def controlloRegioniBianche(self):
		matriceVal = self.getMatriceGui()
		matrice2 = self.getMatrice()
		cont = 0
		cont2 = 0
		supp = 0
		supp2 = 0
		esito = 0
		esito2 = 0

		# codice per il controllo di regioni di celle bianche non funzionanti
		for x in range(self.rows()):
			for y in range(self.cols()):
				if matrice2[x][y] == BLACK and esito == 0:
					if cont == 0 :
						supp = x
					if x < self.cols()-1 and y < self.cols()-1 :
						if matrice2[x+1][y+1] == BLACK :
							cont += 1
							if cont == 7 - supp:
								self.setRegioniChiuse(self.getRegioniChiuse()+1)
								esito = 1

		for x in range(self.rows()):
			for y in range(self.cols()):
				if matrice2[x][y] == BLACK and esito2 == 0:
					if cont2 == 0 :
						supp2 = y
					if x > 0 and y > 0 :
						if matrice2[x - 1][y - 1] == BLACK:
							cont2 += 1
							if cont2 == 7 - supp2:
								self.setRegioniChiuse(self.getRegioniChiuse()+1)
								esito2 = 1

	def finished(self) -> bool:
		if self.controlloCelleNereColonne() != 0 :
			g2d.alert(self.message("ci sono due celle nere vicine in una colonna"))
		if self.controlloCelleNereRighe() != 0:
			g2d.alert(self.message("ci sono due celle nere vicine in una riga"))
		if self.cellaBiancaChiusa() != 0 :
			g2d.alert(self.message("una o più celle bianche sono chiuse dalle celle nere"))

		if(self.controlloRigheNumeri()/2 == 0 and self.controlloColonneNumeri()/2 == 0 and self.controlloCelleNereRighe() == 0
				and self.controlloCelleNereColonne() == 0 and self.cellaBiancaChiusa() == 0) :
			return True

	#metodo che controlla che non ci siano numeri ripetuti in una riga
	def controlloRigheNumeri(self) -> int:
		matriceVal = self.getMatriceGui()
		matrice2 = self.getMatrice()
		finitoRighe = 0
		# variabili usate per controllare che nel ciclo non venga guardata la cella che si sta già controllando
		cont1R = 0
		cont2R = 0

		for y in range(self.rows()):
			for x in range(self.cols()):
				for val in range(self.cols()):
					if cont2R != cont1R and matriceVal[y][x] == matriceVal[y][val] and matrice2[y][x] != BLACK and matrice2[y][val] != BLACK:
						finitoRighe += 1
					cont1R += 1;
				cont2R += 1;
				cont1R = 0
			cont2R = 0

		return finitoRighe

	# metodo che controlla che non ci siano numeri ripetuti in una colonna
	def controlloColonneNumeri(self) -> int:
		matriceVal = self.getMatriceGui()
		matrice2 = self.getMatrice()
		finitoColonne = 0
		#variabili usate per controllare che nel ciclo non venga guardata la cella che si sta già controllando
		cont1C = 0
		cont2C = 0

		for y in range(self.rows()):
			for x in range(self.cols()):
				for val in range(self.cols()):
					if cont2C != cont1C and matriceVal[x][y] == matriceVal[val][y] and matrice2[x][y] != BLACK and matrice2[val][y] != BLACK:
						finitoColonne += 1
					cont1C += 1;
				cont2C += 1;
				cont1C = 0
			cont2C = 0
		return finitoColonne

	# metodo che controlla che non ci siano celle annerite vicine in una riga
	def controlloCelleNereRighe(self) -> int:
		matrice2 = self.getMatrice()
		finitoNeriR = 0

		for y in range(self.rows()):
			for x in range(self.cols()):
				if x < self.cols()-1:
					if (matrice2[y][x] == BLACK and matrice2[y][x + 1] == BLACK):
						finitoNeriR += 1
		return finitoNeriR

	#metodo che controlla che non ci siano celle annerite vicine in una colonna
	def controlloCelleNereColonne(self) -> int:
		matrice2 = self.getMatrice()
		finitoNeriC = 0

		for y in range(self.rows()):
			for x in range(self.cols()):
				if x < self.cols()-1:
					if (matrice2[x][y] == BLACK and matrice2[x + 1][y] == BLACK):
						finitoNeriC += 1
		return finitoNeriC

	#metodo che controlla se c'è una cella chiusa da celle nere
	def cellaBiancaChiusa(self):
		matriceVal = self.getMatriceGui()
		matrice2 = self.getMatrice()

		celleBiancheChiuse = 0

		try:
			for x in range(self.rows()):
				for y in range(self.cols()):
					if x == 0:
						if y == 0:
							if (matrice2[x + 1][y] == BLACK and matrice2[x][y + 1] == BLACK):
								celleBiancheChiuse += 1
						elif y == self.cols()-1:
							if (matrice2[x + 1][y] == BLACK and matrice2[x][y - 1] == BLACK):
								celleBiancheChiuse += 1
						else:
							if (matrice2[x + 1][y] == BLACK and matrice2[x][y - 1] == BLACK and matrice2[x][
								y + 1] == BLACK):
								celleBiancheChiuse += 1

					elif x == self.cols()-1:
						if y == 0:
							if (matrice2[x - 1][y] == BLACK and matrice2[x][y + 1] == BLACK):
								celleBiancheChiuse += 1
						elif y == self.cols()-1:
							if (matrice2[x - 1][y] == BLACK and matrice2[x][y - 1] == BLACK):
								celleBiancheChiuse += 1
						else:
							if (matrice2[x - 1][y] == BLACK and matrice2[x][y + 1] == BLACK and matrice2[x][
								y - 1] == BLACK):
								celleBiancheChiuse += 1
					else:
						if y == 0:
							if (matrice2[x + 1][y] == BLACK and matrice2[x - 1][y] == BLACK and matrice2[x][
								y + 1] == BLACK):
								celleBiancheChiuse += 1
						elif y == self.cols()-1:
							if (matrice2[x + 1][y] == BLACK and matrice2[x - 1][y] == BLACK and matrice2[x][
								y - 1] == BLACK):
								celleBiancheChiuse += 1
						else:
							if (matrice2[x + 1][y] == BLACK and matrice2[x - 1][y] == BLACK and matrice2[x][
								y + 1] == BLACK and matrice2[x][y - 1] == BLACK):
								celleBiancheChiuse += 1
		except:
			pass

		return celleBiancheChiuse

	#metodo che controlla mossa per i suggerimenti : NON funzionante
	def wrong(self) -> bool:

		if (self.controlloCelleNereRighe() == 0
				and self.controlloCelleNereColonne() == 0 and self.cellaBiancaChiusa() == 0):
			return False
		else :
			return True

	#Suggerimenti : NON funzionante
	def suggerimenti(self):
		matriceVal = self.getMatriceGui()
		matrice2 = self.getMatrice()

		for y in range(self.rows()):
			for x in range(self.cols()):
				supp = matrice2[y][x]
				matrice2[y][x] = BLACK
				self.setMatrice(matrice2)
				if self.wrong() :
					matrice2[y][x] = 0
					self.setMatrice(matrice2)
					self.flag_at(x,y)
				else :
					matrice2[y][x] = 0
					self.setMatrice(matrice2)
					self.play_at(x,y,0)

	#Automatismi: metodo per annerire in automatico in base alla celle cerchiate
	def annerireAuto(self,x1: int, y1: int):
		matrice = self.getMatriceGui()
		matriceVal = self.getMatrice()

		for y in range (self.rows()) :
			if matrice[x1][y] == matrice[x1][y1] and y != y1:
				self.play_at(y,x1,1)

		for x in range (self.cols()) :
			if matrice[x][y1] == matrice[x1][y1] and x != x1:
				self.play_at(y1,x,1)

	#metodo per annerire una cella
	def play_at(self, x: int, y: int, val: int):
		matriceVal = self.getMatrice()
		matrice = self.getMatriceGui()
		matOriginale = self.getMatriceOriginale()

		matOriginale[y][x] = matrice[y][x] #salva il valore numerico che c'era prima che la cella fosse annerita
		matriceVal[y][x] = BLACK

		#se attivato l'automatismo cerchia le celle automaticamente
		auto = self.getValAutomatismi()
		if auto == 1 and val == 0:
			if x == 0:
				if y == 0:
					self.flag_at(x, y + 1)
					self.flag_at(x + 1, y)
				elif y == self.cols()-1:
					self.flag_at(x, y - 1)
					self.flag_at(x + 1, y)
				else:
					self.flag_at(x, y - 1)
					self.flag_at(x, y + 1)
					self.flag_at(x + 1, y)
			elif x == self.cols()-1:
				if y == 0:
					self.flag_at(x, y + 1)
					self.flag_at(x - 1, y)
				elif y == self.cols()-1:
					self.flag_at(x, y - 1)
					self.flag_at(x - 1, y)
				else:
					self.flag_at(x, y - 1)
					self.flag_at(x, y + 1)
					self.flag_at(x - 1, y)
			else:
				if y == 0:
					self.flag_at(x, y + 1)
					self.flag_at(x-1, y)
					self.flag_at(x + 1, y)
				elif y == self.cols()-1:
					self.flag_at(x, y - 1)
					self.flag_at(x - 1, y)
					self.flag_at(x + 1, y)
				else:
					self.flag_at(x,y+1)
					self.flag_at(x, y - 1)
					self.flag_at(x+1, y )
					self.flag_at(x-1, y )
		
		self.setMatriceOriginale(matOriginale)
		self.setMatrice(matriceVal)

	#metodo per cerchiare una cella
	def flag_at(self, x: int, y: int):
		matrice = self.getMatriceGui()
		matriceVal = self.getMatrice()
		matOriginale = self.getMatriceOriginale()

		matOriginale[y][x] = matrice[y][x] #salva il valore numerico che c'era prima che la cella fosse cerchiata
		matriceVal[y][x] = CIRCLE

		self.setMatriceOriginale(matOriginale)
		self.setMatrice(matriceVal)

		#se attivato l'automatismo chiama il metodo annerireAuto()
		auto = self.getValAutomatismi()
		if auto == 1:
			self.annerireAuto(y,x)

	#metodo che serve per ritornare il valore numerico originale per una cella annerita o cerchiata
	def returnOldValue(self, x: int, y: int) -> int:
		matrice = self.getMatriceOriginale()
		matrice2 = self.getMatrice()

		matrice2[y][x] = matrice[y][x]

		self.setMatrice(matrice2)

		return matrice[y][x]

	#metodo per ritornare il valore aggiornato di una cella
	def value_at(self, x: int, y: int):
		matriceVal = self.getMatrice()
		matrice = self.getMatriceGui()

		if matriceVal[x][y] != BLACK and matriceVal[x][y] != CIRCLE :
			return matrice[x][y]
		else :
			return matriceVal[x][y]

	def message(self, str) -> str:
		return str


def main():

	game = Hitori()
	gui_play(game)

main()