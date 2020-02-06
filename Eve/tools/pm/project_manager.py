import os
import sqlite3
import subprocess
import webbrowser
from PySide2 import QtCore, QtWidgets

# Import UI
from ui import ui_pm_warning
from ui import ui_pm_main
from ui import ui_project
from ui import ui_project_properties
from ui import ui_pm_add_project
from ui import ui_asset
from ui import ui_asset_properties
from ui import ui_pm_add_asset
from ui import ui_sequence
from ui import ui_sequence_properties
from ui import ui_pm_add_sequence
from ui import ui_shot
from ui import ui_shot_properties
from ui import ui_pm_add_shot

from core import database
from core import settings
from core.common import Model


def build_project_root(project_name):
    """Build project root folder string"""

    project_root = '{0}/{1}'.format(settings.PROJECTS, project_name)
    return project_root


def build_folder_structure():
    """
    Create list for project folder structure

    TODO: build assets, sequences and shots folders based on EVE data
    assets=None, shots=None

    :param assets: list of Asset objects, assets of current project
    :param shots:  list of Shot objects, shots of current project
    :return:
    """

    # PROJECT FOLDER STRUCTURE
    # Shots structure
    SHOTS = [
        ['010', [
            ['SHOT_010', []],
            ['SHOT_020', []]
        ]]
    ]
    # Assets structure
    ASSETS = [
        ['CHARACTERS', []],
        ['ENVIRONMENTS', []],
        ['PROPS', []]
    ]
    # Types structure
    TYPES = [
        ['ASSETS', ASSETS],
        ['SHOTS', SHOTS]
    ]
    # Formats structure
    FORMATS = [
        ['ABC', []],
        ['GEO', []],
        ['FBX', []]
    ]
    # Folders structure
    FOLDERS = [
        ['EDIT', [
            ['OUT', []],
            ['PROJECT', []]
        ]],
        ['PREP', [
            ['ART', []],
            ['SRC', []],
            ['PIPELINE', [
                ['genes', []]
            ]],
        ]],
        ['PROD', [
            ['2D', [
                ['COMP', SHOTS],
                ['RENDER', SHOTS]
            ]],
            ['3D', [
                ['lib', [
                    ['ANIMATION', []],
                    ['MATERIALS', ASSETS]  # Or TYPES ?
                ]],
                ['fx', TYPES],
                ['caches', TYPES],
                ['hda', [
                    ['ASSETS', ASSETS],
                    ['FX', TYPES],
                ]],
                ['render', SHOTS],
                ['scenes', [
                    ['ASSETS', ASSETS],
                    ['ANIMATION', SHOTS],
                    ['FX', TYPES],
                    ['LAYOUT', SHOTS],
                    ['LOOKDEV', TYPES],
                    ['RENDER', SHOTS]
                ]],
                ['textures', TYPES],
            ]],
        ]]
    ]

    return FOLDERS


class Warnings(QtWidgets.QDialog, ui_pm_warning.Ui_Warning):
    def __init__(self, name):
        # SETUP UI WINDOW
        super(Warnings, self).__init__()
        self.setupUi(self)

        message = 'Delete {}?'.format(name)
        self.labWarning.setText(message)


class ProjectUI(QtWidgets.QWidget, ui_project.Ui_Project):
    def __init__(self):
        super(ProjectUI, self).__init__()
        self.setupUi(self)
        self.linHoudini.setText(settings.default_build)


class AssetUI(QtWidgets.QWidget, ui_asset.Ui_Asset):
    def __init__(self):
        super(AssetUI, self).__init__()
        self.setupUi(self)


class SequenceUI(QtWidgets.QWidget, ui_sequence.Ui_Sequence):
    def __init__(self):
        super(SequenceUI, self).__init__()
        self.setupUi(self)


class ShotUI(QtWidgets.QWidget, ui_shot.Ui_Shot):
    def __init__(self):
        super(ShotUI, self).__init__()
        self.setupUi(self)


class ProjectProperties(QtWidgets.QWidget, ui_project_properties.Ui_ProjectProperties):
    def __init__(self):
        super(ProjectProperties, self).__init__()
        self.setupUi(self)
        self.project_ui = ProjectUI()
        self.layoutProject.addWidget(self.project_ui)


