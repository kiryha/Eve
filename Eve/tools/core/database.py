import sqlite3

# Project resolution (width + height) - global resolution for all shots.
# If SHOT has resolution - it is override for global resolution


def init_database(connection, cursor):
    """
    Create database tables
    :return:
    """

    # TYPES
    cursor.execute('''CREATE TABLE asset_types (
                    id integer primary key autoincrement,
                    name text,
                    description text
                    )''')

    cursor.execute('''CREATE TABLE file_types (
                    id integer primary key autoincrement,
                    name text,
                    description text
                    )''')

    # MAIN ITEMS
    cursor.execute('''CREATE TABLE projects (
                    id integer primary key autoincrement,
                    name text,
                    houdini_build text,
                    width integer,
                    height integer,
                    description text
                    )''')

    cursor.execute('''CREATE TABLE assets (
                    id integer primary key autoincrement,
                    name text,
                    project integer,
                    type integer,
                    description text,
                    FOREIGN KEY(project) REFERENCES projects(id)
                    FOREIGN KEY(type) REFERENCES asset_types(id)
                    )''')

    cursor.execute('''CREATE TABLE sequences (
                    id integer primary key autoincrement,
                    name text,
                    project integer,
                    description text,
                    FOREIGN KEY(project) REFERENCES projects(id)
                    )''')

    cursor.execute('''CREATE TABLE shots (
                    id integer primary key autoincrement,
                    name text,
                    sequence integer,
                    start_frame integer,
                    end_frame integer,
                    width integer, 
                    height integer,
                    description text,
                    FOREIGN KEY(sequence) REFERENCES sequences(id)
                    )''')

    # FILES
    cursor.execute('''CREATE TABLE asset_files (
                    id integer primary key autoincrement,
                    type integer,
                    asset integer,
                    snapshot integer,
                    description text,
                    FOREIGN KEY(type) REFERENCES file_types(id)
                    FOREIGN KEY(asset) REFERENCES assets(id)
                    FOREIGN KEY(snapshot) REFERENCES asset_snapshots(id)
                    )''')

    cursor.execute('''CREATE TABLE shot_files (
                    id integer primary key autoincrement,
                    type integer,
                    shot integer,
                    snapshot integer,
                    description text,
                    FOREIGN KEY(type) REFERENCES file_types(id)
                    FOREIGN KEY(shot) REFERENCES shots(id)
                    FOREIGN KEY(snapshot) REFERENCES shot_snapshots(id)
                    )''')

    # LINKS
    # Link assets to the shots
    cursor.execute('''CREATE TABLE shot_assets (
                    id integer primary key autoincrement,
                    shot_id integer,
                    asset_id integer,
                    FOREIGN KEY(shot_id) REFERENCES shots(id)
                    FOREIGN KEY(asset_id) REFERENCES assets(id)
                    )''')

    # SNAPSHOTS
    cursor.execute('''CREATE TABLE asset_snapshot (
                    id integer primary key autoincrement,
                    asset_name text,
                    asset_id text,
                    asset_version text,
                    description text
                    )''')

    connection.commit()


def init_asset_types(connection, cursor):
    """
    Fill asset types table in the DB (character, environment, prop, FX)

    :param connection:
    :param cursor:
    :return:
    """

    for name, data in Asset.asset_types.iteritems():
        cursor.execute("INSERT INTO asset_types VALUES ("
                       ":id,"
                       ":name,"
                       ":description)",

                       {'id': data['id'],
                        'name': name,
                        'description': data['description']})

    connection.commit()


def init_file_types(connection, cursor):
    """
    Fill file types table in the DB.

    Any file used in Eve should has a particular type. Here is the full list of all possible types in Eve.

    asset_hip:
        Working scene for Assets. Here we store all source data to build an asset. Results are exported as caches,
        and caches used in asset_hda files.

    asset_hda:
        Houdini Digital Asset for ASSETS. Used to load assets of any type (char, env, props, fx) into shots.
        Contain cached data with interface. Source of cached data is stored in asset_hip

    :param connection:
    :param cursor:
    :return:
    """

    for name, data in EveFile.file_types.iteritems():

        cursor.execute("INSERT INTO file_types VALUES ("
                       ":id,"
                       ":name,"
                       ":description)",

                       {'id': data['id'],
                        'name': name,
                        'description': data['description']})

    connection.commit()


