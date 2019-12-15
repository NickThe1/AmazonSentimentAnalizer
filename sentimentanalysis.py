from matplotlib.figure import Figure
from textblob import TextBlob
import matplotlib.pyplot as plt

import pandas as pd
import review_parser as rp


class Analizer():
    url = ""
    fullpage = True
    data = None

    def __init__(self, url, full=True):
        self.url = url
        self.fullpage =  full

    def make_data(self,):
        rp.parse(rp.url_formatter(self.url))
        self.data = pd.DataFrame(rp.dater)

    def polarity(self,):
        data = self.data
        pol = lambda x: TextBlob(x).sentiment.polarity
        sub = lambda x: TextBlob(x).sentiment.subjectivity

        data['polarity'] = data[4].apply(pol)
        data['subjectivity'] = data[4].apply(sub)

    def get_figure(self, alf, title="Sentiment Analysis", xlabel="<-- Negative -------- Positive -->",
                    ylabel ='<-- Facts -------- Opinions -->', legeng=True):
        fig = Figure()
        fn = fig.add_subplot(111)
        fn.scatter(self.data['polarity'], self.data['subjectivity'], c='b', alpha=alf)
        fn.set_title(title, size=20, color='indigo')
        fn.set_xlabel(xlabel)
        fn.set_ylabel(ylabel)
        if legeng:
            fn.legend(loc='best', frameon=True)
        return fig

    def show_plot(self, alf, title="Sentiment Analysis", xlabel="<-- Negative -------- Positive -->",
                    ylabel ='<-- Facts -------- Opinions -->'):

        plt.scatter(self.data['polarity'], self.data['subjectivity'], c='b', alpha=alf)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

if __name__ == '__main__':
    anl = Analizer(URL)
    anl.make_data()
    anl.polarity()
    anl.show_plot()
