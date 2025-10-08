# Access the modules in the engine
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Init function called once at the beginning
def init(obj, engine):
    pass

# Update function called every frame
def update(obj, engine):
    pass