import os
import shutil
import argparse

__version__ = '1.0.6'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", help="create a project")
    parser.add_argument("name", help="project name")
    return parser.parse_args()


def dist_dir_check(dist_dir):
    if not os.path.exists(dist_dir):
        return True
    elif os.path.isfile(dist_dir):
        return False
    else:
        if os.listdir(dist_dir):
            return False
        else:
            return True


def format_dir(root, project_name):
    os.rename(os.path.join(root, 'project_name'), os.path.join(root, project_name))
    for fl in os.walk(root):
        dir, sub_dir, files = fl
        for file in files:
            if not file.endswith('.py'):
                continue
            fp = os.path.join(dir, file)
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
                content = content.replace("{% project_name %}", project_name)
                # print(content)
                with open(f'{fp}.bak', 'w', encoding='utf-8') as f:
                    f.write(content)

            os.remove(fp)
            os.rename(f'{fp}.bak', fp)


def main():
    args = parse_args()
    if args.cmd == 'create':
        project_name = args.name
        print(f'Will create Flask project with name "{project_name}"')
        dir_name = os.path.dirname(__file__)
        source_dir = os.path.join(dir_name, 'templates', 'project_template', project_name)
        dist_dir = os.path.join(os.getcwd(), args.name)
        if dist_dir_check(dist_dir, ):
            shutil.copytree(source_dir, dist_dir,
                            ignore=lambda src, names: [name for name in names if name == '__pycache__'])
            format_dir(dist_dir, args.name)
            print(f'Create project at {dist_dir} Success!')
        else:
            print(f'The directory {dist_dir} was not empty, Can\'t create project.')
