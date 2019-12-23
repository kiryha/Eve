import os
import sqlite3
import subprocess
import webbrowser
from PySide2 import QtCore, QtWidgets

# Import UI
from ui import ui_pm_main
from ui import ui_project
from ui import ui_project_properties
from ui import ui_pm_add_project

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


class ProjectUI(QtWidgets.QWidget, ui_project.Ui_Project):
    '''
    Shot properties widget
    '''
    def __init__(self):
        super(ProjectUI, self).__init__()
        self.setupUi(self)
        self.linHoudini.setText(settings.default_build)


class ProjectProperties(QtWidgets.QWidget, ui_project_properties.Ui_ProjectProperties):
    def __init__(self):
        super(ProjectProperties, self).__init__()
        self.setupUi(self)
        self.project_ui = ProjectUI()
        self.layoutProject.addWidget(self.project_ui)


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
        self.project_ui.linProjectName.setText('eve_example_new')

    def project_name_changed(self):

        project_name = self.project_ui.linProjectName.text()
        project_root = build_project_root(project_name)
        self.project_ui.labProjectLocation.setText(project_root)

    def add_project(self):
        '''
        Create asset entity in datatbase
        :return:
        '''

        # Get project data from UI
        project_name = self.project_ui.linProjectName.text()
        houdini_build = self.project_ui.linHoudini.text()
        project_description = self.project_ui.txtDescription.toPlainText()
        # Call add_project in PM class
        self.parent.add_project(project_name, houdini_build, project_description)


class ProjectManager(QtWidgets.QMainWindow,  ui_pm_main.Ui_ProjectManager):
    '''
    Custom "Shotgun". Create, edit, delete projects data. Launch apps
    '''

    def __init__(self):
        super(ProjectManager, self).__init__()
        # SETUP UI
        self.setupUi(self)
        self.project_properties_ui = ProjectProperties()
        self.layoutProperties.addWidget(self.project_properties_ui)
        self.btn_project_create = 'Create Project'
        self.btn_project_update = 'Update Project'

        # SETUP ENVIRONMENT
        os.environ['EVE_ROOT'] = os.environ['EVE_ROOT'].replace('\\', '/')
        self.eve_root = os.environ['EVE_ROOT']

        # Load Eve DB
        # Create database file if not exists (first time Project Manager launch)
        self.SQL_FILE_PATH = settings.SQL_FILE_PATH.format(self.eve_root)
        if not os.path.exists(os.path.dirname(self.SQL_FILE_PATH)):
            os.makedirs(os.path.dirname(self.SQL_FILE_PATH))
            self.create_database()
        self.eve_data = database.Data(self.SQL_FILE_PATH)
        self.model_projects = Model(self.eve_data.projects)
        self.model_assets = None
        self.model_sequences = None
        self.model_shots = None

        # Load classes
        self.AP = AddProject(self)

        # Fill UI with data from database
        self.init_pm()

        # Connect functions
        # Menu
        self.actionEveDocs.triggered.connect(self.documentation)
        # Add project, assets, sequences and shots
        self.btnAddProject.clicked.connect(self.AP.exec_)
        # Project properties
        self.listProjects.clicked.connect(self.init_project)
        self.project_properties_ui.btnCreateProject.clicked.connect(self.run_create_project)
        self.project_properties_ui.btnLaunchHoudini.clicked.connect(self.launch_houdini)

    def documentation(self):
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

        connection.close()

    def init_pm(self):
        '''
        Read Athena database and populate information in Project Manager UI
        :return:
        '''

        # Hide PROPERTIES widgets
        self.project_properties_ui.hide()
        # self.asset_properties_ui.hide()
        # self.shot_properties_ui.hide()
        # self.material_properties_ui.hide()

        # Fill PROJECTS and MATERIALS views
        self.listProjects.setModel(self.model_projects)

    def init_project(self):

        # Show and set up PROPERTIES widget
        # self.asset_properties_ui.hide()
        # self.shot_properties_ui.hide()
        self.project_properties_ui.show()

        # Setup data
        model_index = self.listProjects.currentIndex()  # .selectedIndexes()[0]
        project_id = model_index.data(QtCore.Qt.UserRole + 1)
        project = self.eve_data.get_project(project_id)
        self.eve_data.selected_project = project
        # self.eve_data.get_project_assets(project)
        # self.eve_data.get_project_sequences(project)
        # self.eve_data.get_project_shots(project)

        # Fill Project Properties widget
        project_root = build_project_root(project.name)
        self.project_properties_ui.project_ui.labProjectLocation.setText(project_root)
        self.project_properties_ui.project_ui.linProjectName.setText(project.name)
        self.project_properties_ui.project_ui.linProjectName.setEnabled(False)
        self.project_properties_ui.project_ui.linHoudini.setText(project.houdini_build)
        self.project_properties_ui.project_ui.txtDescription.setText(project.description)

        # FILL ASSET and SHOTS WIDGETS
        # self.model_assets = Model(self.eve_data.project_assets)
        # self.model_sequences = Model(self.eve_data.project_shots)
        # self.model_shots = Model(self.eve_data.project_shots)
        # self.listAssets.setModel(self.model_assets)
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

    def add_project(self, project_name, houdini_build, project_description):
        '''
        Add project to database and reload UI
        :param catch: Determine if function executed from this class or from AddProject()
        :return:
        '''


        # Create project object
        project = database.Project(project_name)
        project.houdini_build = houdini_build
        project.description = project_description

        # Add project to DB and update UI
        self.model_projects.layoutAboutToBeChanged.emit()
        self.eve_data.add_project(project)
        self.model_projects.layoutChanged.emit()

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

        # Pause launcher creation. BAT files are not working in Ford.
        # self.create_local_launcher(project_root, project_name, project.maya)

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
            self.update_project(project_name)
        else:
            print '>> Creating project...'
            # Create project
            self.create_project(project_name)
            print '>> Project creation complete!'


# Run Project Manager
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    PM = ProjectManager()
    PM.show()
    app.exec_()