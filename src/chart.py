from matplotlib import pyplot as plt
from matplotlib import style

class ChartPrompt:

    def showChart(self, xVals, yVals, chartTitle, xLabel, yLabel, xLabels):

        style.use('ggplot')

        x = xVals
        y = yVals

        fig, ax = plt.subplots()

        ax.bar(x, y, align='center')

        ax.set_title(chartTitle)
        ax.set_ylabel(yLabel)
        ax.set_xlabel(xLabel)

        ax.set_xticks(x)
        ax.set_xticklabels(xLabels)

        plt.ion()
        plt.show()