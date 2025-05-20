from Classes import DB, Word
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTableWidget, QTableWidgetItem, 
                            QCheckBox, QPushButton, QLineEdit, QHeaderView,
                            QFrame, QMessageBox, QLabel)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from pycccedict.cccedict import CcCedict
import random

ccdict = CcCedict()
FONT = QFont("Arial", 14)  # Adjust size as needed

class ChineseHelperApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize UI
        self.setWindowTitle("Chinese Helper")
        self.resize(1280, 720)
        
        # Initialize database
        self.db = DB()
        
        # Set up the central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create UI components
        self.create_widgets()
        
    def create_widgets(self):
        # Create display section for words
        self.create_display_frame()
        
        # Create input section
        self.create_input_frame()
        
        # Create bottom section
        self.create_bottom_frame()
        
    def create_display_frame(self):
        # Display Frame
        display_frame = QFrame()
        display_layout = QVBoxLayout(display_frame)
        
        # Checkbox Frame
        checkbox_frame = QFrame()
        checkbox_layout = QHBoxLayout(checkbox_frame)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        
        # Checkboxes for toggling columns "Pinyin"
        self.pinyin_checkbox = QCheckBox("Pinyin")
        self.pinyin_checkbox.setChecked(True)
        self.pinyin_checkbox.toggled.connect(self.toggle_pinyin)

        # Checkboxes for toggling columns "Translation"
        self.translation_checkbox = QCheckBox("Translation")
        self.translation_checkbox.setChecked(True)
        self.translation_checkbox.toggled.connect(self.toggle_translation)
        
        # Button for Shuffling
        shuffle_button = QPushButton("Shuffle")
        shuffle_button.clicked.connect(self.shuffle_table_rows)


        # Add checkboxes and button into the Checkbox layout
        checkbox_layout.addWidget(self.pinyin_checkbox)
        checkbox_layout.addWidget(self.translation_checkbox)
        checkbox_layout.addWidget(shuffle_button)
        checkbox_layout.addStretch()
        
        # Table Widget
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Character", "Pinyin", "Translation"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self.handle_item_changed)


        # Column Width
        self.table.setColumnWidth(0, 60) # Char
        self.table.setColumnWidth(1, 100) # Pinyin

        # Set the ResizeMode of the Headers
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        # Load initial data to table
        self.load_data_from_db()
        
        # Add widgets to display layout
        display_layout.addWidget(checkbox_frame)
        display_layout.addWidget(self.table)
        
        # Add display frame to main layout
        self.main_layout.addWidget(display_frame)
        
    def create_input_frame(self):
        # Input Frame
        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.Shape.Box)
        input_layout = QVBoxLayout(input_frame)
        
        # Text field
        self.entry_label = QLabel()
        self.entry_label.setText("Add a New Word")

        # Input field
        self.entry = QLineEdit()
        self.entry.setFont(QFont("Arial", 20))
        self.entry.returnPressed.connect(self.entry_submit)
        
        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.entry_submit)
        
        # Add widgets to input layout
        input_layout.addWidget(self.entry_label)
        input_layout.addWidget(self.entry)
        input_layout.addWidget(self.submit_button)
        
        # Add input frame to main layout
        self.main_layout.addWidget(input_frame)
        
    def create_bottom_frame(self):
        # Bottom Frame
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.database_save)
        
        # Add widget to bottom layout
        bottom_layout.addWidget(self.save_button)
        bottom_layout.addStretch()
        
        # Add bottom frame to main layout
        self.main_layout.addWidget(bottom_frame)
        
    def toggle_pinyin(self, checked):
        """Toggle visibility of the Pinyin column"""
        self.table.setColumnHidden(1, not checked)
        
    def toggle_translation(self, checked):
        """Toggle visibility of the Translation column"""
        self.table.setColumnHidden(2, not checked)
        
    def load_data_from_db(self):
        """Load data from database to table"""
        self.table.setRowCount(0)
        for word in self.db.arrayer:
            self.table.blockSignals(True)
            self.add_row_to_table(word)
            self.table.blockSignals(False)
        
    def entry_submit(self):
        """Handle submission of new word"""
        input_text = self.entry.text()
        
        if input_text:
            # Check if character already exists
            if self.db.char_exists(input_text):
                # Show notification for duplicate entry
                self.show_duplicate_notification(input_text)
                # Get the existing word
                word = self.db.get_word_by_char(input_text)
                # Find and select the existing row
                self.find_and_select_row(word.char)
            else:
                self.table.blockSignals(True)
                # Add the new word
                new_word = self.db.push_new_char(input_text)
                
                # Add new word to table
                row_position = self.add_row_to_table(new_word)

                # Select the newly added row
                self.table.selectRow(row_position)

                self.table.blockSignals(False)
                        
            # Clear input field
            self.entry.clear()
    
    def show_duplicate_notification(self, char_text):
        """Show a notification that the character already exists"""
        QMessageBox.information(
            self,
            "Duplicate Entry",
            f"The character '{char_text}' already exists in your collection."
        )
    
    def find_and_select_row(self, char_text):
        """Find and select the row containing the given character"""
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)  # Character is in column 0
            if item and item.text() == char_text:
                self.table.selectRow(row)
                self.table.scrollToItem(item)
                break
    
    def translation_save(self):
        print("Changing Translation of this Row Item...")
        return


    def database_save(self):
        """Save database changes"""
        self.db.update_db()
        QMessageBox.information(self, "Save Complete", "Your collection has been saved.")

    def add_row_to_table(self, word):
        """Create and insert a formatted row into the table for the given word."""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        char_item = QTableWidgetItem(word.char)
        pinyin_item = QTableWidgetItem(word.pinyin)
        translation_item = QTableWidgetItem(word.translation)

        char_item.setFlags(char_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # char not editable
        pinyin_item.setFlags(pinyin_item.flags() | Qt.ItemFlag.ItemIsEditable)
        translation_item.setFlags(translation_item.flags() | Qt.ItemFlag.ItemIsEditable)

        char_item.setFont(FONT)
        pinyin_item.setFont(FONT)
        translation_item.setFont(FONT)

        char_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        pinyin_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        translation_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        translation_item.setToolTip(word.translation)

        self.table.setItem(row_position, 0, char_item)
        self.table.setItem(row_position, 1, pinyin_item)
        self.table.setItem(row_position, 2, translation_item)

        return row_position
    
    def handle_item_changed(self, item):
        """Update the corresponding word in the DB when the table is edited."""
        row = item.row()
        column = item.column()
        new_value = item.text()

        # Get character to identify the word (column 0 is char)
        char_item = self.table.item(row, 0)
        if not char_item:
            return

        char = char_item.text()

        # Find the word in the DB
        word = self.db.get_word_by_char(char)
        if not word:
            return

        # Update the field based on column
        if column == 1:  # Pinyin
            word.pinyin = new_value
        elif column == 2:  # Translation
            word.translation = new_value
        
        self.table.resizeRowsToContents()

    def shuffle_table_rows(self):
        # Extract current data from the table
        data = []
        for row in range(self.table.rowCount()):
            char = self.table.item(row, 0).text()
            pinyin = self.table.item(row, 1).text()
            translation = self.table.item(row, 2).text()
            data.append((char, pinyin, translation))
        
        # Shuffle the data
        random.shuffle(data)
        
        # Temporarily block signals to avoid triggering itemChanged
        self.table.blockSignals(True)

        # Clear and repopulate the table
        self.table.setRowCount(0)
        for char, pinyin, translation in data:
            self.add_row_to_table(Word(char, pinyin, translation))
        
        self.table.blockSignals(False)


def main():
    app = QApplication(sys.argv)
    window = ChineseHelperApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()