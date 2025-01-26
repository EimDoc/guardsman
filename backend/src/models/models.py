from pydantic import BaseModel


class FileModel(BaseModel):
    path_to_file: str
