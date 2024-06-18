import sys
import locale
import time
import win32gui, win32con
from ctypes import windll
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem
from PyQt6.QtGui import QPainter, QImage, QFont
from PyQt6.QtCore import Qt, QPoint, QTimer, QEvent

locale.setlocale(locale.LC_TIME, '')

# Opciones del reloj
FRASE_8 = True

def opciones():
	global RUTA_DE_LA_IMAGEN, ESCALA, USUARIO, FUENTE, COLOR, TAMAÑO_GLOBAL_DE_FUENTE, SALUDO_CAMBIA_CON_LA_HORA, FRASE_1, FRASE_2, FRASE_3, FRASE_4, SALUDO, FRASE_5, FRASE_6, FRASE_7, HORA_24H, HORA_12H, FRASE_9, FRASE_10
	
	RUTA_DE_LA_IMAGEN = 'YuYuYu/Itsuki.png'
	ESCALA = 0.675

	USUARIO = 'Jhonny'
	FUENTE = 'Please write me a song'
	COLOR = '#565151'
	TAMAÑO_GLOBAL_DE_FUENTE = 20

	FRASE_1 = '¡Hola!'
	FRASE_2 = '¡Buenos días!'
	FRASE_3 = '¡Buenas tardes!'
	FRASE_4 = '¡Buenas noches!'

	SALUDO = saludo_especial(time.strftime('%d/%m'))

	FRASE_5 = (f'Hoy es {time.strftime('%A')},')
	FRASE_6 = time.strftime('%d de %B de %Y')
	FRASE_7 = 'Son las'
	# Frase 8
	HORA_24H = time.strftime('%H:%M')
	HORA_12H = time.strftime('%I:%M')
	FRASE_9 = time.strftime('%S')
	FRASE_10 = 'PM' if int(time.strftime('%H')) > 12 else 'AM'

def saludo(hora: str, cambiar_con_hora: bool = True):
	global FRASE_1, FRASE_2, FRASE_3, FRASE_4

	if not cambiar_con_hora:
		return FRASE_1
	
	hora = int(hora)
	if hora in range(6, 11):
		return FRASE_2
	elif hora in range(12, 17):
		return FRASE_3
	elif hora in range(18, 23) or range(0, 5):
		return FRASE_4

def saludo_especial(fecha: str):
	global USUARIO
	match fecha:
		case '21/05':
			diálogo = f'¡Feliz cumpleaños, {USUARIO}!'
		case '01/01':
			diálogo = '¡Feliz año nuevo!'
		case '24/12' | '25/12':
			diálogo = '¡Feliz navidad!'
		case '31/12':
			diálogo = f'¡Feliz año {int(time.strftime('%Y')) + 1}!'
		case _:
			diálogo = saludo(time.strftime('%H'))
		
	return diálogo

