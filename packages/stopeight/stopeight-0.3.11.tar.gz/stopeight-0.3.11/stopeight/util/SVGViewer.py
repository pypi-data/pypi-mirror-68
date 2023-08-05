def show(filename='parser.out.svg'):
    import sys

    sys.path.append('..\PyQt5\examples\painting\svgviewer')

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    import svgviewer

    window = svgviewer.MainWindow()
    window.openFile(filename)
    window.show()
    sys.exit(app.exec_())

