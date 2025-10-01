import os, shutil, re

print("Searching for Dependencies")

basic_setup = """from Dependencies.engine_core import *
from Dependencies.scene_manager import SceneManager
from Dependencies.camera import Camera

engine = EngineCore()

cam = Camera(vec2(0,0), 1)
engine.add_camera(cam)

scene_manager = SceneManager(engine)
scene_manager.load()

while engine.looping:
    cam.update()
    engine.main_loop()"""

print("Generating Builds Folder")
if not os.path.exists("Builds"):
    os.mkdir("Builds")

print("Generating Dependencies")
if not os.path.exists("Builds/Dependencies"):
    os.mkdir("Builds/Dependencies")

print("Generating Build File")
with open("Builds/build.py", "w") as build:
    build.writelines(basic_setup)

def find_dependencies(string_to_search):
    potential_dependencies = [f for f in os.listdir('.') if f.endswith('.py')]

    dependencies = []

    for line in string_to_search.splitlines():
        line = line.strip()
        if line.startswith("import "):
            print("Found import statement")
            dependency = line.split(" ")[1]
            dependencies.append(dependency)

        elif line.startswith("from "):
            print("Found from statement")
            dependency = line.split(" ")[1]
            if "." in dependency:
                parts = dependency.split(".")
                dependency = parts[1]
            dependencies.append(dependency)

        if len(dependencies) == 0:
            continue

        if not f"{dependencies[-1]}.py" in potential_dependencies:
            print(f"Dependency {dependencies[-1]} not found in root directory")
            dependencies.pop()

    return dependencies

def recursive_search(starting_file):
    dependencies = []
    searched_files = []

    files_to_search = [starting_file]

    while files_to_search:
        current_file = files_to_search.pop()
        print(f"Searching {current_file}")
        if current_file in searched_files:
            continue

        searched_files.append(current_file)

        if not os.path.exists(current_file):
            continue

        with open(current_file, 'r') as f:
            content = f.read()

        found_deps = find_dependencies(content)

        for dep in found_deps:
            dep_file = f"{dep}.py"
            if dep_file not in searched_files and dep_file not in files_to_search:
                files_to_search.append(dep_file)
            if dep not in dependencies:
                dependencies.append(dep)

    return dependencies

os.mkdir("temp")
with open("temp/temp_basic.py", "w") as temp:
    temp.writelines(basic_setup)

dependencies = recursive_search("temp/temp_basic.py")
print(f"Found Dependencies: {dependencies}")
shutil.rmtree("temp")

for dependency in dependencies:
    shutil.copy(f"{dependency}.py", "Builds/Dependencies")
    print(f"Copied {dependency}.py to Builds/Dependencies")

for dependency in dependencies:
    src_file = f"{dependency}.py"
    dst_file = f"Builds/Dependencies/{dependency}.py"
    shutil.copy(src_file, dst_file)
    print(f"Copied {dependency}.py to Builds/Dependencies")

    with open(dst_file, 'r') as f:
        content = f.readlines()

    new_content = []
    import_pattern = re.compile(r'^(from|import) (\S+)')

    for line in content:
        stripped = line.strip()
        match = import_pattern.match(stripped)
        if match:
            keyword, module = match.groups()
            first_module_part = module.split('.')[0]

            if first_module_part in dependencies and not module.startswith("Dependencies."):
                parts = module.split('.')
                parts[0] = "Dependencies." + parts[0]
                new_module = '.'.join(parts)
                line = line.replace(module, new_module, 1)

        new_content.append(line)

    with open(dst_file, 'w') as f:
        f.writelines(new_content)