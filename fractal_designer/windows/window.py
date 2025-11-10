from fractal_designer.actions import Actions


class Window:
    def __init__(self, actions: Actions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_ = actions

    def disable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setDisabled(True)

    def enable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setEnabled(True)
