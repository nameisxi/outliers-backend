from dataclasses import field
from scipy.stats import zscore


class Normalizer:
    def __init__(self):
        # TODO: Unskew data (log transformer power distributions etc)
        pass

    def _clip_field_distribution(self, values, field_name):
        clippings = {
            'repos_count': {
                'min':0,
                'max':250,
            },
            'gists_count': {
                'min':0,
                'max':100,
            },
            'contributions_count': {
                'min':0,
                'max':2500,
            },
            'followers_count': {
                'min':0,
                'max':400,
            },
            'followers_following_counts_difference': {
                'min':-250,
                'max':400,
            },
            'size_in_kilobytes': {
                'min':0,
                'max':1000,
            },
            'stargazers_count': {
                'min':0,
                'max':50,
            },
            'forks_count': {
                'min':0,
                'max':10,
            },
            'watchers_count': {
                'min':0,
                'max':50,
            },
        }

        values = [max(value, clippings[field_name]['min']) for value in values]
        clipped_distribution = [min(value, clippings[field_name]['max']) for value in values]

        return clipped_distribution

    def _clip_single_value(self, value, field_name):
        clippings = {
            'repos_count': {
                'min':0,
                'max':250,
            },
            'gists_count': {
                'min':0,
                'max':100,
            },
            'contributions_count': {
                'min':0,
                'max':2500,
            },
            'followers_count': {
                'min':0,
                'max':400,
            },
            'followers_following_counts_difference': {
                'min':-250,
                'max':400,
            },
            'size_in_kilobytes': {
                'min':0,
                'max':1000,
            },
            'stargazers_count': {
                'min':0,
                'max':50,
            },
            'forks_count': {
                'min':0,
                'max':10,
            },
            'watchers_count': {
                'min':0,
                'max':50,
            },
        }

        value = max(value, clippings[field_name]['min'])
        value = min(value, clippings[field_name]['max'])

        return value

    # def find_distributions(self):
    #     pass

    # def unskew_data(self):
    #     pass

    def compute_z_scores(self, list):
        """
        Computes Z-scores based on the given list for all of its elements and returns a dictionary where every key represents the original value and every value represents the Z-score.
        """
        z_scores_lookup = {}
        z_scores = zscore(list)
        
        for original_value, z_score in zip(list, z_scores):
            if original_value not in z_scores_lookup.keys():
                z_scores_lookup[original_value] = z_score

        return z_scores_lookup

    def min_max_scale(self, value, min, max):
        """
        Uses min-max scaling to scale a given value to the range of (0, 1).
        """
        return (value - min) / (max - min)

    def scale_z_scores(self, z_scores):
        """
        Scales given z_scores dictionary's z-score values into the range of (0,1) using min-max-scaling.
        """
        # Find min and max values of the dictionary's z scores
        min_value = min(z_scores.values())
        max_value = max(z_scores.values())

        # Apply min max scaling to the dictionary's z scores
        scaled_z_scores = {value: self.min_max_scale(z_score, min_value, max_value) for value, z_score in z_scores.items()}

        return scaled_z_scores

    def _normalize_fields(self, objects_and_fields):
        """
        Normalizes given objects fields in three steps:
            1: Z-scores are computed for every field
            2: These Z-scores are scaled to range of (0, 1) using min-max scaling
            3: The original objects field values will be replaced by the scaled Z-scores
        """

        for model_object, fields in objects_and_fields.items():
            objects = model_object.objects.all()

            for field in fields:
                clipped_values = self._clip_field_distribution(list(model_object.objects.values_list(field, flat=True)), field)
                z_scores = self.compute_z_scores(clipped_values)
                scaled_z_scores = self.scale_z_scores(z_scores)
                
                for object in objects:
                    # Updates an object's field with a scaled Z-score
                    object.__dict__[f'normalized_{field}'] = scaled_z_scores[self._clip_single_value(getattr(object, field), field)]

            normalized_fields = [f'normalized_{field}' for field in fields]
            model_object.objects.bulk_update(objects, normalized_fields)
