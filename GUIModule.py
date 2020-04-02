
import matplotlib.pyplot as plt
import numpy as np
from Dataset import *

#A constantly evolving GUI Module updated based on analytical capabilities
class GUIModule:
    def __init__(self):
        self.d = Dataset()
        self.startMonth = self.d.monthNames[0][2:5]+" 20"+self.d.monthNames[0][5:]
        self.endMonth = self.d.monthNames[len(self.d.monthNames)-1][2:5]+" 20"+self.d.monthNames[len(self.d.monthNames)-1][5:]

        self.times = []
        for i in range(len(self.d.months)):
            self.times.append(i)

    def cumulativeFreq(self,freq):
        a = []
        c = []
        for i in freq:
            a.append(i + sum(c))
            c.append(i)
        return np.array(a)

    def column(self,a, colIndex):
        l = []
        for row in a:
            l.append(row[colIndex])
        return l

    def plotCumulativeDownloadsOverTime(self):
        plt.plot(self.times, self.cumulativeFreq(self.d.totalDownloadsOverTime()))
        plt.ylabel('Cumulative Downloads')
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.show()

    def plotNoncumulativeDownloadsOverTime(self):
        plt.plot(self.times, self.d.totalDownloadsOverTime())
        plt.ylabel('NonCumulative Downloads')
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.show()

    def plotDownloadsByCountryOverTime(self,cutoff=10):
        countries = self.d.totalDownloadsByCountryOverTime(cutoff)
        c = []
        for i in range(len(countries[0])):
            if i == 0:
                c = self.cumulativeFreq(self.column(countries[1], i))
            else:
                c += self.cumulativeFreq(self.column(countries[1], i))
            plt.plot(self.times, c, label=countries[0][i])
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.legend()
        plt.show()

    def plotDownloadsByInstitutionOverTime(self,cutoff=10):
        institutions = self.d.totalDownloadsByInstitutionOverTime(cutoff)
        c = []
        for i in range(len(institutions[0])):
            if i == 0:
                c = self.cumulativeFreq(self.column(institutions[1], i))
            else:
                c += self.cumulativeFreq(self.column(institutions[1], i))
            plt.plot(self.times, c, label=institutions[0][i])
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.legend()
        plt.show()

    def plotDownloadsByInstitutionTypeOverTime(self):
        institutions = self.d.totalDownloadsByInstitutionTypeOverTime()
        c = []
        for i in range(len(institutions[0])):
            if i == 0:
                c = self.cumulativeFreq(self.column(institutions[1], i))
            else:
                c += self.cumulativeFreq(self.column(institutions[1], i))
            plt.plot(self.times, c, label=institutions[0][i])
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.legend()
        plt.show()

    def plotDownloadsByArticleOverTime(self,cutoff=10):
        articles = self.d.totalDownloadsByArticleOverTime(cutoff)

        c = []
        for i in range(len(articles[0])):
            if i == 0:
                c = self.cumulativeFreq(self.column(articles[1], i))
            else:
                c += self.cumulativeFreq(self.column(articles[1], i))
            plt.plot(self.times, c, label=articles[0][i])
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.legend()
        plt.show()

    def plotMostDownloadedArticles(self,cutoff=10):
        articles = self.d.totalDownloadsByArticle(cutoff)
        names = []
        vals = []
        for k, v in sorted(articles.items(), key=lambda item: item[1]):
            names.append(k)
            vals.append(v)
        names.reverse()
        y_pos = np.arange(len(names))
        plt.bar(y_pos, vals, align='center', alpha=0.5)
        plt.ylabel("Downloads")
        plt.show()

    def printMostDownloadedArticles(self,cutoff=10):
        articles = self.d.totalDownloadsByArticle(cutoff)
        names = []
        for k, v in sorted(articles.items(), key=lambda item: item[1]):
            names.append(k)
        names.reverse()
        for n in names:
            print(n)

    def printArticlesWithLessThanNDownloads(self,N):
        articles = self.d.articlesWithLessThanNDownloads(30)
        for a in articles:
            print(a)

    def printArticlesWithNoDownloads(self):
        articles = self.d.articlesWithNoDownloads()
        for a in articles:
            print(a)

    def plotDownloadsByReferralSourceOverTime(self,cutoff=10):
        sources = self.d.referralsOverTime()

        c = []
        for i in range(len(sources[0])):
            if i == 0:
                c = self.cumulativeFreq(self.column(sources[1], i))
            else:
                c += self.cumulativeFreq(self.column(sources[1], i))
            plt.plot(self.times, c, label=sources[0][i])
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.legend()
        plt.show()

    def printMostDownloadedArticlesByInstitutionType(self,type):
        education = self.d.mostDownloadedArticlesByInstitutionType(type)
        names = self.column(education, 0)
        vals = self.column(education, 1)
        y_pos = np.arange(len(names))
        plt.bar(y_pos, vals, align='center', alpha=0.5)
        plt.ylabel("Downloads ("+type+")")
        plt.show()

        for n in names:
            print(n)



