# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from aqt.qt import *
from operator import itemgetter
from anki.hooks import addHook, remHook, runHook
from aqt.utils import isMac, shortcut
import aqt

class ModelChooser(QHBoxLayout):

    def __init__(self, mw, widget, label=True, name = ""):
        QHBoxLayout.__init__(self)
        self.widget = widget
        self.mw = mw
        self.col = mw.col
        self.label = label
        self.setMargin(0)
        self.setSpacing(8)
        self.setupModels()
        self.name = name
        addHook('reset' + name, self.onReset)
        self.widget.setLayout(self)

    def setupModels(self):
        if self.label:
            self.modelLabel = QLabel(_("Type"))
            self.addWidget(self.modelLabel)
        # models box
        self.button = QPushButton()
        #self.button.setStyleSheet("* { text-align: left; }")
        self.button.setToolTip(shortcut(_("Change Note Type (Ctrl+N)")))
        s = QShortcut(QKeySequence(_("Ctrl+N")), self.widget)
        s.connect(s, SIGNAL("activated()"), self.onModelChange)
        self.addWidget(self.button)
        self.connect(self.button, SIGNAL("clicked()"), self.onModelChange)
        # layout
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy(7),
            QSizePolicy.Policy(0))
        self.button.setSizePolicy(sizePolicy)
        self.updateButtonText()

    def cleanup(self):
        remHook('reset' + self.name, self.onReset)

    def onReset(self):
        self.updateButtonText()

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def onEdit(self):
        import aqt.models
        aqt.models.Models(self.mw, self.widget)

    def onModelChange(self):
        from aqt.studydeck import StudyDeck
        current = self.col.models.current()['name']
        # edit button
        edit = QPushButton(_("Manage"))
        self.connect(edit, SIGNAL("clicked()"), self.onEdit)
        def nameFunc():
            return sorted(self.col.models.allNames())
        ret = StudyDeck(
            self.mw, names=nameFunc,
            accept=_("Choose"), title=_("Choose Note Type"),
            help="_notes", current=current, parent=self.widget,
            buttons=[edit], cancel=False)
        if not ret.name:
            return

        self.updateCollection(ret.name)


    def updateCollection(self, new_model_name = None):
        really_changed = new_model_name
        if not really_changed:
            # only update collection with current name
            new_model_name = str(self.button.text())

        m = self.col.models.byName(new_model_name)
        if not m:
            return
        self.col.conf['curModel'] = m['id']
        cdeck = self.col.decks.current()
        cdeck['mid'] = m['id']
        self.col.decks.save(cdeck)
        self.updateButtonText()

        if really_changed:
            runHook("currentModelChanged" + self.name)
#        self.mw.reset()

    def updateButtonText(self):
        self.button.setText(self.col.models.current()['name'])
