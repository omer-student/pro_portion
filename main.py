import sys
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

from modules.database import load_database, save_database
from modules.ui_dashboard import DashboardView
from modules.ui_add_recipe import AddRecipeView

THEME = """
    QMainWindow, QWidget {
        background-color: #0E0E0F;
    }
    QLabel {
        color: #CCCCCC;
    }
    QComboBox, QLineEdit, QSpinBox {
        background-color: #161618;
        color: #E5E5E5;
        border: 1px solid #2C2C2E;
        border-radius: 6px;
        padding: 6px 12px;
    }
    QTextEdit {
        background-color: #161618;
        color: #FFFFFF;
        border: 1px solid #2A2A2D;
        border-radius: 8px;
        padding: 14px;
    }
    QPushButton {
        background-color: #161618;
        color: #E5E5E5;
        border: 1px solid #2C2C2E;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #222225;
    }
    QPushButton#actionButton {
        background-color: #A31D1D;
        color: #FFFFFF;
        border: 1px solid #B82323;
    }
    QPushButton#actionButton:hover {
        background-color: #C12727;
    }
"""

class ProPortionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recipe_catalog = load_database()
        self.selected_recipe = list(self.recipe_catalog.keys())[0]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ProPortion — Grams & Volume Scaling")
        self.setMinimumSize(520, 580)
        self.setStyleSheet(THEME)

        self.view_stack = QStackedWidget()
        self.setCentralWidget(self.view_stack)

        self.dashboard_screen = DashboardView(self)
        self.add_recipe_screen = AddRecipeView(self)

        self.view_stack.addWidget(self.dashboard_screen)
        self.view_stack.addWidget(self.add_recipe_screen)
        
        self.refresh_dropdown_ui()
        self.reset_to_recipe_base()

    def refresh_dropdown_ui(self):
        box = self.dashboard_screen.dropdown_box
        box.blockSignals(True)
        box.clear()
        box.addItems(list(self.recipe_catalog.keys()))
        box.setCurrentText(self.selected_recipe)
        box.blockSignals(False)

    def handle_recipe_swap(self, target_recipe_name):
        if target_recipe_name: 
            self.selected_recipe = target_recipe_name
            self.reset_to_recipe_base()

    def reset_to_recipe_base(self):
        base_value = self.recipe_catalog[self.selected_recipe]["base_servings"]
        self.dashboard_screen.servings_input.blockSignals(True)
        self.dashboard_screen.servings_input.setValue(base_value)
        self.dashboard_screen.servings_input.blockSignals(False)
        self.execute_scaling_math(base_value)

    def parse_amount_string(self, text_str):
        """Regex breakdown engine for parsing text chunks like '300ml' or '10.5g' safely."""
        match = re.match(r"([0-9]*\.?[0-9]+)\s*([a-zA-Z]*)", text_str)
        if match:
            return float(match.group(1)), match.group(2)
        return None, text_str

    def execute_scaling_math(self, active_servings):
        active_dataset = self.recipe_catalog[self.selected_recipe]
        initial_servings = active_dataset["base_servings"]
        scale_ratio = active_servings / initial_servings
        compiled_manifest = ""
        
        for ingredient in active_dataset["ingredients"]:
            raw_str = ingredient["amount_str"]
            numeric_val, unit_tag = self.parse_amount_string(raw_str)
            
            if numeric_val is not None:
                calculated = numeric_val * scale_ratio
                calculated_int = int(round(calculated))
                formatted_str = f"{calculated_int}{unit_tag}"
            else:
                formatted_str = raw_str
                
            compiled_manifest += f"•  {formatted_str:<12} | {ingredient['name']}\n"
            
        self.dashboard_screen.manifest_display.setText(compiled_manifest)

    def confirm_and_delete_recipe(self):
        recipe_to_delete = self.selected_recipe

        if len(self.recipe_catalog) <= 1:
            QMessageBox.warning(self, "Action Blocked", "You must retain at least one entry inside storage registries.")
            return

        confirmation = QMessageBox.question(
            self, "Delete Recipe", f"Are you sure you want to permanently delete '{recipe_to_delete}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            del self.recipe_catalog[recipe_to_delete]
            save_database(self.recipe_catalog)
            self.selected_recipe = list(self.recipe_catalog.keys())[0]
            self.refresh_dropdown_ui()
            self.reset_to_recipe_base()

    def abort_form(self):
        scr = self.add_recipe_screen
        scr.input_name.clear()
        scr.staged_ingredients.clear()
        scr.preview_display.clear()
        scr.lbl_form_error.setText("")
        self.view_stack.setCurrentIndex(0)

    def validate_and_commit_recipe(self):
        scr = self.add_recipe_screen
        name = scr.input_name.text().strip()
        base_servings = scr.input_base_servings.value()

        if not name:
            scr.lbl_form_error.setText("Validation Error: Recipe name field cannot remain empty.")
            return

        if not scr.staged_ingredients:
            scr.lbl_form_error.setText("Validation Error: Please stage at least one ingredient.")
            return

        self.recipe_catalog[name] = {
            "base_servings": base_servings,
            "ingredients": list(scr.staged_ingredients)
        }
        save_database(self.recipe_catalog)

        self.selected_recipe = name
        self.abort_form()
        self.refresh_dropdown_ui()
        self.reset_to_recipe_base()


def main():
    app = QApplication(sys.argv)
    window = ProPortionApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()