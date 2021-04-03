black:
	python -m black .

gitall:
	git add .
	git commit -m $$m
	git push
