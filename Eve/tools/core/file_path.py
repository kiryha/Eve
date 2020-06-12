"""
Create file path strings for any file in Eve
Asset path example: 'Z:/projects/Avatar/3D/scenes/ASSETS/NYC/AST_NYC_001.hip'



File Naming convention for filePath:
<file_path> = <file_location>/<file_name>
<file_name> = <file_code>_<file_version>.<file_extension>
<file_code_version> = <file_code>_<file_version>
<file_code> = <file_prefix>_<file_base>

Versions (for current file path string):
    - NEXT: current + 1
    - LAST: maximum number of existing versions on HDD
    - LATEST: last + 1

Eve can generate/analyze 3 types of path:
    - FILE PATH:      S:/location/code_name_001.mb
                      S:/location/001/code_name_001.mb

    - FILE SEQUENCE:   S:/location/001/code_name_001.001.mb

    - FILE LOCATION:  S:/location/001

"""

# TODO: Handle sequences paths <file_name> = <file_code>_<file_version>.<frame_number>.<file_extension>
# TODO: Handle location paths <file_name> = <file_location>

import os
import glob
import settings
from PySide2 import QtWidgets, QtCore


class SNV(QtWidgets.QDialog):
    def __init__(self, file_name, version_latest, parent=None):
        super(SNV, self).__init__(parent=parent)
        # Keep window on top of Maya UI
        self.parent = parent
        self.setParent(self.parent, QtCore.Qt.WindowStaysOnTopHint)

        # Create widgets
        self.resize(400, 50)
        self.setWindowTitle('Warning! File version exists:')
        self.lab = QtWidgets.QLabel(file_name)
        self.lab.setAlignment(QtCore.Qt.AlignHCenter)
        self.btnOVR = QtWidgets.QPushButton("Overwrite")
        self.btnSNV = QtWidgets.QPushButton(" Save {} Version ".format(version_latest))
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        # Create layout and add widgets
        layout_main = QtWidgets.QVBoxLayout()
        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(self.btnOVR)
        layout_buttons.addWidget(self.btnSNV)
        layout_buttons.addWidget(self.btnCancel)
        layout_main.addWidget(self.lab)
        layout_main.addLayout(layout_buttons)
        # Set dialog layout
        self.setLayout(layout_main)
        # Add button signal to greetings slot
        self.btnOVR.clicked.connect(self.OVR)
        self.btnSNV.clicked.connect(self.SNV)
        self.btnCancel.clicked.connect(self.close)

    def OVR(self):
        self.done(2)

    def SNV(self):
        self.done(3)


