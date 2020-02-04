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

from core import database
from core import settings
from core.common import Model


# TODO: Create per-project Houdini launcher 


def build_project_root(project_name):
    '''Build project root folder string'''

    project_root = '{0}/{1}'.format(settings.PROJECTS, project_name)
    return project_root


def build_folder_structure():
    '''
    Create list for project folder structure

    TODO: build assets, sequences and shots folders based on EVE data
    assets=None, shots=None

    :param assets: list of Asset objects, assets of current project
    :param shots:  list of Shot objects, shots of current project
    :return:
    '''

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
    '''
    Shot properties widget
    '''
    def __init__(self):
        super(ProjectUI, self).__init__()
        self.setupUi(self)
        self.linHoudini.setText(settings.default_build)


class AssetUI(QtWidgets.QWidget, ui_asset.Ui_Asset):
    '''
    Shot properties widget
    '''
    def __init__(self):
        super(AssetUI, self).__init__()
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


class AddProject(QtWidgets.QDialog, ui_pm_add_project.Ui_AddProject):
    '''
    Add project entity Dialog.
    '''
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
        '''
        Executed when AppProject class is shown (AddProject.show())
        :param event:
        :return:
        '''

        # Clean UI
        self.project_ui.linProjectName.clear()
        self.project_ui.txtDescription.clear()
        self.project_ui.linProjectName.clear()

    def project_name_changed(self):

        project_name = self.project_ui.linProjectName.text()
        project_root = build_project_root(project_name)
        self.project_ui.linProjectLocation.setText(project_root)

    def add_project(self):
        '''
        Create asset entity in datatbase
        :return:
        '''

        # Get project data from UI
        project_name = self.project_ui.linProjectName.text()
        houdini_build = self.project_ui.linHoudini.text()
        project_width = self.project_ui.linProjectWidth.text()
        project_height = self.project_ui.linProjectHeight.text()
        project_description = self.project_ui.txtDescription.toPlainText()
        # Call add_project in PM class
        self.parent.add_project(project_name, houdini_build, project_width, project_height, project_description)


class AddAsset(QtWidgets.QDialog, ui_pm_add_asset.Ui_AddAsset):
    '''
    Create asset entity in the database
    '''
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
        '''
        Executed when AddProject class is shown (AddProject.show())
        :param event:
        :return:
        '''
        # Clean UI
        self.asset_ui.linAssetName.clear()
        self.asset_ui.txtDescription.clear()
        self.asset_ui.linProjectName.setText(self.project.name)
        self.asset_ui.linProjectName.setEnabled(False)
        # Add asset types to ui
        self.model_asset_types = Model(self.asset_types)
        self.asset_ui.comAssetType.setModel(self.model_asset_types)

    def add_asset(self):
        '''
        Create asset entity in the DB
        :return:
        '''

        # Get asset name from UI
        asset_name = self.asset_ui.linAssetName.text()
        asset_type_index = self.asset_ui.comAssetType.model().index(self.asset_ui.comAssetType.currentIndex(), 0)
        asset_type_id = asset_type_index.data(QtCore.Qt.UserRole + 1)
        # asset_publish = self.asset_ui.linHDAName.text()
        asset_description = self.asset_ui.txtDescription.toPlainText()

        self.parent.add_asset(asset_name, self.project, asset_type_id, asset_description)


