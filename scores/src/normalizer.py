import numpy as np
from sklearn.preprocessing import QuantileTransformer#, MinMaxScaler

from django.core.exceptions import FieldError


class Normalizer:
    def __init__(self):
        self._random_state = 42

    def _transform_distribution(self, distribution):
        """
        Transforms a given distribution using quantile transformation.
        """
        transformer = QuantileTransformer(output_distribution='uniform', random_state=self._random_state)
        transformer = transformer.fit(distribution)
        return transformer.transform(distribution), transformer

    # def _scale_distribution(self, distribution):
    #     """
    #     Scales a given distribution using min max scaling (range 0.0 to 1.0).
    #     """
    #     scaler = MinMaxScaler(feature_range=(0,1))
    #     scaler = scaler.fit(distribution)
    #     return scaler.transform(distribution), scaler

    def normalize_fields(self, model_object, objects, fields):
        """
        Normalizes given objects fields in two steps:
            1: Transform every field's values distribution into quantile distribution
            2: Scale every field's quantile distribution to the range of 0.0 to 1.0
        """

        # for model_object, fields in objects_and_fields.items():
        # objects = model_object.objects.all()

        for field in fields:
            try:
                values = model_object.objects.values_list(field, flat=True)
            except FieldError:
                values = [getattr(obj, field) for obj in model_object.objects.all()]
            
            # Transform and scale field's value distribution
            distribution = np.array(values).reshape(-1, 1)
            transformed_distribution, transformer = self._transform_distribution(distribution)
            # scaled_distribution, scaler = self._scale_distribution(transformed_distribution)
            
            for object in objects:
                # Updates an object's field with a corresponding normalized value
                value = np.array(getattr(object, field)).reshape(1, -1)
                transformed_value = transformer.transform(value)
                # scaled_value = scaler.transform(transformed_value)
                # object.__dict__[f'normalized_{field}'] = scaled_value
                object.__dict__[f'normalized_{field}'] = transformed_value

        # Bulk update just updated normalized fields
        normalized_fields = [f'normalized_{field}' for field in fields]
        model_object.objects.bulk_update(objects, normalized_fields)
