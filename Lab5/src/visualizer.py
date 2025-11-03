import plotly.express as px
import matplotlib.pyplot as plt

class Visualizer:
    @staticmethod
    def show_chart(df):
        # plt.bar(df)
        # fig = plt.figure()
        fig = px.bar(df, x="code", y="total_size", title="Розподіл скачаного за кодами")
        return fig

    @staticmethod
    def save_chart(fig, filename="chart.png"):
        fig.write_image(filename)
