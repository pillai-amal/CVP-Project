import os

models = ["airplane.obj"]
for model in models:
    filepath = os.path.join(os.path.dirname(__file__), model)
    print("Importing:", filepath)