class EveFilePath:
    def __init__(self, file_path=None):

        # Environment set
        self.project_root = os.environ['EVE_PROJECT']  # Z:/projects/Avatar
        # DEFINE STRINGS
        self.file_name_template = '{0}_{1}_{2}.{3}'
        self.file_name_sequence_template = '{0}_{1}_{2}.{3}.{4}'
        self.asset_root = '{0}/PROD/3D/scenes/ASSETS'.format(self.project_root)
        self.shot_root = '{0}/PROD/3D/scenes/SHOTS'.format(self.project_root)
        self.render_3d_root = '{0}/PROD/3D/images'.format(self.project_root)
        self.render_2d_root = '{0}/PROD/2D/RENDER'.format(self.project_root)
        self.comp_root = '{0}/PROD/2D/COMP'.format(self.project_root)

        # EVE FILE PATH OBJECT ATTRIBUTES
        self.type = None  # String path type ('path', 'sequence' or 'location')
        self.path = None
        self.name = None
        self.location = None
        self.prefix = None
        self.file_version = None
        self.folder_version = None
        self.code = None
        self.base = None
        self.extension = None

        # Disassemble file path if provided with initialization
        if file_path:
            self.set_path(file_path)

    # Parsing string file paths
    def set_path(self, file_path):
        self.path = file_path
        self.analyze_file_path()

    def rebuild_path(self):
        '''
        Record new PATH after modifications
        '''

        if self.folder_version:
            # Replace FOLDER VERSION in location with a new version
            location = self.location
            self.location = '{0}{1}/'.format(location[:-4], self.folder_version)

        self.path = '{0}{1}_{2}.{3}'.format(self.location, self.code, self.file_version, self.extension)

    def build_file_base(self, parts):
        ''' Calculate <file_base> part of the file name '''

        file_base = ''

        for i in range(len(parts) - 2):
            if i == 0:
                file_base += '{}'.format(parts[i + 1])
            else:
                file_base += '_{}'.format(parts[i + 1])

        return file_base

    def analyze_file_name(self):
        '''
        Disassemble <file_name> string
        Example naming conventions:
            <file_name> = AST_navigator_001.mb

        '''

        file_name = self.name

        file_extension = file_name.split('.')[-1]
        file_code_version = file_name.split('.')[0]
        parts = file_code_version.split('_')

        file_prefix = parts[0]
        file_version = parts[-1]
        file_base = self.build_file_base(parts)
        file_code = '{0}_{1}'.format(file_prefix, file_base)

        self.prefix = file_prefix
        self.file_version = file_version
        self.code = file_code
        self.base = file_base
        self.extension = file_extension

    def analyze_file_path(self):
        '''
        Disassemble string file path into components

        '''

        file_path = self.path

        file_name = file_path.split('/')[-1]
        file_location = file_path.replace('{}'.format(file_name), '')

        # Check if file path has a FOLDER VERSION
        folder_version = None
        folder_name = file_location.split('/')[-2]
        if len(folder_name) == 3:
            try:
                int(folder_name)
                folder_version = folder_name
            except:
                pass

        self.name = file_name
        self.location = file_location
        self.folder_version = folder_version

        self.analyze_file_name()

    def build_next_file_version(self):
        '''
        Create next version of provided file (current + 1)

        '''

        self.file_version = '{0:03d}'.format(int(self.file_version) + 1)
        if self.folder_version:
            self.folder_version = self.file_version

        self.rebuild_path()

    def calculate_last_version(self):
        '''
        Get latest existing file version on HDD
        :return: integer, maximum existing version
        '''

        # Get list of existing versions of file
        list_existed = glob.glob('{0}{1}_*.{2}'.format(self.location, self.code, self.extension))

        list_versions = []
        for file_path in list_existed:
            at_file = EveFilePath(file_path)
            list_versions.append(int(at_file.file_version))
        last_version = max(list_versions)

        return last_version

    def build_latest_file_version(self):
        '''
        Create LATEST version of provided file (last existed + 1)
        '''

        latest_version = self.calculate_last_version() + 1
        self.file_version = '{0:03d}'.format(latest_version)
        if self.folder_version:
            self.folder_version = self.file_version

        self.rebuild_path()

    # Build string paths for database.EveFile.file_types
    def build_path_asset_hip(self, file_type, asset_type, asset_name, version):
        """
        Build asset file path:
            <asset_root>/<asset_name>/<file_type_code>_<asset_name>_<version>.mb

        asset_type = {'description': 'Character asset', 'id': 1, 'name': 'character'}
        """

        file_prefix = file_type['prefix']
        asset_folder = '{0}S'.format(asset_type['name']).upper()
        file_name = self.file_name_template.format(file_prefix, asset_name, version, settings.HIP)
        file_path = '{0}/{1}/{2}/{3}'.format(self.asset_root, asset_folder, asset_name, file_name)
        self.type = 'path'

        print 'build_path_asset_hip [file_path] = ', file_path

        self.set_path(file_path)

    def build_path_shot_render(self, file_type, sequence_name, shot_name, version):

        # E:/256/PROJECTS/VEX/PROD/3D/scenes/SHOTS/RENDER/homework/L02/homework_L02_001.hipnc

        file_prefix = file_type['prefix']
        file_name = self.file_name_template.format(file_prefix, shot_name, version, settings.HIP)
        file_path = '{0}/RENDER/{1}/{2}/{3}'.format(self.shot_root, sequence_name, shot_name, file_name)
        self.type = 'path'

        print 'build_path_asset_hip [file_path] = ', file_path

        self.set_path(file_path)

    # File version solver
    def version_control(self):
        '''
        Check if provided FILE (FOLDER) path exists.
            If not - return the same path.
            If exists - ask user save next version or overwrite. Return new path based on user decision
        '''

        if not os.path.exists(self.path):
            return self.path
        else:
            original_path = self.path
            self.build_latest_file_version()

            # Ask user which version to save
            answer = SNV(original_path.split('/')[-1], self.file_version).exec_()

            if answer == 2:  # Overwrite
                self.set_path(original_path)
                return original_path
            if answer == 3:  # Save latest version
                return self.path
