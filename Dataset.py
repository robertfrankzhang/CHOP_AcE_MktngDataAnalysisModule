
import pandas as pd
import numpy as np
import glob
from ArticleGraph import ArticleGraph

import copy

class Dataset:
    def __init__(self):
        #Get total downloads, where index 0 = first month downloads
        data = pd.read_csv("TotalDownloads.csv")
        self.totalDownloads = (np.transpose(data.drop("Date",axis=1).values)).tolist()[0]

        #Get month data
        self.months = {}

        self.monthNames = ["00Oct19","01Nov19","02Dec19","03Jan20","04Feb20","05Mar20","06Apr20"] ##Needs to be edited every month

        manualCategorization = pd.read_csv("ManualArticleCategorization.csv",encoding='ISO-8859–1').values
        self.manualArticleCategoryMap = {}
        self.articleCategories = []
        for article in manualCategorization:
            self.manualArticleCategoryMap[article[0]] = article[1]
            try:
                float(article[1])
            except:
                if not (article[1] in self.articleCategories):
                    self.articleCategories.append(article[1])


        for m in self.monthNames:
            self.months[m] = {}

        for name in self.monthNames:
            #Referral Data
            rCount = 0
            for file in glob.glob(name+"/Referrers*.csv"):
                r = pd.read_csv(file)
                self.months[name]["Referrals"] = r.values
                rCount += 1
            if rCount > 1 or rCount == 0:
                raise Exception("No referral file")

            #Article Data
            wCount = 0
            for file in glob.glob(name+"/Works*.csv"):
                w = pd.read_csv(file)
                self.months[name]["Works"] = w.values
                wCount += 1
            if wCount > 1 or wCount == 0:
                raise Exception("No works file")



            #Institutional Data
            self.months[name]["Inst"] = {}

            fiCount = 0
            for file in glob.glob(name+"/Institutions*.csv"):
                full0i = pd.read_csv(file).values
                self.months[name]["Inst"]["0FULL"] = full0i
                fiCount += 1
            if fiCount > 1 or fiCount == 0:
                raise Exception("No FULL0 institutions file")

            instCount = 0
            unsortedInst = glob.glob(name + "/Institution Details*.csv")
            sortedDict = {}
            for inst in unsortedInst:
                if len(inst) in sortedDict:
                    sortedDict[len(inst)].append(inst)
                else:
                    sortedDict[len(inst)] = [inst]

            s = []
            for key,value in sorted(sortedDict.items()):
                v = sorted(value)
                s.extend(v)

            for file in s:
                i = pd.read_csv(file)
                self.months[name]["Inst"][full0i[instCount,0]] = i.values
                instCount += 1
            # Geographical Data
            self.months[name]["Geo"] = {}

            fgCount = 0
            for file in glob.glob(name + "/Countries*.csv"):
                full0g = pd.read_csv(file).values
                self.months[name]["Geo"]["0FULL"] = full0g
                fgCount += 1
            if fgCount > 1 or fgCount == 0:
                raise Exception("No FULL0 countries file")

            geoCount = 0
            unsortedInst = glob.glob(name + "/Country Details*.csv")
            sortedDict = {}
            for inst in unsortedInst:
                if len(inst) in sortedDict:
                    sortedDict[len(inst)].append(inst)
                else:
                    sortedDict[len(inst)] = [inst]

            s = []
            for key, value in sorted(sortedDict.items()):
                v = sorted(value)
                s.extend(v)

            for file in s:
                g = pd.read_csv(file)
                self.months[name]["Geo"][full0g[geoCount,0]] = g.values
                geoCount += 1

        self.geoArticleGraph = self.createGeoArticleGraph()
        self.instArticleGraph = self.createInstArticleGraph()

    def createInstArticleGraph(self):
        graph = ArticleGraph(self.articleNames())

        for month, value in self.months.items():
            ref = self.months[month]["Inst"]["0FULL"]
            for institution in value["Inst"]:
                if institution != "0FULL":
                    for article in self.months[month]["Inst"][institution]:
                        for article2 in self.months[month]["Inst"][institution]:
                            if article[0] != article2[0]:
                                graph.addOutgoingEdgeFromTo(article[0], article2[0], min(article[1], article2[1]))

        return graph

    def createGeoArticleGraph(self):
        graph = ArticleGraph(self.articleNames())

        for month, value in self.months.items():
            ref = self.months[month]["Geo"]["0FULL"]
            for country in value["Geo"]:
                if country != "0FULL":
                    for article in self.months[month]["Geo"][country]:
                        for article2 in self.months[month]["Geo"][country]:
                            if article[0] != article2[0]:
                                graph.addOutgoingEdgeFromTo(article[0], article2[0], min(article[1], article2[1]))

        return graph

    def getMostRelatedArticles(self,articleName,tag):
        if tag == 'inst':
            return self.instArticleGraph.getRelatedArticles(articleName)
        if tag == 'geo':
            return self.geoArticleGraph.getRelatedArticles(articleName)

    def totalDownloadsOverTime(self):
        #Return list of downloads over time (not cumulative)
        return self.totalDownloads

    def totalDownloadsByCountryOverTime(self,cutoff=10,normalized=False):
        #Return (countryNames,2D list of by country downloads over time (not cumulative)) tuple. Cutoff is the # countries that are distinguished from "other"
        totals = {}

        for month,value in self.months.items():
            vals = value["Geo"]["0FULL"]
            for country in vals:
                if not np.isnan(country[1]):
                    if country[0] in totals:
                        totals[country[0]] += country[1]
                    else:
                        totals[country[0]] = country[1]

        ranked = []
        for key,value in sorted(totals.items(),key=lambda item:item[1]):
            ranked.append(key)

        ranked.reverse()

        ranked = ranked[:cutoff]
        ret = []
        for month,value in self.months.items():
            vals = value["Geo"]["0FULL"]
            l = []
            other = 0
            for r in ranked:
                for country in vals:
                    if country[0] == r:
                        l.append(country[1])
            for country in vals:
                if not (country[0] in ranked) and not np.isnan(country[1]):
                    other += country[1]
            l.append(other)

            if normalized:
                l = (np.array(l)/np.sum(np.array(l))).tolist()
            ret.append(l)
        ranked.append("Other")
        return (ranked,ret)

    def totalDownloadsByInstitutionOverTime(self,cutoff=10):
        #Return (InstitutionNames,2D list of by inst downloads over time (not cumulative)) tuple. Cutoff is the # inst that are distinguished from "other"
        totals = {}

        for month,value in self.months.items():
            vals = value["Inst"]["0FULL"]
            for inst in vals:
                if not np.isnan(inst[2]):
                    if inst[0] in totals:
                        totals[inst[0]] += inst[2]
                    else:
                        totals[inst[0]] = inst[2]

        ranked = []
        for key,value in sorted(totals.items(),key=lambda item:item[1]):
            ranked.append(key)

        ranked.reverse()

        ranked = ranked[:cutoff]
        ret = []
        for month,value in self.months.items():
            vals = value["Inst"]["0FULL"]
            l = []
            other = 0
            for r in ranked:
                didAppend = False
                for inst in vals:
                    if inst[0] == r:
                        l.append(inst[2])
                        didAppend = True
                if not didAppend:
                    l.append(0)
            for inst in vals:
                if not (inst[0] in ranked) and not np.isnan(inst[2]):
                    other += inst[2]
            l.append(other)
            ret.append(l)
        ranked.append("Other")
        return (ranked,ret)

    def totalDownloadsByCHOPAffiliatesOverTime(self,normalized=False): #Return 2D array of affiliate downloads vs all other downloads
        affiliates = ["The Children's Hospital of Philadelphia","Penn Medicine","University of Pennsylvania"]
        mValues = []
        counter = 0
        for month,value in self.months.items():
            vals = value['Inst']["0FULL"]
            totals = {}
            total = 0
            for inst in vals:
                if inst[0] in affiliates:
                    if inst[0] in totals and not np.isnan(inst[2]):
                        totals[inst[0]] += inst[2]
                        total += inst[2]
                    else:
                        totals[inst[0]] = inst[2]
                        total += inst[2]
            n = []
            for i in range(len(affiliates)+1):
                n.append(None)

            for k,v in totals.items():
                for i in range(len(affiliates)):
                    if k == affiliates[i]:
                        if normalized:
                            n[i] = v/self.totalDownloads[counter]
                        else:
                            n[i] = v
            if not normalized:
                n[len(n)-1] = self.totalDownloads[counter] - total
            else:
                n[len(n) - 1] = (self.totalDownloads[counter] - total)/self.totalDownloads[counter]
            counter+=1

            mValues.append(n)
        affiliates.append("Other")
        return (affiliates,mValues)

    def totalDownloadsByCHOPAffiliatesOverTimeEducation(self,normalized=False): #Return 2D array of affiliate downloads vs all other educational downloads
        affiliates = ["The Children's Hospital of Philadelphia","Penn Medicine","University of Pennsylvania"]
        mValues = []
        counter = 0
        for month,value in self.months.items():
            vals = value['Inst']["0FULL"]
            totals = {}
            total = 0
            totalEducational = 0
            for inst in vals:
                if inst[1] == "Education" and not np.isnan(inst[2]):
                    totalEducational += inst[2]
                if inst[0] in affiliates and not np.isnan(inst[2]):
                    if inst[0] in totals:
                        totals[inst[0]] += inst[2]
                        total += inst[2]
                    else:
                        totals[inst[0]] = inst[2]
                        total += inst[2]
            n = []
            for i in range(len(affiliates) + 1):
                n.append(None)

            for k, v in totals.items():
                for i in range(len(affiliates)):
                    if k == affiliates[i]:
                        if normalized:
                            n[i] = v/totalEducational
                        else:
                            n[i] = v
            if not normalized:
                n[len(n) - 1] = totalEducational - total
            else:
                n[len(n) - 1] = (totalEducational - total)/totalEducational
            counter+=1

            mValues.append(n)
        affiliates.append("Other")
        return (affiliates,mValues)

    def institutionalAndNoninstutionalDownloadsOverTime(self): #Return 2D array of institutional, noninstitutional, and total downloads
        mValues = []
        counter = 0
        for month,value in self.months.items():
            vals = value['Inst']["0FULL"]
            totalInst = 0
            for inst in vals:
                if not np.isnan(inst[2]):
                    totalInst += inst[2]
            total = self.totalDownloads[counter]
            nonInst = total - totalInst
            val = [totalInst,nonInst,total]
            mValues.append(val)
            counter += 1
        return (["Institutional","NonInstitutional","All"],mValues)

    def totalDownloadsByInstitutionTypeOverTime(self,normalized=False):
        #Return (InstitutionTypes unsorted,2D list of by insttype downloads over time (not cumulative)) tuple.
        types = []

        for month, value in self.months.items():
            vals = value["Inst"]["0FULL"]
            for inst in vals:
                if not (inst[1] in types):
                    types.append(inst[1])

        ret = []
        for month, value in self.months.items():
            vals = value["Inst"]["0FULL"]
            l = []
            for r in types:
                l.append(0)
            counter = 0
            for r in types:
                for inst in vals:
                    if inst[1] == r and not np.isnan(inst[2]):
                        l[counter] += inst[2]
                counter += 1

            if normalized:
                l = (np.array(l)/np.sum(np.array(l))).tolist()
            ret.append(l)
        return (types, ret)

    def totalDownloadsByArticleOverTime(self,cutoff=10):
        #Return (ArticleNames,2D list of by article downloads over time (not cumulative)) tuple. Cutoff is the # articles that are distinguished from "other"
        totals = {}

        for month, value in self.months.items():
            vals = value["Works"]
            for article in vals:
                if not np.isnan(article[1]):
                    if article[0] in totals:
                        totals[article[0]] += article[1]
                    else:
                        totals[article[0]] = article[1]

        ranked = []
        for key, value in sorted(totals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append(key)
        ranked.reverse()
        ranked = ranked[:cutoff]
        ret = []
        for month, value in self.months.items():
            vals = value["Works"]
            l = []
            other = 0
            for r in ranked:
                didAppend = False
                for work in vals:
                    if work[0] == r:
                        l.append(work[1])
                        didAppend = True
                if not didAppend:
                    l.append(0)
            for work in vals:
                if not (work[0] in ranked) and not(np.isnan(work[1])):
                    other += work[1]
            l.append(other)
            ret.append(l)
        ranked.append("Other")
        return (ranked, ret)

    def totalDownloadsByArticle(self,cutoff=10,month_cutoff=None):
        #Return dictionary of most downloaded articles. Cutoff is the # articles that are distinguished from "other"
        totals = {}

        copyMonths = copy.deepcopy(list(self.months.items()))
        if month_cutoff == None:
            useMonths = copyMonths
        else:
            useMonths = copyMonths[(len(copyMonths) - month_cutoff):]

        for month, value in useMonths:
            vals = value["Works"]
            for article in vals:
                if not np.isnan(article[1]):
                    if article[0] in totals:
                        totals[article[0]] += article[1]
                    else:
                        totals[article[0]] = article[1]

        ranked = []
        for key, value in sorted(totals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append(key)
        ranked.reverse()
        cutoff = min(len(ranked),cutoff)
        ranked = ranked[:cutoff]
        ret = {}
        ret["Other"] = 0

        for artName,value in totals.items():
            if artName in ranked:
                ret[artName] = value
            else:
                if not np.isnan(value):
                    ret["Other"] += value

        return ret

    def articlesWithLessThanNDownloads(self,N):
        # Return list of most articles with less than or equal to N downloads.
        totals = {}

        for month, value in self.months.items():
            vals = value["Works"]
            for article in vals:
                if not np.isnan(article[1]):
                    if article[0] in totals:
                        totals[article[0]] += article[1]
                    else:
                        totals[article[0]] = article[1]
        ranked = []
        for key, value in sorted(totals.items(), key=lambda item: item[1]):
            if np.isnan(value) or value <= N:
                ranked.append(key)

        return ranked

    def articlesWithNoDownloads(self):
        return self.articlesWithLessThanNDownloads(0)

    def referralsOverTime(self,cutoff=10):
        # Return (Origin,2D list of by referrals over time (not cumulative)) tuple. Cutoff is the # referrals that are distinguished from "other"
        totals = {}

        for month, value in self.months.items():
            vals = value["Referrals"]
            for article in vals:
                if not np.isnan(article[1]):
                    if article[0] in totals:
                        totals[article[0]] += article[1]
                    else:
                        totals[article[0]] = article[1]

        ranked = []
        for key, value in sorted(totals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append(key)
        ranked.reverse()
        ranked = ranked[:cutoff]
        ret = []
        for month, value in self.months.items():
            vals = value["Referrals"]
            l = []
            other = 0
            for r in ranked:
                didAppend = False
                for work in vals:
                    if work[0] == r:
                        l.append(work[1])
                        didAppend = True
                if not didAppend:
                    l.append(0)
            for work in vals:
                if not (work[0] in ranked) and not (np.isnan(work[1])):
                    other += work[1]
            l.append(other)
            ret.append(l)
        ranked.append("Other")
        return (ranked, ret)

    def mostDownloadedArticlesByInstitutionType(self,type,month_cutoff=None):
        #Returns 2D sorted list of articles and download frequency.
        #month_cutoff is the cutoff of how many months (including present) should be included in analysis
        types = []

        copyMonths = copy.deepcopy(list(self.months.items()))
        if month_cutoff == None:
            useMonths = copyMonths
        else:
            useMonths = copyMonths[(len(copyMonths)-month_cutoff):]

        for month, value in useMonths:
            vals = value["Inst"]["0FULL"]
            for inst in vals:
                if not (inst[1] in types):
                    types.append(inst[1])

        if type not in types:
            raise Exception("Provided type is invalid")

        totals = {}

        for month, value in useMonths:
            ref = self.months[month]["Inst"]["0FULL"]
            for institution in value["Inst"]:
                if institution != "0FULL":
                    ttype = None
                    for i in ref:
                        if i[0] == institution:
                            ttype = i[1]
                            break

                    if ttype == type:
                        for article in value["Inst"][institution]:
                            if not np.isnan(article[1]):
                                if article[0] in totals:
                                    totals[article[0]] += article[1]
                                else:
                                    totals[article[0]] = article[1]


        ranked = []
        for key, value in sorted(totals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append([key,value])
        ranked.reverse()

        return ranked

    def mostDownloadedArticlesNonInstitutional(self,month_cutoff = None):
        # Returns 2D sorted list of articles and download frequency
        types = []

        copyMonths = copy.deepcopy(list(self.months.items()))
        if month_cutoff == None:
            useMonths = copyMonths
        else:
            useMonths = copyMonths[(len(copyMonths) - month_cutoff):]

        for month, value in useMonths:
            vals = value["Inst"]["0FULL"]
            for inst in vals:
                if not (inst[1] in types):
                    types.append(inst[1])

        instTotals = {}
        totals = {}

        for month, value in useMonths:
            for institution in value["Inst"]:
                if institution != "0FULL":
                    for article in value["Inst"][institution]:
                        if not np.isnan(article[1]):
                            if article[0] in instTotals:
                                instTotals[article[0]] += article[1]
                            else:
                                instTotals[article[0]] = article[1]

            for article in value['Works']:
                if not np.isnan(article[1]):
                    if article[0] in totals:
                        totals[article[0]] += article[1]
                    else:
                        totals[article[0]] = article[1]

        realTotals = {}
        for key in totals.keys():
            if key in instTotals:
                realTotals[key] = totals[key] - instTotals[key]
            else:
                realTotals[key] = totals[key]

        ranked = []
        for key, value in sorted(realTotals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append([key, value])
        ranked.reverse()

        return ranked

    def sectionsDownloadedOverTime(self,balanced=False,normalized=False): #return tuple in std format of sections downloaded over time, w/ sections being manual categories via csv
        ret = []
        for month, value in self.months.items():
            vals = value["Works"]
            l = []
            n = []
            for i in range(len(self.articleCategories)):
                l.append(0)
                n.append(0)

            if balanced:
                for key,value in self.manualArticleCategoryMap.items():
                    for i in range(len(self.articleCategories)):
                        if value == self.articleCategories[i]:
                            n[i] += 1

            for categoryIndex in range(len(self.articleCategories)):
                for work in vals:
                    if work[0][0:8] == "Draft - ": #Remove draft articles
                        pass
                    elif not work[0] in self.manualArticleCategoryMap:
                        k = self.getSimilarStringKey(work[0],self.manualArticleCategoryMap)
                        if not k == None:
                            if self.manualArticleCategoryMap[k] == self.articleCategories[categoryIndex] and not np.isnan(work[1]):
                                l[categoryIndex] += work[1]
                        else:
                            print("key "+str(work[0])+"not manually categorized")
                            pass
                    elif self.manualArticleCategoryMap[work[0]] == self.articleCategories[categoryIndex] and not np.isnan(work[1]):
                        l[categoryIndex] += work[1]

            if balanced:
                newL = []
                for categoryIndex in range(len(self.articleCategories)):
                    if l[categoryIndex] == 0 and n[categoryIndex] == 0:
                        newL.append(0)
                    else:
                        newL.append(l[categoryIndex]/n[categoryIndex])
                l = newL
            if normalized:
                l = (np.array(l)/np.sum(np.array(l))).tolist()
            ret.append(l)
        return (self.articleCategories, ret)

    def getSimilarStringKey(self,tryKey,dictionary,threshold=0.95):
        nKey2 = self.stripPunctation(tryKey)
        for key,value in dictionary.items():
            cCounter = 0
            counter = 0
            if isinstance(key,str) and len(key) > 0:
                nKey = self.stripPunctation(key)
                for cIndex in range(min(len(nKey),len(nKey2))):
                    if nKey[cIndex] == nKey2[cIndex]:
                        cCounter += 1
                    counter += 1
                if cCounter/counter >= threshold:
                    return key
        return None

    def stripPunctation(self,string): #Assumes param is string
        newS = ""
        for i in string:
            if i in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                newS+=i
        return newS

    ##################################################################################################
    def getArticleTotalDownloads(self,articleName):
        total = 0
        for month, value in self.months.items():
            for article in value["Works"]:
                if article[0] == articleName and not np.isnan(article[1]):
                    total += article[1]
        return total

    def getArticleDownloadsOverTime(self,articleName):
        totals = []
        for month, value in self.months.items():
            monthTotal = 0
            for article in value["Works"]:
                if article[0] == articleName and not np.isnan(article[1]):
                    monthTotal += article[1]
            totals.append(monthTotal)
        return totals

    def getRelativeArticleDownloadsOverTime(self,articleName):
        artOverTime = self.getArticleDownloadsOverTime(articleName)
        totalOverTime = self.totalDownloadsOverTime()
        ret = []
        for i in range(len(artOverTime)):
            ret.append(artOverTime[i]/totalOverTime[i])
        return ret

    def getArticleTopCountries(self,articleName,normalized=True):
        countryTotals = {}
        for month, value in self.months.items():
            for country in value["Geo"]:
                if country != "0FULL":
                    for article in value["Geo"][country]:
                        if article[0] == articleName and not np.isnan(article[1]):
                            if country in countryTotals:
                                countryTotals[country] += article[1]
                            else:
                                countryTotals[country] = article[1]

        ranked = []
        total = 0
        for key, value in sorted(countryTotals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append([key, value])
                total += value
        ranked.reverse()

        if normalized and total != 0:
            for i in range(len(ranked)):
                ranked[i][1]/=total

        return ranked

    def getArticleTopInstitutions(self,articleName,normalized=True):
        instTotals = {}
        for month, value in self.months.items():
            for inst in value["Inst"]:
                if inst != "0FULL":
                    for article in value["Inst"][inst]:
                        if article[0] == articleName and not np.isnan(article[1]):
                            if inst in instTotals:
                                instTotals[inst] += article[1]
                            else:
                                instTotals[inst] = article[1]

        ranked = []
        total = 0
        for key, value in sorted(instTotals.items(), key=lambda item: item[1]):
            if not np.isnan(value):
                ranked.append([key, value])
                total += value
        ranked.reverse()

        if normalized and total != 0:
            for i in range(len(ranked)):
                ranked[i][1]/=total

        return ranked

    def getArticleTotalInstType(self,articleName,normalized=True):
        typesCount  = {}
        for month, value in self.months.items():
            for inst in value['Inst']:
                if inst != "0FULL":
                    for article in value['Inst'][inst]:
                        if article[0] == articleName and not np.isnan(article[1]):
                            #Find inst type
                            for i in value['Inst']['0FULL']:
                                if i[0] == inst:
                                    if i[1] in typesCount:
                                        typesCount[i[1]]+=article[1]
                                    else:
                                        typesCount[i[1]] = article[1]
                                    break
                            break
        s = 0
        for type,count in typesCount.items():
            s += count
        totalD = self.getArticleTotalDownloads(articleName)

        allTypes = ['Education', 'Government', 'Organization', 'Commercial', 'Military', 'Library']
        typesCount2 = {}
        for t in allTypes:
            if not t in typesCount:
                typesCount2[t] = 0
            else:
                typesCount2[t] = typesCount[t]

        typesCount2["NonInstitutional"] = totalD-s
        if normalized and totalD != 0:
            for key in typesCount2.keys():
                typesCount2[key] /= totalD

        return typesCount2

    def getRelativeArticleTotalInstType(self,articleName):
        typesDict = self.getArticleTotalInstType(articleName)
        totals = self.totalDownloadsByInstitutionTypeOverTime()
        totalDict = {}
        for i in range(len(totals[0])):
            totalDict[totals[0][i]] = sum(totals[1][i])/sum(self.totalDownloads)

        retDict = {}
        for type in totals[0]:
            retDict[type] = typesDict[type]-totalDict[type]

        allTypes = ['Education', 'Government', 'Organization', 'Commercial', 'Military', 'Library']
        ret2Dict = {}
        for type in allTypes:
            ret2Dict[type] = retDict[type]

        return ret2Dict

    def getArticleInstTypeOverTime(self,articleName,normalized=True):

        allTypes = ['Education','Government','Organization','Commercial','Military','Library']

        typesCount = []
        types = []
        for month, value in self.months.items():
            monthTypesCount = {}
            for inst in value['Inst']:
                if inst != "0FULL":
                    for article in value['Inst'][inst]:
                        if article[0] == articleName and not np.isnan(article[1]):
                            #Find inst type
                            for i in value['Inst']['0FULL']:
                                if i[0] == inst:
                                    if i[1] in monthTypesCount:
                                        monthTypesCount[i[1]]+=article[1]
                                    else:
                                        monthTypesCount[i[1]] = article[1]
                                    if not i[1] in types:
                                        types.append(i[1])
                                    break
                            break
            typesCount.append(monthTypesCount)
        ret2 = []
        totalDs = self.getArticleDownloadsOverTime(articleName)
        o = []
        c = 0
        for month in range(len(typesCount)):
            monthRet = []
            for type in allTypes:
                if type in types:
                    if type in typesCount[month]:
                        monthRet.append(typesCount[month][type])
                    else:
                        monthRet.append(0)
                else:
                    monthRet.append(0)
            o.append(sum(monthRet))
            monthRet.append(totalDs[c]-sum(monthRet))
            if normalized and sum(monthRet) != 0:
                monthRet = (np.array(monthRet)/sum(monthRet)).tolist()
            ret2.append(monthRet)
            c += 1
        allTypes.append("NonInstitutional")

        return (allTypes,ret2)



    def articleNames(self):
        articles = []
        for month,value in self.months.items():
            for article in value["Works"]:
                if not article[0] in articles:
                    articles.append(article[0])
        return articles

