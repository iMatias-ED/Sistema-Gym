from typing import Callable, Dict, Tuple, List
import sqlite3

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QColor

from __feature__ import snake_case, true_property
from .....shared.components.error_message import ErrorMessageDialog, DialogMessage

from ...service import ControlPanelService
from ...classes.user import User

class ConfigureUserDataDialog(QDialog):
    root_layout = QGridLayout()
    inputs_collection: List[ QLineEdit ] = []

    def __init__(self, parent, service:ControlPanelService):
        super(ConfigureUserDataDialog, self).__init__(parent)

        self.users_service = service
        self.users_service.data_changed.connect(self.on_data_changed) 

        self.setup_ui()
        # self.set_window_flags(Qt.FramelessWindowHint)

    def setup_ui(self) -> None:
        self.minimum_width = 450 

        # Products data
        self.title          = self._create_title("Usuarios", self.last_row())
        self.inp_name       = self._create_input("Nombre y Apellido", "Nombre completo", self.last_row(), "full_name")
        self.inp_password   = self._create_input("Contraseña", "Ingrese su contraseña", self.last_row(), "password")
        self.inp_ci         = self._create_input("Cédula de identidad", "Número de Cédula", self.last_row(), "ci")
        self.inp_phone      = self._create_input("Teléfono", "Número de contacto", self.last_row(), "phone")
        self.inp_email      = self._create_input("Correo Electrónico", "ejemplo@gmail.com", self.last_row(), "email")
        self.inp_genre      = self._create_combo_box("Género", ["Masculino", "Femenino"], self.last_row(), "genre")
        

        # Button
        self.submit = QPushButton("Guardar")
        self.root_layout.add_widget(self.submit, self.last_row(), 1, self.last_row(), 2)

        self.set_layout(self.root_layout)

    def last_row(self) -> int:
        return self.root_layout.row_count()

    # Open mode
    def create(self) -> None:
        self._reconnect_submit(self.on_create_submit)
        self.clear()
        self.show()

    @Slot(int)
    def edit(self, user_id:int) -> None:
        user = self.users_service.get_by_id(user_id)

        for inp in self.inputs_collection:
            value = str(getattr(user, inp.object_name))
            inp.text = value

        self.inp_genre.current_index = self.inp_genre.find_text( user.genre )

        self._reconnect_submit(self.on_edit_submit, user.id)
        self.show()
            
    # Signal Slots
    @Slot()
    def on_create_submit(self) -> None:
        try:         
            self.users_service.create( User(self._collect_data()) )
        except sqlite3.IntegrityError as e:
            self.manage_error(e.args[0])

    @Slot()
    def on_edit_submit(self, customer_id:int) -> None:
        try:         
            self.users_service.update( User(self._collect_data(customer_id)) )
        except sqlite3.IntegrityError as e:
            self.manage_error(e.args[0])

    def manage_error(self, error: str):
        if "ci" in error:
            ErrorMessageDialog(self, self.reset_inp_ci).show(DialogMessage(
                "Número de cédula duplicado",
                f'Ya existe un usuario con el número de cédula "{self.inp_ci.text}"'
            ))
        if "phone" in error:
            ErrorMessageDialog(self, self.reset_inp_phone).show(DialogMessage(
                "Número de teléfono duplicado",
                f'Ya existe un usuario con el número de teléfono "{self.inp_phone.text}"'
            ))
        if "email" in error:
            ErrorMessageDialog(self, self.reset_inp_email).show(DialogMessage(
                "Correo electrónico duplicado",
                f'Ya existe un usuario con el email "{self.inp_email.text}"'
            ))
    
    def reset_inp_ci(self):
        self.inp_ci.text = ""
        self.inp_ci.set_focus()

    def reset_inp_phone(self):
        self.inp_phone.text = ""
        self.inp_phone.set_focus()
    
    def reset_inp_email(self):
        self.inp_email.text = ""
        self.inp_email.set_focus()

    @Slot()
    def on_data_changed(self) -> None:
        self.hide()

    # Widgets Creations
    def _create_title(self, text:str, row:int, obj_name:str = "") -> QLabel:
        title = QLabel(text, alignment=Qt.AlignCenter, object_name=obj_name)
        self.root_layout.add_widget(title, row, 1, row, 2)
        return title

    def _create_input(self, title:str, placeholder:str, row:int, obj_name:str = "") -> QLineEdit:
        label = QLabel(title)
        line_edit = QLineEdit(placeholder_text=placeholder, object_name=obj_name)

        self.inputs_collection.append(line_edit)
        self.root_layout.add_widget(label, row, 1)
        self.root_layout.add_widget(line_edit, row, 2)

        return line_edit

    def _create_combo_box(self, title:str, values: List[str], row:int, obj_name:str = "") -> QComboBox:
        label = QLabel(title)
        combo_box = QComboBox(object_name = obj_name)
        # self.inputs_collection.append(combo_box)

        model = combo_box.model()
        for index, genre in enumerate(values):
            combo_box.add_item(genre)
            model.set_data(model.index(index, 0), QColor("white"), Qt.BackgroundRole)
        
        self.root_layout.add_widget(label, row, 1)
        self.root_layout.add_widget(combo_box, row, 2)

        return combo_box

    def _create_date_picker(self, title:str, row:int, obj_name:str = "") -> QLineEdit:
        label = QLabel(title)

        dateEdit = QDateTimeEdit( QDate.current_date(), locale = QLocale.Spanish, display_format = "dd/MM/yyyy", object_name=obj_name)
        dateEdit.calendar_popup = True

        self.inputs_collection.append(dateEdit)
        self.root_layout.add_widget(label, row, 1)
        self.root_layout.add_widget(dateEdit, row, 2)

        return dateEdit
    
    # Utils
    def clear(self) -> None:
        for inp in self.inputs_collection: inp.clear()

    def _collect_data(self, id: int=None) -> Dict:
        data = {}
        for inp in self.inputs_collection:
            data[inp.object_name] = inp.text;

        # Bug when comboBox is added to a list. Loses its value
        # So we can't add it to self.inputs_collection
        data[self.inp_genre.object_name] = self.inp_genre.current_text;

        if id: data["id"] = id
        return data

    def _reconnect_submit(self, connect_to: Callable, parameter=None) -> None:
        try:     self.submit.clicked.disconnect()
        except   RuntimeError: pass
        finally: 
            if parameter:
                self.submit.clicked.connect( lambda: connect_to(parameter) )
            else: self.submit.clicked.connect(connect_to)
