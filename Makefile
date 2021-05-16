black:
	python -m black .

gitall:
	git add .
	echo 'Enter the commit message:'
	read commitMessage
	git commit -m "$commitMessage"
	git push

export_requirements:
	conda list --export > requirements.txt

install_requirements:
	conda install --file requirements.txt

notebook_memory_usage:
	conda install -c conda-forge jupyter-resource-usage


install_some_packages:
	conda install pip
	pip install jedi==0.17.2

run_script:
	jupyter nbconvert --to script ExploratoryDataAnalysis.ipynb
	python ExploratoryDataAnalysis.py
