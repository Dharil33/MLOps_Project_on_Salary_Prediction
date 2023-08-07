import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')

project_name = "MLOps_Project_on_Salary_Prediction"

list_of_files = [
    ".github/workflow/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/pipeline/predict_pipeline.py",
    f"src/{project_name}/pipeline/train_pipeline.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/exception.py",
    f"src/{project_name}/logger.py",
    "config/__init__.py",
    "config/config.yaml",
    "Dockerfile",
    "app.py",
    "research/trials.ipynb",
    "params.yaml",
    "templates/index.html"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)
    
    if filedir != '':
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")
        
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists")