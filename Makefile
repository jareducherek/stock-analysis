.PHONY: requirements

PROJECT_NAME=stock-analysis

create_environment:
	conda create --yes --name $(PROJECT_NAME)

requirements:
	pip install -r requirements.txt
	python -m pip install "pymongo[srv]"
	conda install -y jupyter
	python -m ipykernel install --user
	python -m ipykernel install --user --name $(PROJECT_NAME) --display-name "$(PROJECT_NAME)"
