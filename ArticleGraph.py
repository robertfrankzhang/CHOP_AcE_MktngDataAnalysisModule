
class ArticleGraph:
    def __init__(self,articleNames):
        '''
        :param articleNames: list of article names
        '''
        self.vertices = {}
        for article in articleNames:
            self.vertices[article] = Vertex(article,articleNames)

    def getRelatedArticles(self,articleName):
        return self.vertices[articleName].getMostRelatedArticles()

    def addOutgoingEdgeFromTo(self,fromArticle,toArticle,weight):
        self.vertices[fromArticle].addOutgoingEdgeTo(toArticle,weight)


class Vertex:
    def __init__(self,articleName,articleNames):
        self.articleName = articleName
        self.outgoingEdges = {}
        for name in articleNames:
            if name != articleName:
                self.outgoingEdges[name] = 0

    def addOutgoingEdgeTo(self,articleName,addedWeight):
        if articleName == self.articleName:
            raise Exception("Can't add self directing edge")
        self.outgoingEdges[articleName] += addedWeight

    def getMostRelatedArticles(self):
        #Return reversed sorted dictionary by values
        return {k: v for k, v in reversed(sorted(self.outgoingEdges.items(), key=lambda item: item[1]))}