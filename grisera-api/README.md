# GRISERA API
Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) framework provides a persistent model for storing integrated signals and methods for its creation.

To upload new versions:
1. `python3 setup.py sdist bdist_wheel`
2. `twine upload dist/*`
   1. if you don't have twine installed then: `pip3 install twine`