# Código
class Ventana(QWidget):
	def __init__(self, *args, **kwargs):
		super(Ventana, self).__init__(*args, **kwargs)
		self.setWindowTitle('Reloj de Itsuki')
		self.initUI()
		self.show()

		if sys.platform == 'win32':
			win32gui.SetWindowPos(self.winId(),win32con.HWND_BOTTOM, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
			hwnd = win32gui.GetWindow(win32gui.GetWindow(windll.user32.GetTopWindow(0), win32con.GW_HWNDLAST), win32con.GW_CHILD)
			win32gui.SetWindowLong(self.winId(), win32con.GWL_HWNDPARENT, hwnd)

	def initUI(self):
		self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.determinar_tamaño_y_posición()
		self.distribuir_espacio()
		self.colocar_textos()
		self.formato_del_reloj()

		self.timer = QTimer()
		self.timer.timeout.connect(self.actualizar)
		self.timer.start(1000)

	def determinar_tamaño_y_posición(self):
		global RUTA_DE_LA_IMAGEN
		self.imagen = QImage(RUTA_DE_LA_IMAGEN)
		self.imagen = self.imagen.scaled(self.imagen.size() * ESCALA, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

		self.setFixedSize(self.sizeHint())
		posición_inicial = self.screen().size() - self.sizeHint()
		self.move(posición_inicial.width(), posición_inicial.height())

	def sizeHint(self):
		return self.imagen.size()
	
	def distribuir_espacio(self):
		self.organizador_de_espacio = QVBoxLayout()
		self.organizador_de_espacio.setContentsMargins(0, 0, 0, 0)
		self.organizador_de_espacio.setSpacing(0)
		self.setLayout(self.organizador_de_espacio)

		self.espaciador = QHBoxLayout()
		self.espaciador.setContentsMargins(0, 0, 0, 0)
		self.espaciador.setSpacing(0)

		self.organizador_de_espacio.addSpacerItem(QSpacerItem(int(404 * ESCALA), int(406 * ESCALA)))
		self.organizador_de_espacio.addLayout(self.espaciador)
		self.organizador_de_espacio.addSpacerItem(QSpacerItem(int(404 * ESCALA), int(94 * ESCALA)))

		self.organizador = QVBoxLayout()

		self.espaciador.addSpacerItem(QSpacerItem(int(77 * ESCALA), int(206 * ESCALA)))
		self.espaciador.addLayout(self.organizador)
		self.espaciador.addSpacerItem(QSpacerItem(int(38 * ESCALA), int(206 * ESCALA)))

	def colocar_textos(self):
		self.organizador.setContentsMargins(0, int(10 * ESCALA), 0, 0)
		self.organizador.setSpacing(0)

		self.fuente = QFont(
			FUENTE,
			int(
				(TAMAÑO_GLOBAL_DE_FUENTE * 0.9) * ESCALA
			)
		)
		self.fuente_hora = QFont(
			FUENTE,
			int(
				(TAMAÑO_GLOBAL_DE_FUENTE * 1.5) * ESCALA
			)
		)
		self.fuente_segundero = QFont(
			FUENTE,
			int(
				((TAMAÑO_GLOBAL_DE_FUENTE * 1.5) * ESCALA) / 2
			)
		)

		self.línea_1 = self.crear_etiqueta(SALUDO, self.fuente)
		self.línea_2 = self.crear_etiqueta(' ', self.fuente)
		self.línea_3 = self.crear_etiqueta(FRASE_5, self.fuente)
		self.línea_4 = self.crear_etiqueta(FRASE_6, self.fuente)
		self.línea_5 = self.crear_etiqueta(' ', self.fuente)
		self.línea_6 = self.crear_etiqueta(FRASE_7, self.fuente)
		self.línea_7 = self.crear_etiqueta(HORA_24H, self.fuente_hora)
		self.línea_7_0 = self.crear_etiqueta(FRASE_9, self.fuente_segundero)
		self.línea_7_5 = self.crear_etiqueta(FRASE_10, self.fuente_segundero)

		self.reloj = QHBoxLayout()
		self.reloj.setContentsMargins(0, 0, 0, 0)
		self.reloj.setSpacing(5)
		self.segundero = QVBoxLayout()
		self.segundero.setContentsMargins(0, 0, 0, 0)
		self.segundero.setSpacing(0)

		self.reloj.addStretch()
		self.reloj.addWidget(self.línea_7)
		self.reloj.addLayout(self.segundero)
		self.segundero.addWidget(self.línea_7_0)
		self.segundero.addWidget(self.línea_7_5)
		self.segundero.addStretch()
		self.reloj.addStretch()

		self.organizador.addStretch()
		self.organizador.addWidget(self.línea_1)
		self.organizador.addWidget(self.línea_2)
		self.organizador.addWidget(self.línea_3)
		self.organizador.addWidget(self.línea_4)
		self.organizador.addWidget(self.línea_5)
		self.organizador.addWidget(self.línea_6)
		self.organizador.addLayout(self.reloj)
		self.organizador.addStretch()

		self.línea_7.mousePressEvent = lambda evento: self.formato_del_reloj(True)

	def crear_etiqueta(self, texto, fuente):
		global COLOR
		label = QLabel(self)
		label.setText(texto)
		label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		label.setFont(fuente)
		label.setContentsMargins(0, 0, 0, 0)
		label.setStyleSheet(f'color: {COLOR}')

		return label
	
	def formato_del_reloj(self, call_by_lambda = False):
		global FRASE_8, HORA_24H, HORA_12H
		if call_by_lambda:
			FRASE_8 = not FRASE_8

		if FRASE_8:
			self.línea_7.setText(HORA_24H)
			self.línea_7_5.hide()
		else:
			self.línea_7.setText(HORA_12H)
			self.línea_7_5.show()


	def actualizar(self):
		opciones()

		self.línea_1.setText(SALUDO)
		self.línea_3.setText(FRASE_5)
		self.línea_4.setText(FRASE_6)
		self.línea_6.setText(FRASE_7)
		self.formato_del_reloj()
		self.línea_7_0.setText(FRASE_9)

	def paintEvent(self, evento: QEvent):
		dibujante = QPainter(self)
		dibujante.drawImage(QPoint(0, 0), self.imagen)

	def keyPressEvent(self, event: QEvent):
		if event.modifiers() == Qt.KeyboardModifier.AltModifier:
			if event.key() == Qt.Key.Key_F4:
				self.close()

	def mousePressEvent(self, event: QEvent):
		if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
			self.oldPos = event.globalPosition().toPoint()

	def mouseMoveEvent(self, event: QEvent):
		if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
			delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPosition().toPoint()

if __name__ == '__main__':
	opciones()
	aplicacion = QApplication(sys.argv)
	widget = Ventana()
	sys.exit(aplicacion.exec())
