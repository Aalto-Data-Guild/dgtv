class BaseWidget:
    name = 'Widget'

    @property
    def is_visible(self) -> bool:
        return True 