__author__ = 'y981821'


class FeatureBroker:
    def __init__(self, allow_replace=False):
        self.providers = {}
        self.allowReplace = allow_replace

    def provide(self, feature, provider, *args, **kwargs):
        if not self.allowReplace:
            assert not self.providers in feature, "Duplicate feature: %r" % feature
        if callable(provider):
            def call():
                return provider(*args, **kwargs)
        else:
            def call():
                return provider
        self.providers[feature] = call

    def __getitem__(self, feature):
        try:
            provider = self.providers[feature]
        except KeyError:
            raise KeyError("Unknown feature named %r" % feature)
        return provider()


features = FeatureBroker()

http://code.activestate.com/recipes/413268/