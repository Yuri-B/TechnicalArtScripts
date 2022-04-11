README
Current version: 0.5 ( BETA ) 

**&*^&*(^(&* <<<  GENERAL INFO  >>> **&*^&*(^(&*

See the script in action here, to find out how it is used: https://www.artstation.com/artwork/B3ne39

This script allows users to create broken apart or exploded views of an assembly of objects, without changing the original transform coordinates of each object. The script creates a Master controller whose position and rotation move and rotate all the slave controls that are attached to it.

LIMITATIONS:
- the model's centre has to be placed at (0,0,0) coordinate in the viewport, to get the best results.  

FUTURE FEATURES:
- make exploded views work relative to any selected object or group

//////////////////////

Important procedure to activate script:

1.) Open directory "PRODUCTION_CODE"
2.) Copy all the files into the relevant maya scripts folder
3.) Inside scripts folder, open the file "ExplodedViewer_Interface_Production.py"
4.) Under the comment "# ()()()() INSERT YOUR WORKING MAYA SCRIPTS DIRECTORY HERE ()()()()",
edit the folder path of scripts file, in the format that Maya recognises

To run the script : 
5.) Open Maya
6.) Launch script editor. Create a Python tab in the script editor
7.) Drag the script file "ExplodedViewer_Interface_Production.py" into the script editor. Optionally, save it to Maya shelf
8.) Run the script