class AssetProperties(QtWidgets.QWidget, ui_asset_properties.Ui_AssetProperties):
    def __init__(self):
        super(AssetProperties, self).__init__()
        self.setupUi(self)
        self.asset_ui = AssetUI()
        self.layoutAsset.addWidget(self.asset_ui)


class SequenceProperties(QtWidgets.QWidget, ui_sequence_properties.Ui_SequenceProperties):
    def __init__(self):
        super(SequenceProperties, self).__init__()
        self.setupUi(self)
        self.sequence_ui = SequenceUI()
        self.layoutSequence.addWidget(self.sequence_ui)


class ShotProperties(QtWidgets.QWidget, ui_shot_properties.Ui_ShotProperties):
    def __init__(self):
        super(ShotProperties, self).__init__()
        self.setupUi(self)
        self.shot_ui = ShotUI()
        self.layoutShot.addWidget(self.shot_ui)


class AddProject(QtWidgets.QDialog, ui_pm_add_project.Ui_AddProject):
    """
    Add project entity Dialog.
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddProject, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.project_ui = ProjectUI()
        self.layoutProject.addWidget(self.project_ui)
        self.project_ui.linProjectLocation.setEnabled(False)

        self.project_ui.linProjectName.textChanged.connect(self.project_name_changed)
        # self.project_ui.btnPickMaya.clicked.connect(self.pick_maya)
        self.btnAddProject.clicked.connect(self.add_project)
        self.btnAddProject.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AppProject class is shown (AddProject.show())
        :param event:
        :return:
        """

        # Clean UI
        self.project_ui.linProjectName.clear()
        self.project_ui.txtDescription.clear()
        self.project_ui.linProjectName.clear()

    def project_name_changed(self):

        project_name = self.project_ui.linProjectName.text()
        project_root = build_project_root(project_name)
        self.project_ui.linProjectLocation.setText(project_root)

    def add_project(self):
        """
        Create asset entity in datatbase
        :return:
        """

        # Get project data from UI
        project_name = self.project_ui.linProjectName.text()
        houdini_build = self.project_ui.linHoudini.text()
        project_width = self.project_ui.linProjectWidth.text()
        project_height = self.project_ui.linProjectHeight.text()
        project_description = self.project_ui.txtDescription.toPlainText()

        # Call add_project in PM class
        self.parent.add_project(project_name, houdini_build, project_width, project_height, project_description)


class AddAsset(QtWidgets.QDialog, ui_pm_add_asset.Ui_AddAsset):
    """
    Create asset entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddAsset, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.asset_ui = AssetUI()
        self.layoutAsset.addWidget(self.asset_ui)

        self.project = None
        self.asset_types = None
        self.model_asset_types = None

        self.btnAddAsset.clicked.connect(self.add_asset)
        self.btnAddAsset.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddProject class is shown (AddProject.show())
        """

        # Clean UI
        self.asset_ui.linProjectName.setText(self.project.name)
        self.asset_ui.linAssetName.clear()
        self.asset_ui.txtDescription.clear()

        # Add asset types to ui
        self.model_asset_types = Model(self.asset_types)
        self.asset_ui.comAssetType.setModel(self.model_asset_types)

    def add_asset(self):
        """
        Create asset entity in the DB
        """

        # Get asset name from UI
        asset_name = self.asset_ui.linAssetName.text()
        asset_type_index = self.asset_ui.comAssetType.model().index(self.asset_ui.comAssetType.currentIndex(), 0)
        asset_type_id = asset_type_index.data(QtCore.Qt.UserRole + 1)
        # asset_publish = self.asset_ui.linHDAName.text()
        asset_description = self.asset_ui.txtDescription.toPlainText()

        self.parent.add_asset(self.project, asset_name, asset_type_id, asset_description)


class AddSequence(QtWidgets.QDialog, ui_pm_add_sequence.Ui_AddSequence):
    """
    Create sequence entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddSequence, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.sequence_ui = SequenceUI()
        self.layoutSequence.addWidget(self.sequence_ui)

        self.project = None

        self.btnAddSequence.clicked.connect(self.add_sequence)
        self.btnAddSequence.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddSequence class is shown (AddSequence.show())
        :param event:
        :return:
        """

        self.sequence_ui.linProjectName.setText(self.project.name)
        self.sequence_ui.linSequenceName.clear()
        self.sequence_ui.txtDescription.clear()

    def add_sequence(self):
        """
        Create sequence entity in the DB
        :return:
        """

        # Get sequence name from UI
        sequence_name = self.sequence_ui.linSequenceName.text()
        sequence_description = self.sequence_ui.txtDescription.toPlainText()

        self.parent.add_sequence(self.project, sequence_name, sequence_description)


