import numpy as np
from sklearn.preprocessing import QuantileTransformer, MinMaxScaler


class Normalizer:
    def __init__(self):
        # TODO: add random state to transformers and scalers
        pass

    def _transform_distribution(self, distribution):
        transformer = QuantileTransformer(output_distribution='normal', random_state=42)
        transformer = transformer.fit(distribution)
        return transformer.transform(distribution), transformer

    def _scale_distribution(self, distribution):
        scaler = MinMaxScaler(feature_range=(-1,1))
        scaler = scaler.fit(distribution)
        return scaler.transform(distribution), scaler

    def _normalize_fields(self, objects_and_fields):
        """
        Normalizes given objects fields in two steps:
            1: Transform every field's values distribution into quantiles
            2: Scale every field's quantile distribution's between 0.0 and 1.0
        """

        for model_object, fields in objects_and_fields.items():
            objects = model_object.objects.all()

            for field in fields:
                # Transform and scale field's value distribution
                distribution = np.array(model_object.objects.values_list(field, flat=True)).reshape(-1, 1)
                transformed_distribution, transformer = self._transform_distribution(distribution)
                scaled_distribution, scaler = self._scale_distribution(transformed_distribution)
                
                for object in objects:
                    # Updates an object's field with a corresponding normalized value
                    value = np.array(getattr(object, field)).reshape(1, -1)
                    transformed_value = transformer.transform(value)
                    scaled_value = scaler.transform(transformed_value)
                    object.__dict__[f'normalized_{field}'] = scaled_value

            # Bulk update just updated normalized fields
            normalized_fields = [f'normalized_{field}' for field in fields]
            model_object.objects.bulk_update(objects, normalized_fields)