### READDME - Data Science blueprint


## ROOT

# 1. CICD Azure DevOps yaml
 - Blueprint of CICD Azure Devops yaml

# 2. Connector module
 - Module to connect to a specific DSEE, Datalake and DSPE

# 3. Model metadata
 - Metadata which contains owner, data sources, use cases et cetera

# 4. Releasenotes
 - Releasenotes can be found within this directory

# 5. Pylint config
 - Blueprint of a Pylint configuration used within ABN Amro

# 6. MLFlow project
 - Blueprint of a MLFlow project which contains the ABN Amro template

# 7. Template scripts

	|- 7.01 ETL (including ingestion)
	  - Scripts regarding ETL processes are stored within this directory 

	|- 7.02 Feature engineering
	  - In this script feature engineering can be conducted

	|- 7.03 Training
	  - The train script(s) of the model

	|- 7.04 Predict / score
	  - Prediction or scoring scripts

	|- 7.05 Evaluation metrics
	  - Model specific evaluation metrics are stored here
	
	|- 7.06 Post processing
	  - After 'Predict / score' and 'Evaluation metrics' scripts are executed post processing 
	    may be conducted. For example to exclude a specific population from being processed 
	    in further stages

	|- 7.07 Export
	  - Export the model output to another pipeline. For example to make the model output 
	    available for endusers

	|- 7.08 Model monitoring
	  - Model monitoring contains all constructs to monitoring model use. For example 
	    amount of endusers, comparing performance to historical results et cetera

	|- 7.09 Model validation
	  - Scripts to validate the model and conduct final sanity checks

	|- 7.10 Serving
	  - Script regarding the serving of the model

	|- 7.11 Visualisation
	  - Scripts regarding visualizations of the model 


# 8. Artifacts

	|- 8.01 Docs
