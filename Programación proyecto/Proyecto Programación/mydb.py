import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox, QListWidget
)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_database()  # Crear la base de datos y la tabla
        self.load_data()  # Cargar datos al inicio

    def initUI(self):
        self.setWindowTitle('Registro de Gastos')
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()

        # Formulario para introducir datos
        self.form_layout = QFormLayout()

        
        self.descripcion_input = QLineEdit()
        self.montopresupuestado_input = QLineEdit()
        self.montoreal_input = QLineEdit()
        self.categoria_input = QLineEdit()
        self.fecha_input = QLineEdit()

        
        self.form_layout.addRow('Descripción:', self.descripcion_input)
        self.form_layout.addRow('Gasto presupuestado', self.montopresupuestado_input)
        self.form_layout.addRow('Monto Real:', self.montoreal_input)
        self.form_layout.addRow('Categoría:', self.categoria_input)
        self.form_layout.addRow('Fecha:', self.fecha_input)

        self.layout.addLayout(self.form_layout)

        self.submit_button = QPushButton('Registrar Gasto')
        self.submit_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.submit_button)

        # Lista para mostrar los gastos registrados
        self.gastos_list = QListWidget()
        self.layout.addWidget(self.gastos_list)

        self.setLayout(self.layout)

    def create_database(self):
        # Conectar a la base de datos (se creará si no existe)
        conn = sqlite3.connect('gastos.db')
        cursor = conn.cursor()

        # Crear una tabla
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            gastosid INTEGER PRIMARY KEY AUTOINCREMENT,
            montopresupuestado REAL NOT NULL,
            descripcion TEXT NOT NULL,
            montoreal REAL NOT NULL,
            categoria TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
        ''')
        conn.commit()
        conn.close()

    def submit_data(self):
        # Obtener los datos del formulario
        montopresupuestado = self.montopresupuestado_input.text()
        descripcion = self.descripcion_input.text()
        montoreal = self.montoreal_input.text()
        categoria = self.categoria_input.text()
        fecha = self.fecha_input.text()

        # Validar que el monto real sea un número
        try:
            montoreal = float(montoreal)
        except ValueError:
            QMessageBox.warning(self, 'Error', 'El monto real debe ser un número.')
            return

        # Conectar a la base de datos
        conn = sqlite3.connect('gastos.db')
        cursor = conn.cursor()

        # Insertar los datos en la tabla
        cursor.execute('''
        INSERT INTO gastos (montopresupuestado, descripcion, montoreal, categoria, fecha)
        VALUES (?, ?, ?, ?, ?)
        ''', (montopresupuestado, descripcion, montoreal, categoria, fecha))

        # Guardar (commit) los cambios y cerrar la conexión
        conn.commit()
        conn.close()

        # Limpiar los campos
        self.montopresupuestado_input.clear()
        self.descripcion_input.clear()
        self.montoreal_input.clear()
        self.categoria_input.clear()
        self.fecha_input.clear()

        QMessageBox.information(self, 'Éxito', 'Gasto registrado exitosamente.')
        
        # Cargar nuevamente los datos para mostrar en la lista
        self.load_data()

    def load_data(self):
        # Limpiar la lista antes de cargar nuevos datos
        self.gastos_list.clear()

        # Conectar a la base de datos
        conn = sqlite3.connect('gastos.db')
        cursor = conn.cursor()

        # Consultar los datos
        cursor.execute("SELECT montopresupuestado, descripcion, montoreal, categoria, fecha FROM gastos")
        rows = cursor.fetchall()

        # Agregar los datos a la lista
        for row in rows:
            self.gastos_list.addItem(f'Gasto: {row[0]}, Descripción: {row[1]}, Monto: {row[2]}, Categoría: {row[3]}, Fecha: {row[4]}')

        # Cerrar la conexión
        conn.close()

# Crear y ejecutar la aplicación
app = QApplication(sys.argv)
ex = App()
ex.show()
sys.exit(app.exec_())