def convert_to_project(project_tuples):
    """
    Convert list of projects tuples to list of Eve Project objects

    :param project_tuples: list of tuples, project data: [(id, name, houdini_build, width, height, description)]
    :return:
    """

    projects = []
    for project_tuple in project_tuples:
        project = Project(project_tuple[1])
        project.id = project_tuple[0]
        project.houdini_build = project_tuple[2]
        project.width = project_tuple[3]
        project.height = project_tuple[4]
        project.description = project_tuple[5]
        projects.append(project)

    return projects


def convert_to_asset(asset_tuples):
    """
    Convert list of assets tuples to list of athena Asset objects
    :param asset_tuples:  [(id, name, project, type, description)]
    :return:
    """

    assets = []

    for asset_tuple in asset_tuples:
        asset = Asset(asset_tuple[1], asset_tuple[2])
        asset.id = asset_tuple[0]
        asset.type = asset_tuple[3]
        asset.description = asset_tuple[4]
        assets.append(asset)

    return assets


def convert_to_sequence(sequence_tuples):
    """
    Convert list of sequence tuples to list of athena Sequence objects
    :param sequence_tuples:  [(id, name, project, description)]
    :return:
    """

    sequences = []

    for sequence_tuple in sequence_tuples:
        sequence = Sequence(sequence_tuple[1], sequence_tuple[2])
        sequence.id = sequence_tuple[0]
        sequence.description = sequence_tuple[3]
        sequences.append(sequence)

    return sequences


def convert_to_shot(shot_tuples):
    """
    Convert list of shot tuples to list of athena Shot objects
    :param shot_tuples:  [(id, name, sequence, start_frame, end_frame, width, height, description)]
    :return:
    """

    shots = []

    for shot_tuple in shot_tuples:
        shot = Shot(shot_tuple[1], shot_tuple[2])
        shot.id = shot_tuple[0]
        shot.start_frame = shot_tuple[3]
        shot.end_frame = shot_tuple[4]
        shot.width = shot_tuple[5]
        shot.height = shot_tuple[6]
        shot.description = shot_tuple[7]
        shots.append(shot)

    return shots


def convert_to_asset_types(asset_types_tuples):
    """
    Convert list of asset types tuples to list of Eve AssetType objects
    :param asset_types_tuples: list of tuples, asset type data: [(id, name, description)]
    :return:
    """

    asset_types = []
    for asset_types_tuple in asset_types_tuples:
        asset_type = AssetType(asset_types_tuple[0], asset_types_tuple[1], asset_types_tuple[2])
        asset_types.append(asset_type)

    return asset_types


class Project:
    def __init__(self, project_name):
        self.id = None
        self.name = project_name
        self.houdini_build = ''
        self.width = ''
        self.height = ''
        self.description = ''


class Asset:

    asset_types = {
        'character':
            {'id': 1,
             'name': 'character',
             'description': 'Character asset'},

        'environment':
            {'id': 2,
             'name': 'environment',
             'description': 'Environment asset'},

        'prop':
            {'id': 3,
             'name': 'prop',
             'description': 'Animated asset with rig'},

        'static':
            {'id': 4,
             'name': 'static',
             'description': 'Non animated asset'},

        'fx':
            {'id': 5,
             'name': 'fx',
             'description': 'FX asset'}}

    def __init__(self, asset_name, project_id):
        self.id = None
        self.name = asset_name
        self.project = project_id
        self.type = None
        self.description = ''


class Sequence:
    def __init__(self, sequence_name, project_id):
        self.id = None
        self.name = sequence_name
        self.project = project_id
        self.description = ''


class Shot:
    def __init__(self, shot_name, sequence_id):
        self.id = None
        self.name = shot_name
        self.sequence = sequence_id
        self.start_frame = ''
        self.end_frame = ''
        self.width = ''
        self.height = ''
        self.description = ''


class AssetType:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


class EveFile:

    file_types = {
        'asset_hip':
            {'id': 1,
             'name': 'asset_hip',
             'prefix': '',
             'description': 'Houdini working scene for assets'},

        'asset_hda':
            {'id': 2,
             'name': 'asset_hda',
             'prefix': '',
             'description': 'Houdini digital asset for assets'},

        'asset_fx':
            {'id': 3,
             'name': 'asset_hip',
             'prefix': '',
             'description': ''},

        'shot_animation':
            {'id': 4,
             'name': 'asset_hip',
             'prefix': '',
             'description': ''},

        'shot_render':
            {'id': 5,
             'name': 'asset_hip',
             'prefix': '',
             'description': ''},

        'shot_fx':
            {'id': 6,
             'name': 'asset_hip',
             'prefix': '',
             'description': 'Houdini working scene for assets.'}}

    def __init__(self, file_type_id, source_id):
        self.id = None
        self.type = file_type_id
        self.source = source_id  # Source DB item id (asset, shot etc)
        self.snapshot = None
        self.description = ''


