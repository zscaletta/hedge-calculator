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
            self.window.trows = float(self.window.uirows.text())
            self.window.tcols = float(self.window.uicols.text())
            self.window.vincre = float(self.window.ince.text())
            self.window.hincre = float(self.window.since.text())
        except:
            print("Table Update Failed")

        try:
            self.window.start_hedge = int(self.window.sle.text())
        except:
            print("Start Hedge Update Failed")

        try:
            self.window.sprice = float(self.window.ssle.text())
        except:
            print("Strike price to Current price linking failed")

        try:
            self.window.strike = float(self.window.ssle.text())
        except:
            print("Strike failed to update")

        try:
            self.window.optpnl = float(self.window.ople.text())*100
        except:
            print("Option price update failed")

        try:
            self.window.optqty = float(self.window.oqle.text())
            if self.window.optqty < 0:
                self.window.longopt = False
            elif self.window.optqty > 0:
                self.window.longopt = True
        except:
            print("Option qty update failed")

        try:
            self.window.stke = float(self.window.sele.text())
        except:
            print("Stock info Update Failed")

        if self.window.radio1.isChecked():
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
