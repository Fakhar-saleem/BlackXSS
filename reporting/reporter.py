
import os
import json
from jinja2 import Environment, FileSystemLoader
from config.settings import REPORT_TEMPLATE_DIR, EXPORT_JSON, EXPORT_CSV
from utils.logger import log

class Reporter:
    def __init__(self, template=None):
        template_name = template or os.getenv('BXXS_TEMPLATE', None)
        self.env = Environment(loader=FileSystemLoader(REPORT_TEMPLATE_DIR))
        self.template = self.env.get_template(template_name)

    def generate(self, results, output_path):
        """
        Render the HTML report and optionally export JSON/CSV.
        - results: list of finding dicts
        - output_path: path to write the .html report
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        # Render HTML
        html_content = self.template.render(results=results)
        with open(output_path, 'w') as f:
            f.write(html_content)
        log(f"[REPORT] HTML report saved to {output_path}")

        # Export JSON
        if EXPORT_JSON:
            json_path = output_path.replace('.html', '.json')
            with open(json_path, 'w') as jf:
                json.dump(results, jf, indent=2)
            log(f"[REPORT] JSON report saved to {json_path}")

        # Export CSV if enabled
        if EXPORT_CSV:
            import csv
            csv_path = output_path.replace('.html', '.csv')
            keys = results[0].keys() if results else []
            with open(csv_path, 'w', newline='') as cf:
                writer = csv.DictWriter(cf, fieldnames=keys)
                writer.writeheader()
                writer.writerows(results)
            log(f"[REPORT] CSV report saved to {csv_path}")
