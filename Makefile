black:
	python -m black .

gitall:
	git add .
	echo 'Enter the commit message:'
	read commitMessage
	git commit -m "$commitMessage"
	git push

make export_requirements:
	conda list --export > requirements.txt

make install_requirements:
	conda install --file requirements.txt

make notebook_memory_usage:
	conda install -c conda-forge jupyter-resource-usage


make install_some_packages:
	conda install pip
	pip install jedi==0.17.2

make run_script:
	jupyter nbconvert --to script ExploratoryDataAnalysis.ipynb
	python ExploratoryDataAnalysis.py
