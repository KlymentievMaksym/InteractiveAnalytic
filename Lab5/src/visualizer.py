import plotly.express as px
# import matplotlib.pyplot as plt

from io import BytesIO

class Visualizer:
    def __init__(self, st):
        self.st = st

    def show_chart(self, dataframe):
        fig = px.bar(dataframe, x="status", y="size", title="Розподіл скачаного за кодами")
        fig.update_layout(xaxis=dict(type="category"))
        self.st.plotly_chart(fig)
        return fig

    def save_chart(self, fig, filename="chart.png"):
        buf = BytesIO()
        fig.write_image(buf, format="png")
        buf.seek(0)

        self.st.download_button(
            label="⬇️ Download chart as PNG",
            data=buf,
            file_name=filename,
            mime="image/png"
        )
