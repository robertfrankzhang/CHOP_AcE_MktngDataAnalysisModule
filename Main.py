from ExportModule import *
from Dataset import *
from GUIModule import *

# d = Dataset()
# print(d.getArticleTotalDownloads("Orphan Drugs: Understanding the FDA Approval Process"))
# print(d.getArticleDownloadsOverTime("Orphan Drugs: Understanding the FDA Approval Process"))
# print(d.getArticleTopCountries("Orphan Drugs: Understanding the FDA Approval Process"))
# print(d.getArticleTopInstitutions("Orphan Drugs: Understanding the FDA Approval Process"))
# print(d.getArticleTotalInstType("Orphan Drugs: Understanding the FDA Approval Process"))
# print(d.getArticleInstTypeOverTime("Orphan Drugs: Understanding the FDA Approval Process"))
#
# print(d.getArticleTotalDownloads("Nonprofit and Foundation Sponsored Research: Developing New Models of Collaboration for Research and Development"))
# print(d.getArticleDownloadsOverTime("Nonprofit and Foundation Sponsored Research: Developing New Models of Collaboration for Research and Development"))
# print(d.getArticleTopCountries("Nonprofit and Foundation Sponsored Research: Developing New Models of Collaboration for Research and Development",normalized=False))
# print(d.getArticleTopInstitutions("Nonprofit and Foundation Sponsored Research: Developing New Models of Collaboration for Research and Development",normalized=False))
# print(d.getArticleTotalInstType("Nonprofit and Foundation Sponsored Research: Developing New Models of Collaboration for Research and Development",normalized=False))
# print(d.getArticleInstTypeOverTime("Nonprofit and Foundation Sponsored Research: Developing New Models of Collaboration for Research and Development",normalized=False))
#

e = ExportModule()
e.exportAll()
