

class IoCConverter():

    def __init__(self, original_file_str: str):
        self.original_file_str = original_file_str
        self.returned_file_str = None
        self.convert()

    # TODO: The actual conversion
    def convert(self) -> str:
        self.returned_file_str = self.original_file_str
        return self.returned_file_str