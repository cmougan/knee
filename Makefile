black:
	python -m black .

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
	python ExploratoryDataAnalysis.py
	python Models.py
	python SportsAnalysis.py
gitall:
	git add .
	@read -p "Enter commit message: " message; 	git commit -m "$$message"
	git push

sum_hours:
	awk -F"," '{print;x+=$2}END{print "Total " x}' data/ecs.csv

sum_sport_hours:
	awk -F',' '{sum+=$5;}END{print sum;}' data/sport.csv




