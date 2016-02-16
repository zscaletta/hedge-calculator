from PyQt4 import QtGui
from backend import Backend

class Window(QtGui.QWidget):


    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.hlbl = []
        self.ihlbl = []
        self.tcols = 0
        self.vlbl = []
        self.trows = 0

        self.strike = 0.0
        self.sprice = 0.0
        self.optpnl = 0
        self.optqty = 0
        self.stke= 0.0
        self.put = True
        self.long = True
        self.longopt = True
        self.start_hedge = 0

        self.hc_backend = Backend()
        self.hc_backend.window = self
        grid = QtGui.QGridLayout()
        grid.setColumnStretch(1, 2)
        self.setLayout(grid)
        grid.addWidget(self.draw_opt_settings(), 0, 0)
        grid.addWidget(self.draw_table_settings(), 1, 0)
        grid.addWidget(self.draw_table(self.trows, self.tcols), 0, 1, 3, 2)

        self.hc_backend.redraw_table()
        self.setWindowTitle("HedgeCalc")
        self.resize(850, 500)

    def refresh_table(self):
        self.hc_backend.redraw_table()

    def draw_opt_settings(self):

        # create 'option settings' group box
        groupBox = QtGui.QGroupBox("Option/Stock Settings")

        # vertical box to hold widgets
        ope = QtGui.QVBoxLayout()

        # horizontal boxes to hold widgets
        opqt = QtGui.QHBoxLayout()
        oqla = QtGui.QLabel("Option Qty (+/-):", self)
        self.oqle = QtGui.QLineEdit(self)
        self.oqle.setText("0")
        opqt.addWidget(oqla)
        opqt.addWidget(self.oqle)
        opqt.addStretch(1)
        self.oqle.editingFinished.connect(lambda: self.refresh_table())

        pnl = QtGui.QHBoxLayout()
        opla = QtGui.QLabel("Option Price:", self)
        self.ople = QtGui.QLineEdit(self)
        self.ople.setText(".05")
        pnl.addWidget(opla)
        pnl.addWidget(self.ople)
        pnl.addStretch(1)
        self.ople.editingFinished.connect(lambda: self.refresh_table())

        sstrk = QtGui.QHBoxLayout()
        ssla = QtGui.QLabel("Strike Price:", self)
        self.ssle = QtGui.QLineEdit(self)
        self.ssle.setText("5")
        sstrk.addWidget(ssla)
        sstrk.addWidget(self.ssle)
        sstrk.addStretch(1)
        self.ssle.editingFinished.connect(lambda: self.refresh_table())

        # radio buttons to select put/call
        lsopt = QtGui.QHBoxLayout()
        self.radio1 = QtGui.QRadioButton("Put")
        radio2 = QtGui.QRadioButton("Call")
        self.radio1.setChecked(True)
        lsopt.addWidget(self.radio1)
        lsopt.addWidget(radio2)
        lsopt.addStretch(1)
        self.radio1.clicked.connect(lambda: self.refresh_table())
        radio2.clicked.connect(lambda: self.refresh_table())

        stkent = QtGui.QHBoxLayout()
        sel = QtGui.QLabel("Stock Entry:", self)
        self.sele = QtGui.QLineEdit(self)
        self.sele.setText("2")
        stkent.addWidget(sel)
        stkent.addWidget(self.sele)
        self.sele.editingFinished.connect(lambda: self.refresh_table())

        # add horizontal boxes to vertical box
        ope.addLayout(opqt)
        ope.addLayout(pnl)
        ope.addLayout(sstrk)
        ope.addLayout(lsopt)
        ope.addLayout(stkent)
        # add vertical container to 'option' groupbox
        groupBox.setLayout(ope)

        return groupBox

    def draw_table_settings(self):

        groupBox = QtGui.QGroupBox("Table Settings")

        # vertical box to hold widgets
        vbox = QtGui.QVBoxLayout()

        plvl = QtGui.QHBoxLayout()
        uirl = QtGui.QLabel("Price Levels:", self)
        self.uirows = QtGui.QLineEdit(self)
        self.uirows.setText("3")
        plvl.addWidget(uirl)
        plvl.addWidget(self.uirows)
        plvl.addStretch(1)
        self.uirows.editingFinished.connect(lambda: self.refresh_table())

        pinc = QtGui.QHBoxLayout()
        incl = QtGui.QLabel("Price Increment:", self)
        self.ince = QtGui.QLineEdit(self)
        self.ince.setText('1')
        pinc.addWidget(incl)
        pinc.addWidget(self.ince)
        pinc.addStretch(1)
        self.ince.editingFinished.connect(lambda: self.refresh_table())

        hlvl = QtGui.QHBoxLayout()
        uicl = QtGui.QLabel("Hedge Levels:", self)
        self.uicols = QtGui.QLineEdit(self)
        self.uicols.setText("2")
        hlvl.addWidget(uicl)
        hlvl.addWidget(self.uicols)
        hlvl.addStretch(1)
        self.uicols.editingFinished.connect(lambda: self.refresh_table())

        hinc = QtGui.QHBoxLayout()
        sincl = QtGui.QLabel("Hedge Increment:", self)
        self.since = QtGui.QLineEdit(self)
        self.since.setText('100')
        hinc.addWidget(sincl)
        hinc.addWidget(self.since)
        hinc.addStretch(1)
        self.since.editingFinished.connect(lambda: self.refresh_table())

        strk = QtGui.QHBoxLayout()
        sla = QtGui.QLabel("Hedge Start (+/-):", self)
        self.sle = QtGui.QLineEdit(self)
        self.sle.setText("0")
        self.sle.editingFinished.connect(lambda: self.refresh_table())
        strk.addWidget(sla)
        strk.addWidget(self.sle)
        strk.addStretch(1)

        vbox.addLayout(plvl)
        vbox.addLayout(pinc)
        vbox.addLayout(hlvl)
        vbox.addLayout(hinc)
        vbox.addLayout(strk)
        groupBox.setLayout(vbox)
        return groupBox

    def draw_table(self, rows, cols):

        self.tableWidget = QtGui.QTableWidget(rows, cols, self)
        self.tableWidget.resize(700, 400)
        self.tableWidget.move(75, 20)
        self.tableWidget.setHorizontalHeaderLabels(self.hlbl)
        self.tableWidget.setVerticalHeaderLabels(self.vlbl)

        return self.tableWidget

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
