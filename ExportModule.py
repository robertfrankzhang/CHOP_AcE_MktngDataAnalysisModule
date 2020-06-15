from Dataset import *
import numpy as np
import csv

class ExportModule:
    def __init__(self):
        self.d = Dataset()
        self.times = []
        for i in range(len(self.d.months)):
            self.times.append(self.d.monthNames[i][2:5] + " 20" + self.d.monthNames[i][5:])

    def cumulativeFreq(self, freq):
        a = []
        c = []
        for i in freq:
            a.append(i + sum(c))
            c.append(i)
        return np.array(a)

    def column(self, a, colIndex):
        l = []
        for row in a:
            l.append(row[colIndex])
        return l

    def exportElementsOverTimeGeneral(self,a,writer,title,cumulative,stacked=False):
        if cumulative and stacked:
            c = []
            b = []
            b.append(self.times)
            for i in range(len(a[0])):
                if i == 0:
                    c = self.cumulativeFreq(self.column(a[1], i))
                else:
                    c += self.cumulativeFreq(self.column(a[1], i))
                b.append(c.tolist())
        elif cumulative and not stacked:
            c = []
            b = []
            b.append(self.times)
            for i in range(len(a[0])):
                c = self.cumulativeFreq(self.column(a[1], i))
                b.append(c.tolist())
        elif not cumulative and stacked:
            c = []
            b = []
            b.append(self.times)
            for i in range(len(a[0])):
                if i == 0:
                    c = np.array(self.column(a[1], i))
                else:
                    c += np.array(self.column(a[1], i))
        else:
            b = []
            b.append(self.times)
            for i in range(len(a[0])):
                c = self.column(a[1],i)
                b.append(c)

        writer.writerow([title])
        headers = [""]
        for i in a[0]:
            headers.append(i)
        writer.writerow(headers)
        b = np.transpose(np.array(b))
        for row in b:
            writer.writerow(row.tolist())
        writer.writerow([])

    def exportAll(self,filename="Exports/exported.csv"):
        with open(filename,mode="w") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(["Cumulative Downloads Over Time"])
            writer.writerow(["","Downloads"])
            d = self.cumulativeFreq(self.d.totalDownloadsOverTime())
            for i in range(len(self.times)):
                writer.writerow([self.times[i],d[i]])
            writer.writerow([])

            writer.writerow(["Non Cumulative Downloads Over Time"])
            writer.writerow(["", "Downloads"])
            d = self.d.totalDownloadsOverTime()
            for i in range(len(self.times)):
                writer.writerow([self.times[i], d[i]])
            writer.writerow([])

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCountryOverTime(5),writer,"NonCumulative Downloads by Country Over Time",cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCountryOverTime(5),writer,"Cumulative Downloads by Country Over Time",cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCountryOverTime(5), writer,
                                               "Cumulative Downloads by Country Over Time (Stacked)", cumulative=True, stacked = True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCountryOverTime(5,normalized=True),writer,"NonCumulative Downloads by Country Over Time (%)",cumulative=False)


            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionOverTime(5), writer,
                                               "NonCumulative Downloads by Institution Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionOverTime(5), writer,
                                               "Cumulative Downloads by Institution Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionOverTime(5), writer,
                                               "Cumulative Downloads by Institution Over Time (Stacked)", cumulative=True, stacked = True)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(), writer,
                                               "NonCumulative Downloads by CHOP Affiliates Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(), writer,
                                               "Cumulative Downloads by CHOP Affiliates Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(), writer,
                                               "Cumulative Downloads by CHOP Affiliates Over Time (Stacked)", cumulative=True, stacked=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(normalized=True), writer,
                                               "Downloads by CHOP Affiliates Over Time (%)", cumulative=False)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(), writer,
                                               "NonCumulative Downloads by CHOP Affiliates (vs Education) Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(), writer,
                                               "Cumulative Downloads by CHOP Affiliates (vs Education) Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(), writer,
                                               "Cumulative Downloads by CHOP Affiliates (vs Education) Over Time (Stacked)",
                                               cumulative=True,stacked=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(normalized=True), writer,
                                               "Downloads by CHOP Affiliates (vs Education) Over Time (%)",
                                               cumulative=False)

            self.exportElementsOverTimeGeneral(self.d.institutionalAndNoninstutionalDownloadsOverTime(), writer,
                                               "NonCumulative Downloads (Inst vs NonInst) Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.institutionalAndNoninstutionalDownloadsOverTime(), writer,
                                               "Cumulative Downloads (Inst vs NonInst) Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.institutionalAndNoninstutionalDownloadsOverTime(), writer,
                                               "Cumulative Downloads (Inst vs NonInst) Over Time (Stacked)", cumulative=True, stacked=True)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionTypeOverTime(), writer,
                                               "NonCumulative Downloads by Institution Type Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionTypeOverTime(normalized=True), writer,
                                               "NonCumulative Downloads by Institution Type Over Time (%)",
                                               cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionTypeOverTime(), writer,
                                               "Cumulative Downloads by Institution Type Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionTypeOverTime(), writer,
                                               "Cumulative Downloads by Institution Type Over Time (Stacked)", cumulative=True, stacked = True)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByArticleOverTime(8), writer,
                                               "NonCumulative Downloads by Article Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByArticleOverTime(8), writer,
                                               "Cumulative Downloads by Article Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByArticleOverTime(8), writer,
                                               "Cumulative Downloads by Article Over Time (Stacked)", cumulative=True,stacked=True)

            self.exportElementsOverTimeGeneral(self.d.referralsOverTime(5), writer,
                                               "NonCumulative Downloads by Referral Source Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.referralsOverTime(5), writer,
                                               "Cumulative Downloads by Referral Source Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.referralsOverTime(5), writer,
                                               "Cumulative Downloads by Referral Source Over Time (Stacked)", cumulative=True, stacked=True)

            self.exportElementsOverTimeGeneral(self.d.sectionsDownloadedOverTime(),writer,"Sections downloaded over time",cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.sectionsDownloadedOverTime(normalized=True),writer,"Sections downloaded over time (normalized)",cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.sectionsDownloadedOverTime(balanced=True), writer,
                                               "Sections downloaded over time (balanced)", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.sectionsDownloadedOverTime(normalized=True,balanced=True), writer,
                                               "Sections downloaded over time (normalized & balanced)", cumulative=False)

            writer.writerow(["Most Downloaded Articles (Education)"])
            arts = self.d.mostDownloadedArticlesByInstitutionType("Education")
            for row in arts:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Most Downloaded Articles over the past 3 months (Education)"])
            arts = self.d.mostDownloadedArticlesByInstitutionType("Education",month_cutoff=3)
            for row in arts:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Most Downloaded Articles (Commercial)"])
            arts = self.d.mostDownloadedArticlesByInstitutionType("Commercial")
            for row in arts:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Most Downloaded Articles over the past 3 months (Commercial)"])
            arts = self.d.mostDownloadedArticlesByInstitutionType("Commercial", month_cutoff=3)
            for row in arts:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Most Downloaded Articles (NonInstitutional)"])
            arts = self.d.mostDownloadedArticlesNonInstitutional()
            for row in arts:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Most Downloaded Articles over the past 3 months (NonInstitutional)"])
            arts = self.d.mostDownloadedArticlesNonInstitutional(month_cutoff=3)
            for row in arts:
                writer.writerow(row)
            writer.writerow([""])

            #Most Downloaded Articles
            writer.writerow(["Top 50 Most Downloaded Articles"])
            articles = self.d.totalDownloadsByArticle(50)
            names = []
            vals = []
            for k, v in sorted(articles.items(), key=lambda item: item[1]):
                names.append(k)
                vals.append(v)
            names.reverse()
            vals.reverse()
            y_pos = np.arange(len(names))
            t = np.transpose(np.array([names,vals]))
            for row in t:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Top 50 Most Downloaded Articles over the past 3 months"])
            articles = self.d.totalDownloadsByArticle(50,month_cutoff=3)
            names = []
            vals = []
            for k, v in sorted(articles.items(), key=lambda item: item[1]):
                names.append(k)
                vals.append(v)
            names.reverse()
            vals.reverse()
            y_pos = np.arange(len(names))
            t = np.transpose(np.array([names, vals]))
            for row in t:
                writer.writerow(row)
            writer.writerow([""])

            writer.writerow(["Top 8 Most Downloaded Articles"])
            articles = self.d.totalDownloadsByArticle(8)
            names = []
            vals = []
            for k, v in sorted(articles.items(), key=lambda item: item[1]):
                names.append(k)
                vals.append(v)
            names.reverse()
            vals.reverse()
            y_pos = np.arange(len(names))
            t = np.transpose(np.array([names, vals]))
            for row in t:
                writer.writerow(row)



    def exportArticles(self,filename="Exports/articles.csv"):
        with open(filename, mode="w") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for article in self.d.articleNames():
                writer.writerow(["Title: "+article])

                a = self.d.getArticleTotalDownloads(article)
                writer.writerow(["Total Downloads:",a])
                writer.writerow([])

                b = self.d.getArticleDownloadsOverTime(article)
                writer.writerow(["Total Downloads Over Time"])
                writer.writerow(["","Downloads"])
                for i in range(len(self.times)):
                    writer.writerow([self.times[i], b[i]])
                writer.writerow([])

                c = self.d.getArticleTopCountries(article)
                writer.writerow(["Top Countries"])
                writer.writerow(["Country","Downloads"])
                for row in c:
                    writer.writerow(row)
                writer.writerow([])

                d = self.d.getArticleTopInstitutions(article)
                writer.writerow(["Top Institutions"])
                writer.writerow(["Institution", "Downloads"])
                for row in d:
                    writer.writerow(row)
                writer.writerow([])

                d = self.d.getArticleTopInstitutions(article,normalized=False)
                writer.writerow(["Top Institutions (Not %)"])
                writer.writerow(["Institution", "Downloads"])
                for row in d:
                    writer.writerow(row)
                writer.writerow([])

                e = self.d.getArticleTotalInstType(article)
                writer.writerow(["Institution Type Composition"])
                writer.writerow(["Institution Type","Downloads"])
                for type,count in e.items():
                    writer.writerow([type,count])
                writer.writerow([])

                f = self.d.getArticleInstTypeOverTime(article)
                self.exportElementsOverTimeGeneral(f,writer,"Institution Type Over Time",cumulative=False,stacked=False)

                g = self.d.getRelativeArticleTotalInstType(article)
                writer.writerow(["Institution Type Relative Composition"])
                writer.writerow(["Institution Type", "Relative Downloads"])
                for type,count in g.items():
                    writer.writerow([type,count])
                writer.writerow([])

                h = self.d.getRelativeArticleDownloadsOverTime(article)
                writer.writerow(["Total Relative Downloads Over Time"])
                writer.writerow(["", "Downloads"])
                for i in range(len(self.times)):
                    writer.writerow([self.times[i], h[i]])
                writer.writerow([])

                i = self.d.getMostRelatedArticles(article,'geo')
                writer.writerow(["Most Related Articles by Geography"])
                for country,value in i.items():
                    writer.writerow([country,value])
                writer.writerow([])

                j = self.d.getMostRelatedArticles(article, 'inst')
                writer.writerow(["Most Related Articles by Institution"])
                for inst, value in j.items():
                    writer.writerow([inst, value])
                writer.writerow([])

                writer.writerow(["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"])
                writer.writerow([])








