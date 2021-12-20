class Plot:
    def __init__(self):
        needed_attrs = ['display_name', 'exp', 'colors', 'show_n', 'fps']
        if not all(hasattr(self, attr) for attr in needed_attrs):
            raise AttributeError(f"Plotrule class must have the following attributes {needed_attrs} set in its init function.")
        self.stats_pres = 2