class ProjectManager(QtWidgets.QMainWindow,  ui_pm_main.Ui_ProjectManager):
    '''
    Custom "Shotgun". Create, edit, delete projects data. Launch apps
    '''

    def __init__(self):
        super(ProjectManager, self).__init__()
        # SETUP UI
        self.setupUi(self)
        self.project_properties_ui = ProjectProperties()
        self.asset_properties_ui = AssetProperties()
        # self.shot_properties_ui = ShotProperties()
        self.layoutProperties.addWidget(self.project_properties_ui)
        self.layoutProperties.addWidget(self.asset_properties_ui)
        # self.layoutProperties.addWidget(self.shot_properties_ui)
        self.btn_project_create = 'Create Project'
        self.btn_project_update = 'Update Project'

        # HIDE LIBRARY
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

        # Load classes
        self.AP = AddProject(self)
        self.AA = AddAsset(self)

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

        # Project properties
        self.project_properties_ui.btnCreateProject.clicked.connect(self.run_create_project)
        self.project_properties_ui.btnLaunchHoudini.clicked.connect(self.launch_houdini)

        # Asset properties
        self.asset_properties_ui.btnUpdateAsset.clicked.connect(self.update_asset)

    def docs(self):
        '''
        Run Carry Over HELP in web browser
        '''

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
        '''
        Read Athena database and populate information in Project Manager UI
        :return:
        '''

        # Hide PROPERTIES widgets
        self.project_properties_ui.hide()
        self.asset_properties_ui.hide()
        # self.shot_properties_ui.hide()

        # Fill PROJECTS and MATERIALS views
        self.listProjects.setModel(self.model_projects)

    def init_project(self):

        # Show and set up PROPERTIES widget
        self.asset_properties_ui.hide()
        # self.shot_properties_ui.hide()
        self.project_properties_ui.show()

        # Setup data
        model_index = self.listProjects.currentIndex()  # .selectedIndexes()[0]
        project_id = model_index.data(QtCore.Qt.UserRole + 1)
        project = self.eve_data.get_project(project_id)
        self.eve_data.selected_project = project
        self.eve_data.get_project_assets(project)
        # self.eve_data.get_project_sequences(project)
        # self.eve_data.get_project_shots(project)

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

        # FILL ASSET and SHOTS WIDGETS
        self.model_assets = Model(self.eve_data.project_assets)
        # self.model_sequences = Model(self.eve_data.project_shots)
        # self.model_shots = Model(self.eve_data.project_shots)
        self.listAssets.setModel(self.model_assets)
        # self.listSequences.setModel(self.model_shots)
        # self.listShots.setModel(self.model_shots)

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
        #self.shot_properties_ui.hide()
        self.asset_properties_ui.show()

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

    def add_project(self, project_name, build, project_width, project_height, project_description):
        '''
        Add project to database and reload UI
        :param catch: Determine if function executed from this class or from AddProject()
        :return:
        '''

        # Create project object
        project = database.Project(project_name)
        project.houdini_build = build
        project.width = project_width
        project.height = project_height
        project.description = project_description

        # Add project to DB and update UI
        self.model_projects.layoutAboutToBeChanged.emit()
        self.eve_data.add_project(project)
        self.model_projects.layoutChanged.emit()

    def add_asset(self, asset_name, project, asset_type_id, asset_description):
        '''
        Add new asset data to the DB
        :param project:
        :param asset_name:
        :param asset_description:
        :return:
        '''

        # Create asset and set asset properties
        asset = database.Asset(asset_name, project.id)
        asset.type = asset_type_id
        asset.description = asset_description

        # Add asset to DB and update UI
        self.model_assets.layoutAboutToBeChanged.emit()
        self.eve_data.add_asset(asset, project.id)
        self.model_assets.layoutChanged.emit()

    def del_project(self):
        """
        Delete project from database, update UI
        :return:
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
        :return:
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

    def update_project(self):
        """
        Update project data in the DB
        :param project_name:
        :return:
        """

        print '>> Updating project...'

        # Load athena data
        project = self.eve_data.selected_project

        # Update DB
        houdini_build = self.project_properties_ui.project_ui.linHoudini.text()
        project_description = self.project_properties_ui.project_ui.txtDescription.toPlainText()
        width = self.project_properties_ui.project_ui.linProjectWidth.text()
        height = self.project_properties_ui.project_ui.linProjectHeight.text()

        project.maya = houdini_build
        project.width = width
        project.height = height
        project.description = project_description

        self.eve_data.update_project(project)

        # Update folder structure on HDD
        # FOLDERS = build_folder_structure()
        # self.create_folders(build_project_root(project_name), FOLDERS)

    def update_asset(self):
        """
        Update asset data in DB according to Asset Properties widget.
        Now only update description. Cos add-del trims affects database immediately
        :return:
        """

        print '>> Updating asset...'

        # Get asset
        asset = self.eve_data.selected_asset

        # Modify asset data
        asset_type_index = self.asset_properties_ui.asset_ui.comAssetType.model().index(
                                                    self.asset_properties_ui.asset_ui.comAssetType.currentIndex(), 0)
        asset_type_id = asset_type_index.data(QtCore.Qt.UserRole + 1)
        description = self.asset_properties_ui.asset_ui.txtDescription.toPlainText()

        asset.type = asset_type_id
        asset.description = description

        # Save asset data
        self.eve_data.update_asset(asset)

        print '>> Asset "{}" updated!'.format(asset.name)

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
        '''
        Create folder at input path
        :param path: Path to create folder (C:/TEMP)
        '''

        if not os.path.exists(path):
            os.makedirs(path)

    def create_folders(self, root, folders_template):
        '''
        Recursively build folder structure based on template
        :param root: Root directory to create folder structure
        :param folders_template: List of lists, folder structure template
        :return:
        '''

        if folders_template:
            for folder in folders_template:
                folder_name = folder[0]
                path = '{}/{}'.format(root, folder_name)
                self.create_folder(path)
                self.create_folders(path, folder[1])

    def create_project(self, project_name):
        '''
        Create project structure with necessary data on HDD
        :param project_name: string, Project code
        :return:
        '''

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
        '''
        Read UI data and run project creation procedure
        :return:
        '''

        # Read UI data
        project_name = self.eve_data.selected_project.name

        # Determine project action: create new or update existing
        # TODO: switch to DB check ???
        if self.project_properties_ui.btnCreateProject.text() == self.btn_project_update:
            self.update_project()
        else:
            print '>> Creating project...'
            # Create project
            self.create_project(project_name)
            print '>> Project creation complete!'

    def run_add_asset(self):
        '''
        Run create asset window
        :return:
        '''

        # Check if project selected in UI
        if not self.listProjects.selectedIndexes():
            print 'Select Project to create assets!'

        else:
            model_index = self.listProjects.currentIndex()
            project_id = model_index.data(QtCore.Qt.UserRole + 1)
            project = self.eve_data.get_project(project_id)
            self.AA.project = project
            self.AA.asset_types = self.eve_data.asset_types
            self.AA.exec_()


# Run Project Manager
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    PM = ProjectManager()
    PM.show()
    app.exec_()