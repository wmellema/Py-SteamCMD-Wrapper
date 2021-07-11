class SteamCMD_command:
    _commands = []

    def force_install_dir(self, install_dir: str):
        self._commands.append('+force_install_dir "{}"'.format(install_dir))
        return len(self._commands) - 1

    def add_app(self, app_id: int, validate: bool = False, beta: str = '', beta_pass: str = ''):
        self._commands.append('+app_update {}'.format(
            app_id,
            ' validate' if validate else '',
            ' -beta {}'.format(beta) if beta else '',
            ' -betapassword {}'.format(beta_pass) if beta_pass else '',
        ))
        return len(self._commands) - 1

    def add_workshop(self, app_id: int, workshop_id: int):
        self._commands.append('+workshop_download_item {} {}'.format(app_id, workshop_id))
        return len(self._commands) - 1

    def add_custom(self, cmd: str):
        self._commands.append(cmd)
        return len(self._commands) - 1

    def remove(self, idx):
        if self._commands[idx]:
            self._commands[idx] = None
            return True
        else:
            return False

    def get_cmd(self):
        params = filter(None, self._commands)
        return " ".join(params)
