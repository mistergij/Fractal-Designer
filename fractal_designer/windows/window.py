from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap

from fractal_designer.actions import Actions


class Window:
    def __init__(self, actions: Actions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_ = actions

    def disable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setDisabled(True)

    def enable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setEnabled(True)

    def mathTex_to_QPixmap(self, mathTex: str, fs: int) -> QPixmap:
        """
        Converts mathTex to a QPixmap
        :param mathTex:
        :param fs:
        :return:
        Author: https://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget
        """
        # Set up matplotlib figure instance
        fig = Figure()
        fig.patch.set_facecolor("none")
        fig.set_canvas(FigureCanvasAgg(fig))
        renderer = fig.canvas.get_renderer()

        # Plot mathTex expression
        ax = fig.add_axes((0, 0, 1, 1))
        ax.axis("off")
        ax.patch.set_facecolor("none")
        t = ax.text(0, 0, mathTex, ha="left", va="bottom", fontsize=fs)

        # Fit figure size to text artist

        fwidth, fheight = fig.get_size_inches()
        fig_bbox = fig.get_window_extent(renderer)

        text_bbox = t.get_window_extent(renderer)

        tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
        tight_fheight = text_bbox.height * fheight / fig_bbox.height

        fig.set_size_inches(tight_fwidth, tight_fheight)

        # Convert matplotlib figure to QPixmap

        buf, size = fig.canvas.print_to_buffer()
        q_image = QImage.rgbSwapped(QImage(buf, size[0], size[1], QImage.Format.Format_ARGB32))

        q_pixmap = QPixmap(q_image)

        return q_pixmap
