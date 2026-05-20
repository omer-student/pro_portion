from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QTextEdit, QComboBox, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class DashboardView(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        # Header Block
        logo_container = QHBoxLayout()
        logo_text = QLabel("PRO-PORTION")
        logo_text.setStyleSheet("font-family: Arial; font-size: 24px; font-weight: 900; letter-spacing: 2px; color: #D32F2F;")
        logo_subline = QLabel(" /  METRIC SCALE")
        logo_subline.setStyleSheet("color: #555555; font-size: 11px; font-weight: bold; padding-top: 8px;")
        
        logo_container.addWidget(logo_text)
        logo_container.addWidget(logo_subline)
        logo_container.addStretch()

        # Switch to Add Screen
        btn_go_add = QPushButton("+ Add Recipe")
        btn_go_add.clicked.connect(lambda: self.parent.view_stack.setCurrentIndex(1))
        logo_container.addWidget(btn_go_add)
        layout.addLayout(logo_container)

        # Divider Line
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #232325;")
        layout.addWidget(sep)

        # ONE Single Dropdown Selection Box with the Delete Button right next to it
        row_dropdown = QHBoxLayout()
        lbl_recipe = QLabel("Active Recipe:")
        lbl_recipe.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        self.dropdown_box = QComboBox()
        self.dropdown_box.addItems(list(self.parent.recipe_catalog.keys()))
        self.dropdown_box.currentTextChanged.connect(self.parent.handle_recipe_swap)
        
        self.btn_delete = QPushButton("🗑 Delete")
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #1A1A1E;
                color: #CF6679;
                border: 1px solid #3A2428;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #3A1F22;
            }
        """)
        self.btn_delete.clicked.connect(self.parent.confirm_and_delete_recipe)
        
        row_dropdown.addWidget(lbl_recipe)
        row_dropdown.addWidget(self.dropdown_box, stretch=1)
        row_dropdown.addWidget(self.btn_delete)
        layout.addLayout(row_dropdown)

        # Target Servings Counter Row
        row_servings = QHBoxLayout()
        lbl_servings = QLabel("Target Servings:")
        lbl_servings.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        self.servings_input = QSpinBox()
        self.servings_input.setRange(1, 1000)
        self.servings_input.setFixedWidth(100)
        self.servings_input.valueChanged.connect(self.parent.execute_scaling_math)
        
        row_servings.addWidget(lbl_servings)
        row_servings.addWidget(self.servings_input)
        row_servings.addStretch()
        layout.addLayout(row_servings)

        # Output Display Box
        lbl_manifest = QLabel("Proportional Weight Manifest")
        lbl_manifest.setStyleSheet("color: #555555; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;")
        layout.addWidget(lbl_manifest)
        
        self.manifest_display = QTextEdit()
        self.manifest_display.setReadOnly(True)
        self.manifest_display.setFont(QFont("Consolas", 11))
        layout.addWidget(self.manifest_display)