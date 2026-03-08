from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QComboBox, QPushButton, QMessageBox
)
from languages import LANGUAGE_MAP
from translator import TranslatorService
from speech import SpeechService


class TranslatorWindow(QMainWindow):
    MAX_INPUT_CHARS = 2000

    def __init__(self):
        super().__init__()

        self.speech = SpeechService()
        self.translator = TranslatorService()

        self.setWindowTitle("Language Translation Tool")
        self.resize(700, 500)

        central = QWidget()
        self.setCentralWidget(central)
        self.main_layout = QVBoxLayout(central)
        self.build_ui()
        self.statusBar().showMessage("Ready")
    
    def build_ui(self):
        # Input section.
        self.input_label = QLabel("Input Text")
        self.input_text = QTextEdit()

        # Language selectors.
        self.source_combo = QComboBox()
        self.target_combo = QComboBox()
        language_names = list(LANGUAGE_MAP.keys())
        self.source_combo.addItems(language_names)
        self.target_combo.addItems(language_names)

        self.translate_btn = QPushButton("Translate")
        
        # Output section.
        self.output_label = QLabel("Translated Text")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.copy_btn = QPushButton("Copy")
        self.speak_btn = QPushButton("Speak")

        self.source_label = QLabel("Source Language")
        self.target_label = QLabel("Target Language")

        source_col = QVBoxLayout()
        source_col.addWidget(self.source_label)
        source_col.addWidget(self.source_combo)

        target_col = QVBoxLayout()
        target_col.addWidget(self.target_label)
        target_col.addWidget(self.target_combo)

        lang_row = QHBoxLayout()
        lang_row.addLayout(source_col)
        lang_row.addLayout(target_col)
        lang_row.addWidget(self.translate_btn)

        action_row = QHBoxLayout()
        action_row.addWidget(self.copy_btn)
        action_row.addWidget(self.speak_btn)

        self.main_layout.addWidget(self.input_label)
        self.main_layout.addWidget(self.input_text)
        self.main_layout.addLayout(lang_row)
        self.main_layout.addWidget(self.output_label)
        self.main_layout.addWidget(self.output_text)
        self.main_layout.addLayout(action_row)

        # Defaults and initial state.
        self.input_text.setPlaceholderText("Type text to translate...")
        self.output_text.setPlaceholderText("Translation appears here...")
        self.source_combo.setCurrentText("English")
        self.target_combo.setCurrentText("Arabic")

        self.copy_btn.setEnabled(False)
        self.speak_btn.setEnabled(False)
        self.connect_signals()

    def connect_signals(self):
        self.translate_btn.clicked.connect(self.on_translate_clicked)
        self.copy_btn.clicked.connect(self.on_copy_clicked)
        self.speak_btn.clicked.connect(self.on_speak_clicked)

    def on_translate_clicked(self):
        input_text = self.input_text.toPlainText()
        source_name = self.source_combo.currentText()
        target_name = self.target_combo.currentText()

        # Basic input guard to avoid oversized API requests.
        if len(input_text.strip()) > self.MAX_INPUT_CHARS:
            QMessageBox.warning(
                self,
                "Translation Error",
                f"Input is too long. Please limit text to {self.MAX_INPUT_CHARS} characters.",
            )
            return

        self.set_busy(True)
        try:
            translated_text = self.translator.translate(input_text, source_name, target_name)
            self.output_text.setPlainText(translated_text)
            has_output = bool(translated_text.strip())
            self.copy_btn.setEnabled(has_output)
            self.speak_btn.setEnabled(has_output)
            self.statusBar().showMessage("Translation completed.", 3000)
        except ValueError as error:
            QMessageBox.warning(self, "Translation Error", str(error))
            self.output_text.clear()
            self.copy_btn.setEnabled(False)
            self.speak_btn.setEnabled(False)
            self.statusBar().showMessage("Translation failed.", 3000)
        finally:
            self.set_busy(False)

    def on_copy_clicked(self):
        translated_text = self.output_text.toPlainText().strip()
        if not translated_text:
            QMessageBox.warning(self, "Copy", "There is no translated text to copy.")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(translated_text)
        QMessageBox.information(self, "Copy", "Translated text copied to clipboard.")
        self.statusBar().showMessage("Copied to clipboard.", 2500)

    def on_speak_clicked(self):
        translated_text = self.output_text.toPlainText().strip()
        if not translated_text:
            QMessageBox.warning(self, "Speak", "There is no translated text to speak.")
            return

        target_name = self.target_combo.currentText()
        target_code = LANGUAGE_MAP.get(target_name, "en")

        try:
            self.speech.speak(translated_text, target_code)
            self.statusBar().showMessage("Speech played.", 2500)
        except ValueError as error:
            QMessageBox.warning(self, "Speak", str(error))
            self.statusBar().showMessage("Speech failed.", 3000)
        except Exception as error:
            QMessageBox.warning(self, "Speak", f"Speech failed: {error}")
            self.statusBar().showMessage("Speech failed.", 3000)
    
    def set_busy(self, busy: bool):
        self.translate_btn.setEnabled(not busy)
        self.source_combo.setEnabled(not busy)
        self.target_combo.setEnabled(not busy)
        if busy:
            self.statusBar().showMessage("Translating...")
