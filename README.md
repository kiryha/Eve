# Eve: Out of the box Houdini Pipeline
[![](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)](https://live.staticflickr.com/65535/48087908673_fb38ed89fe_o.jpg)


Restructured Eve pipeline for Houdini. 

### Features:
#### Project Manager tool

Here you can create projects with assets and shots, launch Houdini in a project context.
[![](https://live.staticflickr.com/65535/49999218432_8c757dd65c_o.png)](https://live.staticflickr.com/65535/49999218432_8c757dd65c_o.png)
 
#### File paths management system for all Eve files  
This module can create or read string file paths for any possible Eve file types.  
E.g. `D:/PROJECTS/Inception/PROD/3D/scenes/SHOTS/RENDER/cafe/destruction/destruction_001.hip` 

You need to have Python 2.7 with PySide2 in C:/Python27.  
[Get Python with PySide2](https://drive.google.com/open?id=1jC4x2-Dcf5saixe9Z5aBu-kIMMaGEmtJ)

### Learning database
Attempt to make first steps with Houdini, Programming or Math? In addition to `Eve` specific materials, we have plenty of Houdini tutorials! 

The best places to start with VEX and Python:
- [VEX for artists](https://github.com/kiryha/Houdini/wiki/vex-for-artists)  
- [Python for artists](https://github.com/kiryha/Houdini/wiki//python-for-artists)

Don't miss [Programming basics](https://github.com/kiryha/Houdini/wiki//programming-basics) if you don't have programming experience!

Applied Python in Houdini: [Python snippets](https://github.com/kiryha/Houdini/wiki/python-snippets)  
Applied VEX: [VEX snippets](https://github.com/kiryha/Houdini/wiki//vex-snippets)   
Small solutions as a HIP files: [HIP Examples](https://github.com/kiryha/Houdini/wiki//examples)

### Release structure for Eve:  
  
 - Eve (root pipeline folder)  
    - project_manager.bat  
    - data (database file)  
    - tools (pipeline tools)  
        - core (common modules)  
        - houdini (houdini tools)  
        - nuke (nuke tools)  
        - pm (Project Manager)  
              
              
Download release, extract to the temp folder, copy Eve folder from Eve-0.0 to the network drive.