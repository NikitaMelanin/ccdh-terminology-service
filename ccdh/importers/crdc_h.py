import logging
from typing import Dict
import requests
from googleapiclient.discovery import build
from linkml.loaders import yaml_loader
from linkml.utils.yamlutils import YAMLRoot

from ccdh.config import get_settings


def read_ccdh_model_yaml():
    branch = get_settings().ccdhmodel_branch
    yaml_url = f'https://raw.githubusercontent.com/cancerDHC/ccdhmodel/{branch}/src/schema/ccdhmodel.yaml'
    r = requests.get(yaml_url)
    if r.status_code == 200:
        return r.content
    else:
        raise ValueError('Failed to fetch yaml from ' + yaml_url)


class CrdcHImporter:
    def __init__(self):
        pass

    @staticmethod
    def read_harmonized_attributes(yaml: str = read_ccdh_model_yaml()) -> Dict:
        """
        Extract the attributes from the ccdhmodel YAML
        :param yaml:
        :return: a dictionary of the attributes.
        """
        model = yaml_loader.loads(yaml, target_class=YAMLRoot)
        harmonized_attributes = {}
        for cls in model.classes.values():
            for attribute in cls.get('attributes', {}).values():
                if attribute['range'] == 'CodeableConcept':
                    key = f'{model.name}.{cls["name"]}.{attribute["name"]}'
                    harmonized_attribute = {
                        'system': model.name, 'entity': cls["name"], 'attribute': attribute["name"],
                        'definition': attribute["description"], 'node_attributes': []
                    }
                    if "related_mappings" in attribute:
                        for m in attribute["related_mappings"]:
                            harmonized_attribute['node_attributes'].append(m)
                    harmonized_attributes[key] = harmonized_attribute
        return harmonized_attributes
