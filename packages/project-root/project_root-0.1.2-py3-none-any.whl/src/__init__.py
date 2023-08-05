import os
import sys

project_root = os.environ.get('project_root')
if project_root is not None and project_root not in sys.path:  
    package_absolute_path = os.path.abspath(__name__)
    if not package_absolute_path.startswith(project_root):
    	print('possible security vulnerability - project root not added to path')
        print(f'project root: {project_root} not part of the package absolute path({package_absolute_path})')
    else:
        sys.path.append(project_root)

