import json
import copy

class Settings:
    def __init__(self,load_dict: dict, can_save_or_reload: bool = False ,_file_path: str = None) -> None:
        if can_save_or_reload:
            if not isinstance(_file_path, str):
                raise ValueError("a str file path is needed to be saved or reloaded")
        self._path = _file_path
        self._load(load_dict)
        self._can_save_or_reload = can_save_or_reload
    
    def _load(self, load_dict: dict) -> None:
        """
        charge les settings à partir d'un dictionnaire
        """
        for k, v in load_dict.items():
            if isinstance(v, dict):
                v = Settings(v)
            setattr(self, k, v)
    
    def reload(self) -> None:
        """
        recharge les settings (à utiliser si le .json a été modifié durant le jeu)
        """
        if not self._can_save_or_reload:
            raise ValueError(f"{self} is not reloadable")
        
        with open(self._path, "r") as settings_file:
            load_dict = json.load(settings_file)
        self._load(load_dict)

    def save(self) -> None:
        """
        enregistre les settings dans le .json depuis lequel ils ont étés chargés
        """
        if not self._can_save_or_reload:
            raise ValueError(f"{self} is not saveable")
        
        with open(self._path, "w") as settings_file:
            var = self.to_dict()
            json.dump(var, settings_file, indent=4)

    def to_dict(self) -> dict:
        """
        convertis les settings en un dictionnaire
        """
        self_copy = copy.copy(self)
        d = vars(self_copy)
        attr_to_del = []
        for k, v in d.items():
            if k.startswith("_"):
                attr_to_del.append(k)
                continue

            if isinstance(v, Settings):
                d[k] = v.to_dict()
        
        for attr in attr_to_del:
            del d[attr]

        return d

    @staticmethod
    def from_file_path(file_path: str, can_save_or_reload: bool=True):
        """
        créé un objets Settings à partir d'un .json
        """
        with open(file_path, "r") as settings_file:
            load_dict = json.load(settings_file)
        return Settings(load_dict, can_save_or_reload, file_path)


user_settings = Settings.from_file_path("./settings_user.json", True)
dev_settings = Settings.from_file_path("./settings_dev.json", True)
debug_settings = Settings.from_file_path("./settings_debug.json", True)