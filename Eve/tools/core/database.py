import sqlite3


def init_database(connection, cursor):
    '''
    Create database tables
    :return:
    '''

    cursor.execute('''CREATE TABLE projects (
                    id integer primary key autoincrement,
                    name text,
                    houdini_build text,
                    description text
                    )''')

    # cursor.execute('''CREATE TABLE assets (
    #                 id integer primary key autoincrement,
    #                 name text,
    #                 project integer,
    #                 description text
    #                 )''')
    #
    # cursor.execute('''CREATE TABLE asset_publish (
    #                 id integer primary key autoincrement,
    #                 asset_name text,
    #                 asset_id text,
    #                 description text
    #                 )''')
    #
    #
    # cursor.execute('''CREATE TABLE shots (
    #                 id integer primary key autoincrement,
    #                 name text,
    #                 project integer,
    #                 linked_asset integer,
    #                 start_frame integer,
    #                 end_frame integer,
    #                 width integer,
    #                 height integer,
    #                 description text
    #                 )''')

    connection.commit()

def convert_to_project(project_tuples):
    '''
    Convert list of projects tuples to list of athena Project objects
    :param project_tuples: list of tuples, project data: [(id, name, houdini, description)]
    :return:
    '''

    projects = []
    for project_tuple in project_tuples:
        project = Project(project_tuple[1])
        project.id = project_tuple[0]
        project.houdini_build = project_tuple[2]
        project.description = project_tuple[3]
        projects.append(project)

    return projects

class Project:
    def __init__(self, project_name):
        self.id = None
        self.name = project_name
        self.houdini = ''
        self.description = ''


class Data:
    def __init__(self, SQL_FILE_PATH):
        # Load database
        self.SQL_FILE_PATH = SQL_FILE_PATH

        # Data attributes
        # INTERNAL SET
        self.projects = []
        self.project_assets = []
        self.project_sequences = []
        self.project_shots = []
        # EXTERNAL SET
        self.selected_project = None
        self.selected_asset = None
        self.selected_sequences = None
        self.selected_shot = None
        self.linked_asset = None

        # Initialize data
        self.init_data()

    # UI
    def init_data(self):
        ''' Populate data when create a Database instance '''

        self.get_projects()

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
                       ":description)",

                       {'id': cursor.lastrowid,
                        'name': project.name,
                        'houdini_build': project.houdini_build,
                        'description': project.description})

        connection.commit()
        project.id = cursor.lastrowid  # Add database ID to the project object
        connection.close()

        # Add project to data instance
        self.projects.append(project)

    def get_project(self, project_id):
        ''' Get project by id '''

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
        ''' Get project by id '''

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
        ''' Get all project items from projects table in db '''

        connection = sqlite3.connect(self.SQL_FILE_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM projects")
        project_tuples = cursor.fetchall()
        project_objects = convert_to_project(project_tuples)

        connection.close()

        self.projects.extend(project_objects)