class AddShot(QtWidgets.QDialog, ui_pm_add_shot.Ui_AddShot):
    """
    Create shot entity in the database
    """
    def __init__(self, parent=None):
        # SETUP UI WINDOW
        super(AddShot, self).__init__(parent=parent)
        self.setupUi(self)
        # Add shot properties widget
        self.parent = parent
        self.shot_ui = ShotUI()
        self.layoutShot.addWidget(self.shot_ui)

        self.project = None
        self.sequence = None

        self.btnAddShot.clicked.connect(self.add_shot)
        self.btnAddShot.clicked.connect(self.close)

    def showEvent(self, event):
        """
        Executed when AddShot class is shown (AddShot.show())
        """

        self.shot_ui.linProjectName.setText(self.project.name)
        self.shot_ui.linSequenceName.setText(self.sequence.name)
        self.shot_ui.linShotName.clear()
        self.shot_ui.txtDescription.clear()

    def add_shot(self):
        """
        Create sequence entity in the DB
        """

        # Get sequence name from UI
        shot_name = self.shot_ui.linShotName.text()
        shot_start_frame = self.shot_ui.linStartFrame.text()
        shot_end_frame = self.shot_ui.linEndFrame.text()
        shot_width = self.shot_ui.linWidth.text()
        shot_height = self.shot_ui.linHeight.text()
        shot_description = self.shot_ui.txtDescription.toPlainText()

        self.parent.add_shot(self.sequence,
                             shot_name,
                             shot_start_frame,
                             shot_end_frame,
                             shot_width,
                             shot_height,
                             shot_description)


