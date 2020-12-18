import os, json
from jinja2 import Environment, FileSystemLoader
import jinja2

# where to look for template files 
file_loader = FileSystemLoader('templates')

# list json resume files from json_resumes directory
resume_files = os.listdir('json_resumes')

# list template file names in templates directory
template_files = os.listdir('templates')

# create the Environment object with the given loader
# one for .tex template, with << >> variable delimiters
# one for all other templates, with {{ }} variable delimiters
# make environment "strict" on undefined variables, i.e. crash if undefined variables found
tex_env = Environment(loader=file_loader, \
    trim_blocks=True, lstrip_blocks=True, undefined=jinja2.StrictUndefined, \
    variable_start_string="<<", variable_end_string=">>")

env = Environment(loader=file_loader,\
    trim_blocks=True, lstrip_blocks=True, undefined=jinja2.StrictUndefined)

# make template objects from templates,
# store them as a list of tuples with file extension also
def get_templates():
    templates = []
    for template_file in template_files:
        name, extension = os.path.splitext(template_file)
        if extension == ".tex":
            template = tex_env.get_template(template_file)
        else:
            template = env.get_template(template_file)
        templates.append((template, extension, name))
    return templates

# get resume file names, make folders for each resume
# store (resume_dict, resume_file_name, resume_file_name.json) as a triple
def get_resumes():
    resumes = []
    for resume_file in resume_files:
        with open("resumes/resume_file", "r") as f:
            resume_dict = json.load(f)
        name, _ = os.path.splitext(resume_file)
        resumes.append((resume_dict, resume_file, name))

        # make a directory for the resume if there isn't already one
        if name not in os.listdir("resumes"):
            os.mkdir("resumes/" + name)
    return resumes

# make and compile the resumes
for template_triple in get_templates():
    template, extension, name = template_triple

    for resume_triple in get_resumes():

        resume_dict, file_name, file_dir = resume_triple

        # make the file path
        file_path = "./resumes/" + file_dir + "/" + file_name + extension

        print("Writing " + file_name + extension + "...")

        # write the output file
        template.stream(resume_type=resume_dict).dump(file_path)

        # if the template is .tex, compile the tex file
        if extension == ".tex":
            # continue
            compile_command = 'pdflatex --output-directory ' + "./resumes/" + file_dir + " " + file_path
            os.system(compile_command)
