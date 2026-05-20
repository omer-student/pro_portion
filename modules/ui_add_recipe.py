from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QTextEdit, QLineEdit, QPushButton
from PySide6.QtGui import QFont

class AddRecipeView(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent = parent_window
        self.staged_ingredients = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        lbl_title = QLabel("Create New Recipe")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #D32F2F;")
        layout.addWidget(lbl_title)

        # General details fields
        layout.addWidget(QLabel("Recipe Name:"))
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("e.g., Sourdough Bread")
        layout.addWidget(self.input_name)

        layout.addWidget(QLabel("Base Servings Allocation:"))
        self.input_base_servings = QSpinBox()
        self.input_base_servings.setRange(1, 100)
        self.input_base_servings.setValue(4)
        layout.addWidget(self.input_base_servings)

        # Divider
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background-color: #232325; margin: 5px 0px;")
        layout.addWidget(sep)

        # Two distinct simple text input fields
        layout.addWidget(QLabel("Add Ingredients Individually:"))
        
        input_row = QHBoxLayout()
        
        self.ing_amount_str = QLineEdit()
        self.ing_amount_str.setPlaceholderText("Amount (e.g., 250g, 300ml)")
        self.ing_amount_str.setFixedWidth(160)
        
        self.ing_name = QLineEdit()
        self.ing_name.setPlaceholderText("Ingredient label name (e.g., Flour)")
        
        btn_append_item = QPushButton("+ Add Item")
        btn_append_item.clicked.connect(self.stage_single_ingredient)
        
        input_row.addWidget(self.ing_amount_str)
        input_row.addWidget(self.ing_name, stretch=1)
        input_row.addWidget(btn_append_item)
        layout.addLayout(input_row)

        # Visual staging list preview tracker area
        layout.addWidget(QLabel("Staged List Preview:"))
        self.preview_display = QTextEdit()
        self.preview_display.setReadOnly(True)
        self.preview_display.setPlaceholderText("No items added yet.")
        self.preview_display.setFont(QFont("Consolas", 10))
        self.preview_display.setFixedHeight(120)
        layout.addWidget(self.preview_display)

        # Error tracking
        self.lbl_form_error = QLabel("")
        self.lbl_form_error.setStyleSheet("color: #D32F2F; font-weight: bold;")
        layout.addWidget(self.lbl_form_error)

        # Buttons
        row_buttons = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.parent.abort_form)
        
        btn_save = QPushButton("Save Recipe File")
        btn_save.setObjectName("actionButton")
        btn_save.clicked.connect(self.parent.validate_and_commit_recipe)
        
        row_buttons.addStretch()
        row_buttons.addWidget(btn_cancel)
        row_buttons.addWidget(btn_save)
        layout.addLayout(row_buttons)

    def stage_single_ingredient(self):
        self.lbl_form_error.setText("")
        amount = self.ing_amount_str.text().strip()
        name = self.ing_name.text().strip()

        if not amount or not name:
            self.lbl_form_error.setText("Error: Both amount text and name label fields must be completed.")
            return

        self.staged_ingredients.append({
            "name": name,
            "amount_str": amount
        })

        self.ing_amount_str.clear()
        self.ing_name.clear()
        self.refresh_preview_window()

    def refresh_preview_window(self):
        if not self.staged_ingredients:
            self.preview_display.clear()
            return
            
        preview_text = ""
        for idx, item in enumerate(self.staged_ingredients, start=1):
            preview_text += f"[{idx}] {item['amount_str']} — {item['name']}\n"
        self.preview_display.setText(preview_text)