class ProjectManager(QtWidgets.QMainWindow,  ui_pm_main.Ui_ProjectManager):
    """
    Custom "Shotgun". Create, edit, delete projects data. Launch apps

    Project, Asset, Sequence, Shot widgets are nested (to reuse same widget in 2 places):
        ASSET >> ASSET PROPERTIES >> PROJECT MANAGER
        ASSET >> ADD ASSET

    """

    def __init__(self):
        super(ProjectManager, self).__init__()
        # SETUP UI
        self.setupUi(self)
        self.project_properties_ui = ProjectProperties()
        self.asset_properties_ui = AssetProperties()
        self.sequence_properties_ui = SequenceProperties()
        self.shot_properties_ui = ShotProperties()
        self.layoutProperties.addWidget(self.project_properties_ui)
        self.layoutProperties.addWidget(self.asset_properties_ui)
        self.layoutProperties.addWidget(self.sequence_properties_ui)
        self.layoutProperties.addWidget(self.shot_properties_ui)
        self.btn_project_create = 'Create Project'
        self.btn_project_update = 'Update Project'

        # HIDE LIBRARY (until we implement functionality for the libraries)
        self.boxLibrary.hide()

        # SETUP ENVIRONMENT
        os.environ['EVE_ROOT'] = os.environ['EVE_ROOT'].replace('\\', '/')
        self.eve_root = os.environ['EVE_ROOT']

        # Load Eve DB
        # Create database file if not exists (first time Project Manager launch)
        self.SQL_FILE_PATH = settings.SQL_FILE_PATH.format(self.eve_root)
        if not os.path.exists(self.SQL_FILE_PATH):
            if not os.path.exists(os.path.dirname(self.SQL_FILE_PATH)):
                os.makedirs(os.path.dirname(self.SQL_FILE_PATH))
            self.create_database()
        self.eve_data = database.EveData(self.SQL_FILE_PATH)
        self.model_projects = Model(self.eve_data.projects)
        self.model_assets = None
        self.model_sequences = None
        self.model_shots = None

        # Load ADD ENTITY classes
        self.AP = AddProject(self)
        self.AA = AddAsset(self)
        self.AE = AddSequence(self)
        self.AS = AddShot(self)

        # Fill UI with data from database
        self.init_pm()

        # Connect functions
        # Menu
        self.actionEveDocs.triggered.connect(self.docs)
        # Project section
        self.listProjects.clicked.connect(self.init_project)
        self.btnAddProject.clicked.connect(self.AP.exec_)
        self.btnDelProject.clicked.connect(self.del_project)
        # Asset section
        self.listAssets.clicked.connect(self.init_asset)
        self.btnAddAsset.clicked.connect(self.run_add_asset)
        self.btnDelAsset.clicked.connect(self.del_asset)
        # Sequence section
        self.listSequences.clicked.connect(self.init_sequence)
        self.btnAddSequence.clicked.connect(self.run_add_sequence)
        self.btnDelSequence.clicked.connect(self.del_sequence)
        # Shot section
        self.listShots.clicked.connect(self.init_shot)
        self.btnAddShot.clicked.connect(self.run_add_shot)
        self.btnDelShot.clicked.connect(self.del_shot)

        # Project properties
        self.project_properties_ui.btnCreateProject.clicked.connect(self.run_create_project)
        self.project_properties_ui.btnLaunchHoudini.clicked.connect(self.launch_houdini)

        # Asset properties
        self.asset_properties_ui.btnUpdateAsset.clicked.connect(self.update_asset)

        # Sequence properties
        self.sequence_properties_ui.btnUpdateSequence.clicked.connect(self.update_sequence)

        # Shot properties
        self.shot_properties_ui.btnUpdateShot.clicked.connect(self.update_shot)

    def docs(self):
        """
        Run Carry Over HELP in web browser
        """

        # Root folder for the report files
        webbrowser.open(settings.DOCS)

    def create_database(self):
        """
        Create database file with necessary tables
        :return:
        """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        database.init_database(connection, cursor)
        database.init_asset_types(connection, cursor)
        database.init_file_types(connection, cursor)

        connection.close()

    def init_pm(self):
        """
        Read Athena database and populate information in Project Manager UI
        :return:
        """

        # Hide PROPERTIES widgets
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.hide()

        # Fill PROJECTS and MATERIALS views
        self.listProjects.setModel(self.model_projects)

    def init_project(self):

        # Show and set up PROPERTIES widget
        self.project_properties_ui.show()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.hide()

        # Setup data
        model_index = self.listProjects.currentIndex()  # .selectedIndexes()[0]
        project_id = model_index.data(QtCore.Qt.UserRole + 1)
        project = self.eve_data.get_project(project_id)
        self.eve_data.selected_project = project
        self.eve_data.get_project_assets(project)
        self.eve_data.get_project_sequences(project)

        # Fill Project Properties widget
        project_root = build_project_root(project.name)
        self.project_properties_ui.project_ui.linProjectLocation.setText(project_root)
        self.project_properties_ui.project_ui.linProjectLocation.setEnabled(False)
        self.project_properties_ui.project_ui.linProjectName.setText(project.name)
        self.project_properties_ui.project_ui.linProjectName.setEnabled(False)
        self.project_properties_ui.project_ui.linHoudini.setText(project.houdini_build)
        self.project_properties_ui.project_ui.linProjectWidth.setText(str(project.width))
        self.project_properties_ui.project_ui.linProjectHeight.setText(str(project.height))
        self.project_properties_ui.project_ui.txtDescription.setText(project.description)

        # FILL ASSET and SEQUENCE WIDGETS
        self.model_assets = Model(self.eve_data.project_assets)
        self.listAssets.setModel(self.model_assets)

        self.model_sequences = Model(self.eve_data.project_sequences)
        self.listSequences.setModel(self.model_sequences)

        # Enable/disable UI buttons depending on project existence
        if os.path.exists(project_root):
            self.project_properties_ui.btnCreateProject.setText(self.btn_project_update)
            self.project_properties_ui.btnLaunchHoudini.setEnabled(True)
            self.project_properties_ui.btnLaunchNuke.setEnabled(True)
            self.project_properties_ui.btnOpenFolder.setEnabled(True)
        else:
            self.project_properties_ui.btnCreateProject.setText(self.btn_project_create)
            self.project_properties_ui.btnLaunchHoudini.setEnabled(False)
            self.project_properties_ui.btnLaunchNuke.setEnabled(False)
            self.project_properties_ui.btnOpenFolder.setEnabled(False)

    def init_asset(self):
        """
        Show/hide SHOTS Properties area depending on user selection in shots list widget
        Fill shots properties widgets

        :return:
        """

        # Show and set up PROPERTIES widget
        self.project_properties_ui.hide()
        self.asset_properties_ui.show()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.hide()

        # Setup data
        model_index = self.listAssets.currentIndex()
        asset_id = model_index.data(QtCore.Qt.UserRole + 1)
        asset = self.eve_data.get_asset(asset_id)
        self.eve_data.selected_asset = asset

        # Fill ASSET WIDGET
        self.asset_properties_ui.asset_ui.linProjectName.setText(self.eve_data.selected_project.name)
        self.asset_properties_ui.asset_ui.linProjectName.setEnabled(False)
        self.asset_properties_ui.asset_ui.linAssetName.setText(asset.name)
        self.asset_properties_ui.asset_ui.linAssetName.setEnabled(False)

        model_asset_types = Model(self.eve_data.asset_types)
        self.asset_properties_ui.asset_ui.comAssetType.setModel(model_asset_types)
        # Find AssetType string by database index
        # !!! Probably wrong implementation of model data! and can be done via Model() !!!!!
        self.eve_data.get_asset_type_string(asset.type)
        self.asset_properties_ui.asset_ui.comAssetType.setCurrentText(self.eve_data.asset_type_string)
        self.asset_properties_ui.asset_ui.txtDescription.setText(asset.description)

    def init_sequence(self):

        # Show and set up PROPERTIES widget
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.show()
        self.shot_properties_ui.hide()

        # Setup data for sequence
        model_index = self.listSequences.currentIndex()
        sequence_id = model_index.data(QtCore.Qt.UserRole + 1)
        sequence = self.eve_data.get_sequence(sequence_id)
        self.eve_data.selected_sequence = sequence
        # and shot
        self.eve_data.get_sequence_shots(sequence.id)
        self.model_shots = Model(self.eve_data.sequence_shots)
        self.listShots.setModel(self.model_shots)

        # Fill SEQUENCE WIDGET
        self.sequence_properties_ui.sequence_ui.linProjectName.setText(self.eve_data.selected_project.name)
        self.sequence_properties_ui.sequence_ui.linSequenceName.setText(sequence.name)
        self.sequence_properties_ui.sequence_ui.linSequenceName.setEnabled(False)
        self.sequence_properties_ui.sequence_ui.txtDescription.setText(sequence.description)

    def init_shot(self):

        # Show and set up PROPERTIES widget
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        self.sequence_properties_ui.hide()
        self.shot_properties_ui.show()

        # Setup data
        model_index = self.listShots.currentIndex()
        shot_id = model_index.data(QtCore.Qt.UserRole + 1)
        shot = self.eve_data.get_shot(shot_id)
        self.eve_data.selected_shot = shot

        # Fill SHOT WIDGET
        self.shot_properties_ui.shot_ui.linProjectName.setText(self.eve_data.selected_project.name)
        self.shot_properties_ui.shot_ui.linSequenceName.setText(self.eve_data.selected_sequence.name)
        self.shot_properties_ui.shot_ui.linShotName.setText(self.eve_data.selected_shot.name)
        self.shot_properties_ui.shot_ui.linStartFrame.setText(str(shot.start_frame))
        self.shot_properties_ui.shot_ui.linEndFrame.setText(str(shot.end_frame))
        self.shot_properties_ui.shot_ui.linWidth.setText(str(shot.width))
        self.shot_properties_ui.shot_ui.linHeight.setText(str(shot.height))
        self.shot_properties_ui.shot_ui.txtDescription.setText(shot.description)

    def add_project(self, project_name, houdini_build, project_width, project_height, project_description):
        """
        Add project to database and reload UI
        """

        # Create project object
        project = database.Project(project_name)
        project.houdini_build = houdini_build
        project.width = project_width
        project.height = project_height
        project.description = project_description

        # Add project to DB and update UI
        self.model_projects.layoutAboutToBeChanged.emit()
        self.eve_data.add_project(project)
        self.model_projects.layoutChanged.emit()

    def add_asset(self, project, asset_name, asset_type_id, asset_description):
        """
        Add new asset data to the DB
        """

        # Create asset and set asset properties
        asset = database.Asset(asset_name, project.id)
        asset.type = asset_type_id
        asset.description = asset_description

        # Add asset to DB and update UI
        self.model_assets.layoutAboutToBeChanged.emit()
        self.eve_data.add_asset(asset, project.id)
        self.model_assets.layoutChanged.emit()

    def add_sequence(self, project, sequence_name, sequence_description):

        # Create sequence and set sequence properties
        sequence = database.Sequence(sequence_name, project.id)
        sequence.description = sequence_description

        # Add asset to DB and update UI
        self.model_sequences.layoutAboutToBeChanged.emit()
        self.eve_data.add_sequence(sequence, project.id)
        self.model_sequences.layoutChanged.emit()

    def add_shot(self, sequence, shot_name, shot_start_frame, shot_end_frame, shot_width, shot_height, shot_description):

        # Create shot and set shot properties
        shot = database.Shot(shot_name, sequence.id)
        shot.start_frame = shot_start_frame
        shot.end_frame = shot_end_frame
        shot.width = shot_width
        shot.height = shot_height
        shot.description = shot_description

        # Add asset to DB and update UI
        self.model_shots.layoutAboutToBeChanged.emit()
        self.eve_data.add_shot(shot, sequence.id)
        self.model_shots.layoutChanged.emit()

    def del_project(self):
        """
        Delete project from database, update UI
        """

        model_index = self.listProjects.currentIndex()
        project_id = model_index.data(QtCore.Qt.UserRole + 1)
        project_name = model_index.data(QtCore.Qt.UserRole + 2)

        # Notify user about deletion
        warn = Warnings(project_name)
        if warn.exec_():
            # Remove project from DB
            self.model_projects.layoutAboutToBeChanged.emit()
            self.eve_data.del_project(project_id)
            self.model_projects.layoutChanged.emit()

    def del_asset(self):
        """
        Delete shot from database, update UI
        """

        model_index = self.listAssets.currentIndex()
        asset_id = model_index.data(QtCore.Qt.UserRole + 1)
        asset_name = model_index.data(QtCore.Qt.UserRole + 2)

        # Notify user about delete
        WARN = Warnings(asset_name)
        if WARN.exec_():
            self.model_assets.layoutAboutToBeChanged.emit()
            self.eve_data.del_asset(asset_id)
            self.model_assets.layoutChanged.emit()

    def del_sequence(self):

        model_index = self.listSequences.currentIndex()
        sequence_id = model_index.data(QtCore.Qt.UserRole + 1)
        sequence_name = model_index.data(QtCore.Qt.UserRole + 2)

        # Notify user about delete
        WARN = Warnings(sequence_name)
        if WARN.exec_():
            self.model_sequences.layoutAboutToBeChanged.emit()
            self.eve_data.del_sequence(sequence_id)
            self.model_sequences.layoutChanged.emit()

    def del_shot(self):

        model_index = self.listSequences.currentIndex()
        shot_id = model_index.data(QtCore.Qt.UserRole + 1)
        shot_name = model_index.data(QtCore.Qt.UserRole + 2)

        # Notify user about delete
        WARN = Warnings(shot_name)
        if WARN.exec_():
            self.model_shots.layoutAboutToBeChanged.emit()
            self.eve_data.del_shot(shot_id)
            self.model_shots.layoutChanged.emit()

    def update_project(self):
        """
        Update project data in the DB
        """

        print '>> Updating project...'

        # Load athena data
        project = self.eve_data.selected_project

        # Update project data
        project.maya = self.project_properties_ui.project_ui.linHoudini.text()
        project.width = self.project_properties_ui.project_ui.linProjectWidth.text()
        project.height = self.project_properties_ui.project_ui.linProjectHeight.text()
        project.description = self.project_properties_ui.project_ui.txtDescription.toPlainText()

        self.eve_data.update_project(project)

        # Update folder structure on HDD
        # FOLDERS = build_folder_structure()
        # self.create_folders(build_project_root(project_name), FOLDERS)

    def update_asset(self):
        """
        Update asset data in DB according to Asset Properties widget.
        """

        print '>> Updating asset...'

        # Get asset
        asset = self.eve_data.selected_asset

        # Modify asset data
        asset_type_index = self.asset_properties_ui.asset_ui.comAssetType.model().index(
                                                    self.asset_properties_ui.asset_ui.comAssetType.currentIndex(), 0)
        asset_type_id = asset_type_index.data(QtCore.Qt.UserRole + 1)

        asset.type = asset_type_id
        asset.description = self.asset_properties_ui.asset_ui.txtDescription.toPlainText()

        # Save asset data
        self.eve_data.update_asset(asset)

        print '>> Asset "{}" updated!'.format(asset.name)

    def update_sequence(self):
        """
        Update sequence data in DB according to Sequence Properties widget.

        """

        print '>> Updating sequence...'

        # Get sequence
        sequence = self.eve_data.selected_sequence

        # Modify sequence data
        sequence.description = self.sequence_properties_ui.sequence_ui.txtDescription.toPlainText()

        # Save sequence data
        self.eve_data.update_sequence(sequence)

        print '>> Sequence "{}" updated!'.format(sequence.name)

    def update_shot(self):
        """
        Update sequence data in DB according to Sequence Properties widget.
        """

        print '>> Updating shot...'

        # Get shot
        shot = self.eve_data.selected_shot

        # Modify shot data
        shot.start_frame = self.shot_properties_ui.shot_ui.linStartFrame.text()
        shot.end_frame = self.shot_properties_ui.shot_ui.linEndFrame.text()
        shot.width = self.shot_properties_ui.shot_ui.linWidth.text()
        shot.height = self.shot_properties_ui.shot_ui.linHeight.text()
        shot.description = self.shot_properties_ui.shot_ui.txtDescription.toPlainText()

        # Save shot data
        self.eve_data.update_shot(shot)

        print '>> Shot "{}" updated!'.format(shot.name)

    # MAIN FUNCTIONS
    def launch_houdini(self):
        import launch_houdini

        HOUDINI = settings.HOUDINI.format(self.project_properties_ui.project_ui.linHoudini.text())

        # Run Maya
        launch_houdini.run(self.eve_root,
                           settings.PROJECTS,
                           HOUDINI,
                           self.eve_data.selected_project.name)

    def create_folder(self, path):
        """
        Create folder at input path
        :param path: Path to create folder (C:/TEMP)
        """

        if not os.path.exists(path):
            os.makedirs(path)

    def create_folders(self, root, folders_template):
        """
        Recursively build folder structure based on template
        :param root: Root directory to create folder structure
        :param folders_template: List of lists, folder structure template
        :return:
        """

        if folders_template:
            for folder in folders_template:
                folder_name = folder[0]
                path = '{}/{}'.format(root, folder_name)
                self.create_folder(path)
                self.create_folders(path, folder[1])

    def create_project(self, project_name):
        """
        Create project structure with necessary data on HDD
        :param project_name: string, Project code
        :return:
        """

        # Build project root folder string
        project_root = build_project_root(project_name)
        # Get project data from projects DB
        project = self.eve_data.get_project_by_name(project_name)

        # Create folder structure on HDD
        folders = build_folder_structure()  # assets=project.assets, shots=project.shots
        self.create_folders(project_root, folders)

        # Open project folder
        subprocess.Popen('explorer "{}"'.format(project_root.replace('/', '\\')))

    def run_create_project(self):
        """
        Read UI data and run project creation procedure
        """

        # Read UI data
        project_name = self.eve_data.selected_project.name

        # Determine project action: create new or update existing
        if self.project_properties_ui.btnCreateProject.text() == self.btn_project_update:
            self.update_project()
        else:
            print '>> Creating project...'
            # Create project
            self.create_project(project_name)
            print '>> Project creation complete!'

    def run_add_asset(self):
        """
        Run create asset window
        """

        # Check if project selected in UI
        if not self.listProjects.selectedIndexes():
            print 'Select Project to create assets!'

        else:
            self.AA.project = self.eve_data.selected_project
            self.AA.asset_types = self.eve_data.asset_types
            self.AA.exec_()

    def run_add_sequence(self):

        # Check if project selected in UI
        if not self.listProjects.selectedIndexes():
            print 'Select Project to create sequence!'

        else:
            self.AE.project = self.eve_data.selected_project
            self.AE.exec_()

    def run_add_shot(self):

        # Check if project selected in UI
        if not self.listSequences.selectedIndexes():
            print 'Select Sequence to create shot!'

        else:
            self.AS.project = self.eve_data.selected_project
            self.AS.sequence = self.eve_data.selected_sequence
            self.AS.exec_()


# Run Project Manager
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    PM = ProjectManager()
    PM.show()
    app.exec_()
