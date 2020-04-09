from ExportModule import *
from Dataset import *

d = Dataset()
d.articlesWithLessThanNDownloads(10)
e = ExportModule()
e.exportAll()