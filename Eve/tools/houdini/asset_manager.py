import hou
import os
from PySide2 import QtCore, QtWidgets
from ui import ui_asset_manager

from core import settings
from core.database.entities import EveFile, Asset
from core.database import eve_data
from core.database import asset_data
from core.models import ListModel
from core import file_path


reload(file_path)


class AssetManager(QtWidgets.QDialog, ui_asset_manager.Ui_AssetManager):
    def __init__(self):
        super(AssetManager, self).__init__()
        self.setupUi(self)
        self.setParent(hou.ui.mainQtWindow(), QtCore.Qt.Window)

        # Setup environment
        self.eve_root = os.environ['EVE_ROOT']
        self.project_name = os.environ['EVE_PROJECT_NAME']
        self.SQL_FILE_PATH = settings.SQL_FILE_PATH.format(self.eve_root)

        # Get Project Manager data
        self.eve_data = None
        self.project = None
        self.model_assets = None
        # Get asset data
        self.asset_data = None

        self.init_asset_manager()

        # Setup UI functionality
        self.btnAssetCrete.clicked.connect(self.create_asset_scene)

    def init_asset_manager(self):

        self.eve_data = eve_data.EveData(self.SQL_FILE_PATH)
        self.project = self.eve_data.get_project_by_name(self.project_name)

        self.eve_data.get_project_assets(self.project)
        self.model_assets = ListModel(self.eve_data.project_assets)
        self.boxAssetName.setModel(self.model_assets)

    def create_asset_scene(self):

        # Get Asset Object
        index = self.boxAssetName.model().index(self.boxAssetName.currentIndex(), 0)
        asset_id = index.data(QtCore.Qt.UserRole + 1)
        self.asset_data = asset_data.AssetData(self.SQL_FILE_PATH, asset_id)

        # Create file path string
        file_path_asset = file_path.EveFilePath()
        file_type = EveFile.file_types['asset_hip']
        asset_type = self.asset_data.asset_type_dic['name']
        file_path_asset.build_path_asset_hip(file_type, asset_type, self.asset_data.asset.name, '001')
        scene_path = file_path_asset.version_control()


def run_asset_manager():
    asset_manager = AssetManager()
    asset_manager.show()

