class BaseWidget:
    def grid(self, **kwargs):
        self.grid_kwargs = kwargs
        super().grid(**kwargs)
        return self

    def pack(self, **kwargs):
        self.pack_kwargs = kwargs
        super().pack(**kwargs)
        return self

    def configure(self, **kwargs):
        super().configure(**kwargs)
        return self
