# Dmitry Kisler © 2020
# www.dkisler.com

from copy import deepcopy
from typing import Union, Tuple, List
from collections import namedtuple
from google.cloud.bigquery import SchemaField
import fastjsonschema


gbq_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "required": [
            "name",
            "type",
        ],
        "properties": {
            "description": {
                "oneOf": [
                    {"type": "string"},
                    {"type": "null"},
                ],
            },
            "name": {
                "type": "string",
                "examples": [
                    "att1",
                ],
            },
            "type": {
                "type": "string",
                "enum": [
                    "INT",
                    "INTEGER",
                    "INT64",
                    "FLOAT",
                    "FLOAT64",
                    "NUMERIC",
                    "BOOL",
                    "BOOLEAN",
                    "STRING",
                    "BYTES",
                    "DATE",
                    "DATETIME",
                    "TIME",
                    "TIMESTAMP",
                    "RECORD",
                ],
            },
            "mode": {
                "oneOf": [
                    {
                        "type": "string",
                        "enum": [
                            "REQUIRED",
                            "NULLABLE"
                        ]
                    },
                    {
                        "type": "null",
                    },
                ],
            },
        },
        "additionalProperties": True,
    },
}

validate_json = fastjsonschema.compile(gbq_schema)

TEMPLATE = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "$ref": "#/definitions/element"
    },
    "definitions": {
        "element": {},
    },
}

MapTypes = namedtuple("map_types",
                      gbq_schema['items']['properties']['type']['enum'])

map_types = MapTypes(
    INT={"type": "integer"},
    INTEGER={"type": "integer"},
    INT64={"type": "integer"},
    FLOAT={"type": "number"},
    FLOAT64={"type": "number"},
    NUMERIC={"type": "number"},
    BOOL={"type": "boolean"},
    BOOLEAN={"type": "boolean"},
    STRING={"type": "string"},
    BYTES={"type": "string"},
    DATE={"type": "string", "format": "date"},
    DATETIME={
        "type": "string",
        "pattern": "^[0-9]{4}-((|0)[1-9]|1[0-2])-((|[0-2])[1-9]|3[0-1])(|T)((|[0-1])[0-9]|2[0-3]):((|[0-5])[0-9]):((|[0-5])[0-9])(|.[0-9]{1,6})$"
    },
    TIME={
        "type": "string",
        "pattern": "^((|[0-1])[0-9]|2[0-3]):((|[0-5])[0-9]):((|[0-5])[0-9])(|.[0-9]{1,6})$"
    },
    TIMESTAMP={"type": "string", "format": "date-time"},
    RECORD={"type": "object"},
)


def json_representation(gbq_schema: dict,
                        additional_properties: bool = False) -> dict:
    """Function to convert Google BigQuery schema in JSON representation to json schema.

    Args:

      gbq_schema: BigQuery schema, JSON representation
                read https://cloud.google.com/bigquery/docs/schemas#creating_a_json_schema_file 
                for details.

      additional_properties: Json schema should contain "additionalProperties".

    Returns:

      Json schema as dict.

    Raises:

      fastjsonschema.JsonSchemaException: Error occured if input Google BigQuery schema is invalid.
    """
    output = deepcopy(TEMPLATE)
    
    def _converter(gbq_schema: dict) -> dict:
        """Conversion step."""
        try:
            validate_json(gbq_schema)
        except fastjsonschema.JsonSchemaException as ex:
            raise ex

        output = {
            "type": "object",
            "properties": {
            },
            "additionalProperties": False,
            "required": [
            ],
        }

        for element in gbq_schema:
            key = element['name']
            
            output['properties'][key] = getattr(map_types, element['type'])

            if 'mode' in element:
                if element['mode'] == "REQUIRED":
                    output['required'].append(key)
            
            if element['type'] == "RECORD":
                output['properties'][key] = _converter(element['fields'])
                
        if not output['required']:
            _ = output.pop('required')
            
        return output
    
    output['definitions']['element'] = _converter(gbq_schema)

    output['definitions']['element']['additionalProperties'] = additional_properties

    return output


def sdk_representation(gbq_schema: List[SchemaField],
                       additional_properties: bool = False) -> dict:
    """Function to convert Google BigQuery schema in Google SDK representation to json schema.

    Args:

      gbq_schema: BigQuery schema, SDK repsentation
                read https://googleapis.dev/python/bigquery/latest/generated/google.cloud.bigquery.schema.SchemaField.html
                for details.

      additional_properties: Json Schema should contain "additionalProperties".

    Returns:

      json schema as dict.
    """
    output = deepcopy(TEMPLATE)

    def _converter(gbq_schema: dict) -> dict:
        output = {
            "type": "object",
            "properties": {
            },
            "additionalProperties": False,
            "required": [
            ],
        }
        
        for element in gbq_schema:
            key = element.name

            output['properties'][key] = getattr(map_types, element.field_type)

            if element.mode == "REQUIRED":
                output['required'].append(key)
            
            if element.field_type == "RECORD":
                output['properties'][key] = _converter(element.fields)

        if not output['required']:
            _ = output.pop('required')
        
        return output
    
    output['definitions']['element'] = _converter(gbq_schema)

    output['definitions']['element']['additionalProperties'] = additional_properties

    return output