class EveData:
    def __init__(self, SQL_FILE_PATH):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH

        # Data attributes
        # INTERNAL SET
        self.projects = []
        self.project_assets = []
        self.asset_types = []
        self.project_sequences = []
        self.sequence_shots = []
        # EXTERNAL SET
        self.selected_project = None
        self.selected_asset = None
        self.selected_sequences = None
        self.selected_shot = None
        self.linked_assets = None
        self.asset_type_string = None

        # Initialize data
        self.init_data()

    # UI
    def init_data(self):
        """
        Populate data when create a EveData instance
        """

        self.get_projects()
        self.get_asset_types()

    # CRUD
    # Project
    def add_project(self, project):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        # Add project to DB
        cursor.execute("INSERT INTO projects VALUES ("
                       ":id,"
                       ":name,"
                       ":houdini_build,"
                       ":width,"
                       ":height,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': project.name,
                        'houdini_build': project.houdini_build,
                        'width': project.width,
                        'height': project.height,
                        'description': project.description})

        connection.commit()
        project.id = cursor.lastrowid  # Add database ID to the project object
        connection.close()

        # Add project to data instance
        self.projects.append(project)

    def get_project(self, project_id):
        """ Get project by id """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects WHERE id=:id",
                       {'id': project_id})
        project_tuple = cursor.fetchone()
        project_object = convert_to_project([project_tuple])[0]

        connection.close()

        if project_object:
            return project_object

    def get_project_by_name(self, project_name):
        """ Get project by id """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects WHERE name=:name",
                       {'name': project_name})
        project_tuple = cursor.fetchone()
        project_object = convert_to_project([project_tuple])[0]

        connection.close()

        if project_object:
            return project_object

    def get_projects(self):
        """ Get all project items from projects table in db """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects")
        project_tuples = cursor.fetchall()
        project_objects = convert_to_project(project_tuples)

        connection.close()

        self.projects.extend(project_objects)

    def get_project_assets(self, project):
        """ Get all project assets from assets table in db """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE project=:project",
                       {'project': project.id})

        asset_tuples = cursor.fetchall()
        asset_objects = convert_to_asset(asset_tuples)

        connection.close()

        # Clear list and append assets
        del self.project_assets[:]
        for asset in asset_objects:
            self.project_assets.append(asset)

    def get_project_sequences(self, project):
        """ Get all project sequences from sequences table in db """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sequences WHERE project=:project",
                       {'project': project.id})

        sequence_tuples = cursor.fetchall()
        sequence_objects = convert_to_sequence(sequence_tuples)

        connection.close()

        # Clear list and append assets
        del self.project_sequences[:]
        for sequence in sequence_objects:
            self.project_sequences.append(sequence)

    def get_sequence_shots(self, sequence_id):
        """
        Get all sequence shots from shots table in db
        """

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM shots WHERE sequence=:sequence",
                       {'sequence': sequence_id})

        shot_tuples = cursor.fetchall()
        shot_objects = convert_to_shot(shot_tuples)

        connection.close()

        # Clear list and append assets
        del self.sequence_shots[:]
        for shot in shot_objects:
            self.sequence_shots.append(shot)

    def update_project(self, project):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE projects SET "
                       "houdini_build=:houdini_build,"
                       "width=:width,"
                       "height=:height,"
                       "description=:description "

                       "WHERE id=:id",

                       {'id': project.id,
                        'houdini_build': project.houdini_build,
                        'width': project.width,
                        'height': project.height,
                        'description': project.description})

        connection.commit()
        connection.close()

        self.selected_project = project

    def del_project(self, project_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM projects WHERE id=:id",
                       {'id': project_id})

        connection.commit()
        connection.close()

        for project in self.projects:
            if project.id == project_id:
                self.projects.remove(project)

    # Assets
    def add_asset(self, asset, project_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO assets VALUES ("
                       ":id,"
                       ":name,"
                       ":project,"
                       ":type,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': asset.name,
                        'project': project_id,
                        'type': asset.type,
                        'description': asset.description})

        connection.commit()
        asset.id = cursor.lastrowid  # Add database ID to the asset object
        connection.close()

        self.project_assets.append(asset)

    def get_asset(self, asset_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE id=:id",
                       {'id': asset_id})

        asset_tuple = cursor.fetchone()

        connection.close()

        if asset_tuple:
            return convert_to_asset([asset_tuple])[0]

    def get_asset_by_name(self, project_id, asset_name):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM assets WHERE "
                       "name=:name "
                       "AND project=:project",

                       {'name': asset_name,
                        'project': project_id})

        asset_tuple = cursor.fetchone()

        connection.close()

        if asset_tuple:
            return convert_to_asset([asset_tuple])[0]

    def get_asset_types(self):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM asset_types")
        asset_types_tuples = cursor.fetchall()
        asset_types_objects = convert_to_asset_types(asset_types_tuples)

        connection.close()

        self.asset_types.extend(asset_types_objects)

    def get_asset_type_string(self, asset_type_id):
        """
        Get asset type name by asset type id in Asset.asset_types dictionary
        :return:
        """

        for name, data in Asset.asset_types.iteritems():
            if data['id'] == asset_type_id:
                self.asset_type_string = name

    def update_asset(self, asset):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE assets SET "
                       "project=:project,"
                       "type=:type,"
                       "description=:description "

                       "WHERE id=:id",

                       {'id': asset.id,
                        'project': asset.project,
                        'type': asset.type,
                        'description': asset.description})

        connection.commit()
        connection.close()

        self.selected_asset = asset

    def link_asset(self, asset_id, shot_id):
        """
        Link asset to the shot
        :param asset_id:
        :param shot_id:
        :return:
        """

        pass

    def del_asset(self, asset_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM assets WHERE id=:id",
                       {'id': asset_id})

        connection.commit()
        connection.close()

        for asset in self.project_assets:
            if asset.id == asset_id:
                self.project_assets.remove(asset)

    # Sequence
    def add_sequence(self, sequence, project_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO sequences VALUES ("
                       ":id,"
                       ":name,"
                       ":project,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': sequence.name,
                        'project': project_id,
                        'description': sequence.description})

        connection.commit()
        sequence.id = cursor.lastrowid  # Add database ID to the sequence object
        connection.close()

        self.project_sequences.append(sequence)

    def get_sequence(self, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sequences WHERE id=:id",
                       {'id': sequence_id})

        sequence_tuple = cursor.fetchone()

        connection.close()

        if sequence_tuple:
            return convert_to_sequence([sequence_tuple])[0]

    def update_sequence(self, sequence):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE sequences SET "
                       "description=:description "

                       "WHERE id=:id",

                       {'id': sequence.id,
                        'description': sequence.description})

        connection.commit()
        connection.close()

        self.selected_sequences = sequence

    def del_sequence(self, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM sequences WHERE id=:id",
                       {'id': sequence_id})

        connection.commit()
        connection.close()

        for sequence in self.project_sequences:
            if sequence.id == sequence_id:
                self.project_sequences.remove(sequence)

    # Shot
    def add_shot(self, shot, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO shots VALUES ("
                       ":id,"
                       ":name,"
                       ":sequence,"
                       ":start_frame,"
                       ":end_frame,"
                       ":width,"
                       ":height,"
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': shot.name,
                        'sequence': sequence_id,
                        'start_frame': shot.start_frame,
                        'end_frame': shot.end_frame,
                        'width': shot.width,
                        'height': shot.height,
                        'description': shot.description})

        connection.commit()
        shot.id = cursor.lastrowid  # Add database ID to the shot object
        connection.close()

        self.sequence_shots.append(shot)

    def get_shot(self, sequence_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM shots WHERE id=:id",
                       {'id': sequence_id})

        shot_tuple = cursor.fetchone()

        connection.close()

        if shot_tuple:
            return convert_to_shot([shot_tuple])[0]

    def update_shot(self, shot):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("UPDATE shots SET "
                       "sequence=:sequence,"
                       "start_frame=:start_frame,"
                       "end_frame=:end_frame,"
                       "width=:width,"
                       "height=:height,"
                       "description=:description "

                       "WHERE id=:id",

                       {'id': shot.id,
                        'sequence': shot.sequence,
                        'start_frame': shot.start_frame,
                        'end_frame': shot.end_frame,
                        'width': shot.width,
                        'height': shot.height,
                        'description': shot.description})

        connection.commit()
        connection.close()

        self.selected_shot = shot

    def del_shot(self, shot_id):

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM shots WHERE id=:id",
                       {'id': shot_id})

        connection.commit()
        connection.close()

        for shot in self.sequence_shots:
            if shot.id == shot_id:
                self.sequence_shots.remove(shot)