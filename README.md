# script-generator
 
## Purpose
The aim of this code is to create a script for a short film that has 5 acts- an interesting hook for opening, a challenge, a climax, a resolution, and an ending. The output should also display the context that was gathered from Wikipedia while creating this script


## Steps to recreate
1. create a new conda environment: `conda create --name myenv`
2. activate the new env: `conda activate myenv`
3. run the app.py file: `python app.py`
4. install all the dependencies `pip install -r requirements.txt`
5. run the application with streamlit: `streamlit run app.py`

Note: You will have to update your OPEN AI API key in the apikey.py file before you run this code in your conda environment.


## Explanaiton of what's happening
Currently the project is still work in progress. The GPT was running out of memory and not completing the scripts. To solve for this, I'm using multiple API calls instead of trying to generate the entire script in a single API call. This is resulting in some convulated behavior which needs to be fixed.