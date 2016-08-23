from wifi import Cell, Scheme

Cell.all('wlan0')
cell = Cell.all('wlan0')[0]
scheme = Scheme.for_cell('wlan0', 'home', cell, passkey)
scheme.save()
scheme.activate()
scheme = Scheme.find('wlan0', 'home')
scheme.activate()
