from PyQt4 import QtGui


class Backend:

    def __init__(self):

        self.window = None
        self.stk_struc = []
        self.opt_struc = []
        self.calc_struc = []
        self.intval = 0.0
        self.extval = 0.0

    def redraw_table(self):
        self.update_table()
        self.calc_stock()
        self.calc_opt()
        self.calc_vals()
        self.upload_data()

    def calc_stock(self):
        bskt = self.window.ivlbl
        calcbskt = []
        for item in self.window.ihlbl:
            begeq = item*self.window.stke
            endeq = [x * item for x in bskt]
            stkpnl = [x - begeq for x in endeq]
            calcbskt.append(stkpnl)
        finbskt = calcbskt
        self.stk_struc = finbskt
        self.calc_struc = finbskt

    def calc_opt(self):
        cost = -1*(self.window.optpnl*self.window.optqty)
        nlist = []

        for item in self.window.vlbl:
            if self.window.put:
                if float(item) < self.window.strike:
                    int_val = self.window.strike - float(item)
                    val_at_exp = self.window.optqty*100*int_val
                    real_gain = val_at_exp + cost
                    nlist.append(real_gain)
                else:
                    nlist.append(cost)

            elif not self.window.put:
                if float(item) > self.window.strike:
                    int_val = float(item) - self.window.strike
                    val_at_exp = self.window.optqty*100*int_val
                    real_gain = val_at_exp + cost
                    nlist.append(real_gain)
                else:
                    nlist.append(cost)

        if self.window.longopt:
            self.opt_struc = nlist
        else:
            self.opt_struc = nlist*-1
        self.opt_struc = nlist

    def calc_vals(self):
        # eventually this function will combine opt_struc and stk_struc to make calc_struc
        # cHedge.calc_struc=cHedge.stk_struc
        new_struc = []
        for column in self.stk_struc:
            newcol = [x + y for x, y in zip(self.opt_struc, column)]
            new_struc.append(newcol)

        self.calc_struc = new_struc

    def upload_data(self):
        c = 0
        for col in self.calc_struc:
            o = 0
            for item in col:
                nitem = QtGui.QTableWidgetItem()
                item = "{0:.2f}".format(item)
                nitem.setText(str(item))
                self.window.tableWidget.setItem(o, c, nitem)
                o = o + 1
            c = c + 1

    def clear_table(self):
        self.window.tableWidget.setRowCount(0)
        self.window.tableWidget.setColumnCount(0)

    def pull_data(self):
        try:
            self.window.trows = float(self.window.lineedit_pricelevels.text())
            self.window.tcols = float(self.window.lineedit_hedgelevels.text())
            self.window.vincre = float(self.window.lineedit_priceincrement.text())
            self.window.hincre = float(self.window.lineedit_hedgeincrement.text())
        except:
            print("Table Update Failed")

        try:
            self.window.start_hedge = int(self.window.lineedit_hedgestart.text())
        except:
            print("Start Hedge Update Failed")

        try:
            self.window.sprice = float(self.window.lineedit_strike.text())
        except:
            print("Strike price to Current price linking failed")

        try:
            self.window.strike = float(self.window.lineedit_strike.text())
        except:
            print("Strike failed to update")

        try:
            self.window.optpnl = float(self.window.lineedit_optprice.text())*100
        except:
            print("Option price update failed")

        try:
            self.window.optqty = float(self.window.lineedit_optquan.text())
            if self.window.optqty < 0:
                self.window.longopt = False
            elif self.window.optqty > 0:
                self.window.longopt = True
        except:
            print("Option qty update failed")

        try:
            self.window.stke = float(self.window.lineedit_stockentry.text())
        except:
            print("Stock info Update Failed")

        if self.window.radio_putcall.isChecked():
            self.window.put = True
        else:
            self.window.put = False

    def up_vlbl(self):
        self.window.vlbl = []
        self.window.ivlbl = []
        self.window.mlbl = [0]
        nlbl = []
        a = self.window.trows
        numlvl = a
        nlbl.append(float(self.window.sprice))
        while numlvl > 0:

            llvl = float(self.window.sprice+self.window.vincre*numlvl)
            hlvl = float(self.window.sprice-self.window.vincre*numlvl)

            m_llvl = float(0+self.window.vincre*numlvl)
            m_hlvl = float(0-self.window.vincre*numlvl)
            self.window.mlbl.append(m_llvl)
            self.window.mlbl.append(m_hlvl)
            self.window.mlbl.sort()

            if llvl > 0:
                nlbl.append(llvl)
            if hlvl > 0:
                nlbl.append(hlvl)
            numlvl = numlvl - 1

        nlbl = sorted(nlbl)
        for item in nlbl:
            a = "{0:.2f}".format(item)
            thing = str(a)
            ithing = float(item)
            self.window.ivlbl.append(ithing)
            self.window.vlbl.append(thing)

    def up_hlbl(self):
        self.window.hlbl = []
        self.window.ihlbl = []

        new_labels = []
        ca = self.window.tcols
        while ca > 0:

            start = self.window.start_hedge
            llvl = int((start + (ca*self.window.hincre)))
            hlvl = int((start - (ca*self.window.hincre)))

            new_labels.append(llvl)
            new_labels.append(hlvl)
            ca = ca - 1

        new_labels.append(int(self.window.start_hedge))

        shlabels = new_labels
        shlabels.sort()

        self.window.ihlbl = shlabels
        for x in self.window.ihlbl:
            c = '{0} shares'.format(x)
            self.window.hlbl.append(c)

    def up_headers(self):
        self.window.tableWidget.setRowCount(len(self.window.vlbl))
        self.window.tableWidget.setVerticalHeaderLabels(self.window.vlbl)
        self.window.tableWidget.setColumnCount(len(self.window.hlbl))
        self.window.tableWidget.setHorizontalHeaderLabels(self.window.hlbl)

    def update_table(self):
        self.clear_table()
        self.pull_data()
        self.up_vlbl()
        self.up_hlbl()
        self.up_headers()

