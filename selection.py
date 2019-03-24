def truncation(num_parents, sorted_population):
    parents = sorted_population[:num_parents]
    parent_pairs = zip(parents[::2], parents[1::2])
    return parent_pairs

SELECTION_METHODS = {
    'truncation': truncation
}
