# Flaskinator
 Library to simply generate ready to use APIs and response models for Flask ecosystem
 
### For installation:
 
 pip install flaskinator
 
### Usage:
 ```
 from flaskinator import FlaskApiGenerator
 api_generator = FlaskApiGenerator()
 
 #filename => controller file name which should contain all the APIs
 #fileLocation => The directory where the controller file and the modules should be stored
 #apis => List of the APIs to be generated. For more reference see the 'samples' folder
 api_generator.createControllerFile(filename, fileLocation, apis)
 ```
