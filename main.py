import sys
from PyQt6.QtWidgets import QApplication
from ui import TranslatorWindow


def main() -> int:
	# Application bootstrap.
	app = QApplication(sys.argv)
	window = TranslatorWindow()
	window.show()
	return app.exec()


if __name__ == "__main__":
	sys.exit(main())