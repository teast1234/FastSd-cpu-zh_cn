from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSlider,
    QToolButton,
    QFileDialog,
    QApplication,
)


from PyQt5.QtCore import Qt, QEvent

from PIL import Image
from constants import DEVICE
from app_settings import AppSettings
from urllib.parse import urlparse, unquote
from frontend.gui.base_widget import BaseWidget
from backend.models.lcmdiffusion_setting import DiffusionTask
from frontend.i18n import tr


class Img2ImgWidget(BaseWidget):
    def __init__(self, config: AppSettings, parent):
        super().__init__(config, parent)

        # Create init image selection widgets
        self.img_label = QLabel(tr("img2img.init_image"))
        self.img_path = QLineEdit()
        self.img_path.setReadOnly(True)
        self.img_path.setAcceptDrops(True)
        self.img_path.installEventFilter(self)
        self.img_browse = QToolButton()
        self.img_browse.setText("...")
        self.img_browse.setToolTip(tr("img2img.browse_tooltip"))
        self.img_browse.clicked.connect(self.browse_click)
        # Create the init image selection layout
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.img_label)
        hlayout.addWidget(self.img_path)
        hlayout.addWidget(self.img_browse)

        self.strength_label = QLabel(tr("img2img.strength", value=0.3))
        self.strength = QSlider(orientation=Qt.Orientation.Horizontal)
        self.strength.setMaximum(10)
        self.strength.setMinimum(1)
        self.strength.setValue(3)
        self.strength.valueChanged.connect(self.update_strength_label)
        # self.layout().insertWidget(1, self.strength_label)
        # self.layout().insertWidget(2, self.strength)
        self.layout().addLayout(hlayout)
        self.layout().addWidget(self.strength_label)
        self.layout().addWidget(self.strength)

    def browse_click(self):
        filename = self.show_file_selection_dialog()
        if filename[0] != "":
            self.img_path.setText(filename[0])

    def show_file_selection_dialog(self) -> str:
        filename = QFileDialog.getOpenFileName(
            self, tr("img2img.open_image"), "results", tr("img2img.image_filter")
        )
        return filename

    def eventFilter(self, source, event: QEvent):
        """This is the Drag and Drop event filter for the init image QLineEdit"""
        if event.type() == QEvent.DragEnter:
            if event.mimeData().hasFormat("text/plain"):
                event.acceptProposedAction()
            return True
        elif event.type() == QEvent.Drop:
            event.acceptProposedAction()
            path = unquote(urlparse(event.mimeData().text()).path)
            self.img_path.setText(path)
            return True

        return False

    def before_generation(self):
        super().before_generation()
        self.img_browse.setEnabled(False)
        self.img_path.setEnabled(False)

    def after_generation(self):
        super().after_generation()
        self.img_browse.setEnabled(True)
        self.img_path.setEnabled(True)

    def generate_image(self):
        self.parent.prepare_generation_settings(self.config)
        self.config.settings.lcm_diffusion_setting.diffusion_task = (
            DiffusionTask.image_to_image.value
        )
        self.config.settings.lcm_diffusion_setting.prompt = self.prompt.toPlainText()
        self.config.settings.lcm_diffusion_setting.negative_prompt = (
            self.neg_prompt.toPlainText()
        )
        self.config.settings.lcm_diffusion_setting.init_image = Image.open(
            self.img_path.text()
        )
        self.config.settings.lcm_diffusion_setting.strength = self.strength.value() / 10

        images = self.parent.context.generate_text_to_image(
            self.config.settings,
            self.config.reshape_required,
            DEVICE,
        )
        self.parent.context.save_images(images, self.config.settings)
        self.prepare_images(images)
        self.after_generation()

    def update_strength_label(self, value):
        val = round(int(value) / 10, 1)
        self.strength_label.setText(tr("img2img.strength", value=val))
        self.config.settings.lcm_diffusion_setting.strength = val
