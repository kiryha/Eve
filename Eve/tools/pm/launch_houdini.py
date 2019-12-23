import os
import subprocess

def get_HDA(root_3d):
    '''
    Build HOUDINI_OTLSCAN_PATH env variable value:
    Get all subfolders of HDA location dirs (hda and lib/materials) and combine to one string
    Used by Houdini to search for HDA (Houdini Digital Assets)
    '''

    filterFolders = ['backup']


    def combinePaths(listPaths):
        '''
        Combine paths string from list of paths
        :param listPaths: list of subfolders in processed folder
        '''

        pathHDA = ''

        for folder in listPaths:
            path = folder[0].replace('\\', '/')
            # Filter unnecessary folders
            if not path.split('/')[-1] in filterFolders:
                pathHDA += '{};'.format(folder[0].replace('\\', '/'))

        return pathHDA

    # Get list of sub folders
    listPaths_HDA = os.walk('{0}/hda'.format(root_3d)) # HDA
    # listPaths_MTL = os.walk('{0}/lib/MATERIALS'.format(root3D))  # Material library
    # listPaths_LIT = os.walk('{0}/lib/LIGHTS'.format(root3D))  # Light library

    # Global HDA library path (WIP! TBD!)
    listPaths_LIB = os.walk('')  # Global HDA (between projects)

    # Combine paths to a string
    pathHDA = combinePaths(listPaths_HDA)
    # combinePaths(listPaths_MTL)
    # combinePaths(listPaths_LIT)
    # combinePaths(listPaths_LIB)

    # Add Houdini standard OTLs
    pathHDA = pathHDA + '&'

    return pathHDA

def run(eve_root, projects_root, HOUDINI, project_name):


    print eve_root, projects_root, HOUDINI, project_name

    # SETUP PROJECT ENVIRONMENT
    root_3d = '{0}/{1}/PROD/3D'.format(projects_root, project_name)
    project_root = '{0}/{1}'.format(projects_root, project_name)
    # Eve location ('E:/Eve')
    os.environ['EVE_ROOT'] = '{0}'.format(eve_root)
    # Project Root folder ('E:/projects/<project_name>')
    os.environ['AT_PROJECT'] = project_root
    # Project Name
    os.environ['AT_PROJECT_NAME'] = '{0}'.format(project_name)
    # Root of houdini project
    os.environ['JOB'] = root_3d

    # Houdini digital assets folder including sub folders
    # os.environ['HOUDINI_OTLSCAN_PATH'] = get_HDA(root_3d)
    # Houdini path
    os.environ['HOUDINI_PATH'] = '{0}/tools/houdini/settings;&'.format(eve_root)
    # Path to custom python tools
    os.environ['PYTHONPATH'] = '{0}/dna;{0}/tools;&'.format(eve_root)  ### !!!!!!!!!!!!!!!!!!!!!!!!!!! WIP

    # Icons
    # os.environ['HOUDINI_UI_ICON_PATH'] = '{}/EVE/icons'.format(rootPipeline)
    # Houdini current user pref folder in MyDocuments (win)
    # os.environ['home'] = '{}/Documents/houdiniUserPrefs'.format(os.path.expanduser("~"))

    # Setup Redshift
    # os.environ['HOUDINI_DSO_ERROR'] = '2'
    # os.environ['PATH'] += ';' + 'C:/ProgramData/Redshift/bin;$PATH'
    # os.environ['HOUDINI_PATH'] = 'C:/ProgramData/Redshift/Plugins/Houdini/{0};{1}'.format(build, os.environ['HOUDINI_PATH'])

    subprocess.Popen(HOUDINI)

    # Prevent closing CMD window
    # raw_input()