class Window(QtGui.QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.tableWidget = None
        self.hlbl = []
        self.ihlbl = []
        self.tcols = 0
        self.vlbl = []
        self.ivlbl = []
        self.trows = 0

        self.strike = 0.0
        self.sprice = 0.0
        self.optpnl = 0
        self.optqty = 0
        self.stke = 0.0
        self.put = True
        self.long = True
        self.longopt = True
        self.start_hedge = 0

        # 'Options/Stock Settings' Qwidget's
        self.lineedit_optquan = None
        self.lineedit_optprice = None
        self.lineedit_strike = None
        self.radio_putcall = None
        self.lineedit_stockentry = None

        # 'Table Settings' Qwidget's
        self.lineedit_priceincrement = None
        self.lineedit_hedgeincrement = None
        self.lineedit_pricelevels = None
        self.lineedit_hedgelevels = None
        self.lineedit_hedgestart = None

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
        groupbox = QtGui.QGroupBox("Option/Stock Settings")

        # vertical box to hold widgets
        ope = QtGui.QVBoxLayout()

        # horizontal boxes to hold widgets
        opqt = QtGui.QHBoxLayout()
        oqla = QtGui.QLabel("Option Qty (+/-):", self)
        self.lineedit_optquan = QtGui.QLineEdit(self)
        self.lineedit_optquan.setText("0")
        opqt.addWidget(oqla)
        opqt.addWidget(self.lineedit_optquan)
        opqt.addStretch(1)
        self.lineedit_optquan.editingFinished.connect(lambda: self.refresh_table())

        pnl = QtGui.QHBoxLayout()
        opla = QtGui.QLabel("Option Price:", self)
        self.lineedit_optprice = QtGui.QLineEdit(self)
        self.lineedit_optprice.setText(".05")
        pnl.addWidget(opla)
        pnl.addWidget(self.lineedit_optprice)
        pnl.addStretch(1)
        self.lineedit_optprice.editingFinished.connect(lambda: self.refresh_table())

        sstrk = QtGui.QHBoxLayout()
        ssla = QtGui.QLabel("Strike Price:", self)
        self.lineedit_strike = QtGui.QLineEdit(self)
        self.lineedit_strike.setText("5")
        sstrk.addWidget(ssla)
        sstrk.addWidget(self.lineedit_strike)
        sstrk.addStretch(1)
        self.lineedit_strike.editingFinished.connect(lambda: self.refresh_table())

        # radio buttons to select put/call
        lsopt = QtGui.QHBoxLayout()
        self.radio_putcall = QtGui.QRadioButton("Put")
        radio2 = QtGui.QRadioButton("Call")
        self.radio_putcall.setChecked(True)
        lsopt.addWidget(self.radio_putcall)
        lsopt.addWidget(radio2)
        lsopt.addStretch(1)
        self.radio_putcall.clicked.connect(lambda: self.refresh_table())
        radio2.clicked.connect(lambda: self.refresh_table())

        stkent = QtGui.QHBoxLayout()
        sel = QtGui.QLabel("Stock Entry:", self)
        self.lineedit_stockentry = QtGui.QLineEdit(self)
        self.lineedit_stockentry.setText("2")
        stkent.addWidget(sel)
        stkent.addWidget(self.lineedit_stockentry)
        self.lineedit_stockentry.editingFinished.connect(lambda: self.refresh_table())

        # add horizontal boxes to vertical box
        ope.addLayout(opqt)
        ope.addLayout(pnl)
        ope.addLayout(sstrk)
        ope.addLayout(lsopt)
        ope.addLayout(stkent)
        # add vertical container to 'option' groupbox
        groupbox.setLayout(ope)

        return groupbox

    def draw_table_settings(self):

        groupbox = QtGui.QGroupBox("Table Settings")

        # vertical box to hold widgets
        vbox = QtGui.QVBoxLayout()

        plvl = QtGui.QHBoxLayout()
        uirl = QtGui.QLabel("Price Levels:", self)
        self.lineedit_pricelevels = QtGui.QLineEdit(self)
        self.lineedit_pricelevels.setText("3")
        plvl.addWidget(uirl)
        plvl.addWidget(self.lineedit_pricelevels)
        plvl.addStretch(1)
        self.lineedit_pricelevels.editingFinished.connect(lambda: self.refresh_table())

        pinc = QtGui.QHBoxLayout()
        incl = QtGui.QLabel("Price Increment:", self)
        self.lineedit_priceincrement = QtGui.QLineEdit(self)
        self.lineedit_priceincrement.setText('1')
        pinc.addWidget(incl)
        pinc.addWidget(self.lineedit_priceincrement)
        pinc.addStretch(1)
        self.lineedit_priceincrement.editingFinished.connect(lambda: self.refresh_table())

        hlvl = QtGui.QHBoxLayout()
        uicl = QtGui.QLabel("Hedge Levels:", self)
        self.lineedit_hedgelevels = QtGui.QLineEdit(self)
        self.lineedit_hedgelevels.setText("2")
        hlvl.addWidget(uicl)
        hlvl.addWidget(self.lineedit_hedgelevels)
        hlvl.addStretch(1)
        self.lineedit_hedgelevels.editingFinished.connect(lambda: self.refresh_table())

        hinc = QtGui.QHBoxLayout()
        sincl = QtGui.QLabel("Hedge Increment:", self)
        self.lineedit_hedgeincrement = QtGui.QLineEdit(self)
        self.lineedit_hedgeincrement.setText('100')
        hinc.addWidget(sincl)
        hinc.addWidget(self.lineedit_hedgeincrement)
        hinc.addStretch(1)
        self.lineedit_hedgeincrement.editingFinished.connect(lambda: self.refresh_table())

        strk = QtGui.QHBoxLayout()
        sla = QtGui.QLabel("Hedge Start (+/-):", self)
        self.lineedit_hedgestart = QtGui.QLineEdit(self)
        self.lineedit_hedgestart.setText("0")
        self.lineedit_hedgestart.editingFinished.connect(lambda: self.refresh_table())
        strk.addWidget(sla)
        strk.addWidget(self.lineedit_hedgestart)
        strk.addStretch(1)

        vbox.addLayout(plvl)
        vbox.addLayout(pinc)
        vbox.addLayout(hlvl)
        vbox.addLayout(hinc)
        vbox.addLayout(strk)
        groupbox.setLayout(vbox)
        return groupbox

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
