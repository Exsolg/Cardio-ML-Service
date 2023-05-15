from flask_restx import SchemaModel

predict_schema = SchemaModel('predict', {
    'type': 'object',
    'properties': {
        'predict': {
            'type': 'number',
            'format': 'float',
            'minimum': 0,
            'maximum': 1
        }
    }
})

model_schema = SchemaModel('model', {
    'type': 'object',
    'properties': {
        'id': {
            'type': 'string',
            'format': 'uuid',
        },
        'method': {
            'type': 'string'
        },
        'for': {
            'type': 'string'
        },
        'score': {
            'type': 'object',
            'properties': {
                'f1': {
                    'type': 'number',
                    'format': 'float',
                    'minimum': 0,
                    'maximum': 1
                },
                'recall': {
                    'type': 'number',
                    'format': 'float',
                    'minimum': 0,
                    'maximum': 1
                },
                'precision': {
                    'type': 'number',
                    'format': 'float',
                    'minimum': 0,
                    'maximum': 1
                },
                'accuracy': {
                    'type': 'number',
                    'format': 'float',
                    'minimum': 0,
                    'maximum': 1
                }
            }
        }
    }
})
