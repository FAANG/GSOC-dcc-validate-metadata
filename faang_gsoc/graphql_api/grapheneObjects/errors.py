from .constants import MAX_FILTER_QUERY_DEPTH

QUERY_MAX_DEPTH_EXCEEDED = 'Query exceeds the maximum join depth of {}'.format(MAX_FILTER_QUERY_DEPTH)
DERIVED_FROM_EMPTY = 'derived_from filter map cannot be empty'