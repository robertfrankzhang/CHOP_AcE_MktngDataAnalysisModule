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

    def exportElementsOverTimeGeneral(self,a,writer,title,cumulative):
        if cumulative:
            c = []
            b = []
            b.append(self.times)
            for i in range(len(a[0])):
                if i == 0:
                    c = self.cumulativeFreq(self.column(a[1], i))
                else:
                    c += self.cumulativeFreq(self.column(a[1], i))
                b.append(c.tolist())

            writer.writerow([title])
            headers = [""]
            for i in a[0]:
                headers.append(i)
            writer.writerow(headers)
            b = np.transpose(np.array(b))
            for row in b:
                writer.writerow(row.tolist())
        else:
            b = []
            b.append(self.times)
            for i in range(len(a[0])):
                c = self.cumulativeFreq(self.column(a[1], i))
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

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionOverTime(5), writer,
                                               "NonCumulative Downloads by Institution Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionOverTime(5), writer,
                                               "Cumulative Downloads by Institution Over Time", cumulative=True)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(), writer,
                                               "NonCumulative Downloads by CHOP Affiliates Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(), writer,
                                               "Cumulative Downloads by CHOP Affiliates Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTime(normalized=True), writer,
                                               "Downloads by CHOP Affiliates Over Time (%)", cumulative=False)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(), writer,
                                               "NonCumulative Downloads by CHOP Affiliates (vs Education) Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(), writer,
                                               "Cumulative Downloads by CHOP Affiliates (vs Education) Over Time", cumulative=True)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByCHOPAffiliatesOverTimeEducation(normalized=True), writer,
                                               "Downloads by CHOP Affiliates (vs Education) Over Time (%)",
                                               cumulative=False)

            self.exportElementsOverTimeGeneral(self.d.institutionalAndNoninstutionalDownloadsOverTime(), writer,
                                               "NonCumulative Downloads (Inst vs NonInst) Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.institutionalAndNoninstutionalDownloadsOverTime(), writer,
                                               "Cumulative Downloads (Inst vs NonInst) Over Time", cumulative=True)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionTypeOverTime(), writer,
                                               "NonCumulative Downloads by Institution Type Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByInstitutionTypeOverTime(), writer,
                                               "Cumulative Downloads by Institution Type Over Time", cumulative=True)

            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByArticleOverTime(5), writer,
                                               "NonCumulative Downloads by Article Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.totalDownloadsByArticleOverTime(5), writer,
                                               "Cumulative Downloads by Article Over Time", cumulative=True)

            self.exportElementsOverTimeGeneral(self.d.referralsOverTime(5), writer,
                                               "NonCumulative Downloads by Referral Source Over Time", cumulative=False)
            self.exportElementsOverTimeGeneral(self.d.referralsOverTime(5), writer,
                                               "Cumulative Downloads by Referral Source Over Time", cumulative=True)

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





