# Eve: Out of the box Houdini Pipeline
[![](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)


Restructured Eve pipeline for Houdini. 

Features:
 - Project Manager tool (Shotgun for beggars)  
 Here you can create projects with assets and shots, launch Houdini in a project context.
 [![](https://live.staticflickr.com/65535/49999218432_8c757dd65c_o.png)](https://live.staticflickr.com/65535/49999218432_8c757dd65c_o.png)
 
 - File paths management system for all Eve files  
 This module can create or read string file paths for any possible Eve file types.  
 E.g. `D:/PROJECTS/Inception/PROD/3D/scenes/SHOTS/RENDER/cafe/destruction/destruction_001.hip` 


You need to have Python 2.7 with PySide2 in C:/Python27.  
[Get Python with PySide2](https://drive.google.com/open?id=1jC4x2-Dcf5saixe9Z5aBu-kIMMaGEmtJ)

Release structure for Eve:  
  
 - Eve (root pipeline folder)  
    - project_manager.bat  
    - data (database file)  
    - tools (pipeline tools)  
        - core (common modules)  
        - houdini (houdini tools)  
        - nuke (nuke tools)  
        - pm (Project Manager)  
              
              
Download release, extract to the temp folder, copy Eve folder from Eve-0.0 to the network drive.