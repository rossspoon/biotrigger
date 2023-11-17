import pylink

el = pylink.EyeLink("100.1.1.1")
el.receiveDataFile("WEBTEST.EDF", './results/pilot_test.edf')

