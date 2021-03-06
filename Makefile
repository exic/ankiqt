PREFIX=/usr

all:
	@echo "You can run Anki with ./anki"
	@echo "If you wish to install it system wide, type 'sudo make install'"
	@echo "Uninstall with 'sudo make uninstall'"

install:
	@test ! -d .git || (echo "Install from git is not supported. Please use a tarball."; false)
	rm -rf ${DESTDIR}${PREFIX}/share/anki
	mkdir -p ${DESTDIR}${PREFIX}/share/anki
	cp -av * ${DESTDIR}${PREFIX}/share/anki/
	cd ${DESTDIR}${PREFIX}/share/anki && (\
	mv anki ${DESTDIR}${PREFIX}/local/bin/;\
	mv anki.xpm anki.png ${DESTDIR}${PREFIX}/share/pixmaps/;\
	mv anki.desktop ${DESTDIR}${PREFIX}/share/applications;\
	mv anki.1 ${DESTDIR}${PREFIX}/share/man/man1/)
	xdg-mime install anki.xml
	xdg-mime default anki.desktop application/x-anki
	xdg-mime default anki.desktop application/x-apkg
	@echo
	@echo "Install complete."

uninstall:
	rm -rf ${DESTDIR}${PREFIX}/share/anki
	rm -rf ${DESTDIR}${PREFIX}/local/bin/anki
	rm -rf ${DESTDIR}${PREFIX}/share/pixmaps/anki.{xpm,png}
	rm -rf ${DESTDIR}${PREFIX}/share/applications/anki.desktop
	rm -rf ${DESTDIR}${PREFIX}/share/man/man1/anki.1
	-xdg-mime uninstall ${DESTDIR}${PREFIX}/share/mime/packages/anki.xml
	@echo
	@echo "Uninstall complete."
