
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

    def plotElementsOverTimeGeneral(self,a,cumulative):
        if cumulative:
            c = []
            for i in range(len(a[0])):
                if i == 0:
                    c = self.cumulativeFreq(self.column(a[1], i))
                else:
                    c += self.cumulativeFreq(self.column(a[1], i))
                plt.plot(self.times, c, label=a[0][i])
        else:
            c = []
            for i in range(len(a[0])):
                c = self.column(a[1], i)
                plt.plot(self.times, c, label=a[0][i])
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.legend()
        plt.show()

    def plotDownloadsOverTime(self,cumulative=False):
        if cumulative:
            plt.plot(self.times, self.cumulativeFreq(self.d.totalDownloadsOverTime()))
            plt.ylabel('Cumulative Downloads')
        else:
            plt.plot(self.times, self.d.totalDownloadsOverTime())
            plt.ylabel('NonCumulative Downloads')
        plt.xlabel('Months '+self.startMonth+' - '+self.endMonth)
        plt.show()

    def plotDownloadsByCountryOverTime(self,cutoff=10,cumulative=False):
        countries = self.d.totalDownloadsByCountryOverTime(cutoff)
        self.plotElementsOverTimeGeneral(countries,cumulative)

    def plotDownloadsByInstitutionOverTime(self,cutoff=10,cumulative=False):
        institutions = self.d.totalDownloadsByInstitutionOverTime(cutoff)
        self.plotElementsOverTimeGeneral(institutions,cumulative)

    def plotDownloadsByAffiliatesOverTime(self,normalized=False,cumulative=False):
        institutions = self.d.totalDownloadsByCHOPAffiliatesOverTime(normalized)
        self.plotElementsOverTimeGeneral(institutions,cumulative)

    def plotDownloadsByAffiliatesOverTimeEducational(self,normalized=False,cumulative=False):
        institutions = self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(normalized)
        self.plotElementsOverTimeGeneral(institutions,cumulative)

    def plotInstNonInstDownloadsOverTime(self,cumulative=False):
        institutions = self.d.institutionalAndNoninstutionalDownloadsOverTime()
        self.plotElementsOverTimeGeneral(institutions,cumulative)

    def plotDownloadsByInstitutionTypeOverTime(self,cumulative=False):
        institutions = self.d.totalDownloadsByInstitutionTypeOverTime()
        self.plotElementsOverTimeGeneral(institutions,cumulative)

    def plotDownloadsByArticleOverTime(self,cutoff=10,cumulative=False):
        articles = self.d.totalDownloadsByArticleOverTime(cutoff)
        self.plotElementsOverTimeGeneral(articles,cumulative)

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

    def plotDownloadsByReferralSourceOverTime(self,cutoff=10,cumulative=False):
        sources = self.d.referralsOverTime()
        self.plotElementsOverTimeGeneral(sources,cumulative)

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



