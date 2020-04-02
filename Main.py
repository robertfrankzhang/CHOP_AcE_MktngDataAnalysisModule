from Dataset import *

d = Dataset()

print(d.totalDownloadsOverTime())
print(d.totalDownloadsByCountryOverTime())
print(d.totalDownloadsByInstitutionOverTime())
print(d.totalDownloadsByInstitutionTypeOverTime())
print(d.totalDownloadsByArticleOverTime())
print(d.totalDownloadsByArticle())
print(d.articlesWithLessThanNDownloads(10))
print(d.articlesWithNoDownloads())
print(d.referralsOverTime())
print()
print(d.mostDownloadedArticlesByInstitutionType("Government"))
print(d.mostDownloadedArticlesByInstitutionType("Education"))
print(d.mostDownloadedArticlesByInstitutionType("Organization"))
print(d.mostDownloadedArticlesByInstitutionType("Commercial"))
print(d.mostDownloadedArticlesByInstitutionType("Military"))
print(d.mostDownloadedArticlesByInstitutionType("Library"))