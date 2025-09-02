"""Generate HTML and JSON reports using Jinja2"""
from jinja2 import Environment, FileSystemLoader
import json

class Reporter:
    def __init__(self, template='report.html.j2'):
        self.env = Environment(loader=FileSystemLoader('reporting/templates'))
        self.template = self.env.get_template(template)

    def generate(self, results, output_path):
        html = self.template.render(results=results)
        with open(output_path, 'w') as f:
            f.write(html)
        with open(output_path.replace('.html','.json'), 'w') as jf:
            json.dump(results, jf, indent=2)
