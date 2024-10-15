class FolderSystem(object):
    CONFIG_NAME = "FOLDER"

    def __init__(self, utils):
        self.__utils = utils

        self.__folder_settings = self.init_folder_settings()

        self.init()

    def get_utils(self):
        return self.__utils

    def init(self):
        for key, value in self.get_folder_settings().items():
            _key = f"__{key}"
            if _key not in dir(self):
                setattr(self, _key, value)

    def get_folder_settings(self) -> dict:
        return self.__folder_settings

    def get_folder_settings_item(self, key: str) -> any:
        return self.get_folder_settings().get(key, None)

    def init_folder_settings(self) -> dict:
        _settings = self.get_utils().get_settings_item(
            self.get_utils().get_system_settings,
            self.CONFIG_NAME
        )

        if _settings is not None and _settings and isinstance(_settings, dict):
            return _settings
        raise ValueError()

    def get_class_item(self, item: str) -> any:
        _item = f"__{item}"
        if _item in dir(self):
            return getattr(self, _item)
        else:
            return ""

    def get_output_file_folder(self):
        return self.get_class_item("OUTPUT_FILE_FOLDER")

    def get_input_file_folder(self):
        return self.get_class_item("INPUT_FILE_FOLDER")

    def get_log_file_folder(self):
        return self.get_class_item("LOG_FILE_FOLDER")

    def get_read_file_folder(self):
        return self.get_class_item("READ_FILE_FOLDER")

    def get_core_file_folder(self):
        return self.get_class_item("CORE_CODE_FILE_FOLDER")

    def get_tamper_file_folder(self):
        return self.get_class_item("TAMPER_FILE_FOLDER")

    def get_module_file_folder(self):
        return self.get_class_item("MODULE_FILE_FOLDER")
