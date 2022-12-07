from . import test_wave_parsing

from io import BytesIO
from typing import Generator
import zipfile as zf
import os.path
import os
from contextlib import contextmanager

# class TestFileLoader:
#     """
#     This guy manages the test_files archive.
#     """

#     def __init__(self, test_file_arch_name = 'archive.zip') -> None:
#         self.base_path = os.path.join(os.path.dirname(__file__), "test_files")
#         self.test_file_arch_name = test_file_arch_name
#         self._gather_test_files_into_archive()

#     @property
#     def arch_path(self):
#         return os.path.join(self.base_path, self.test_file_arch_name)        

#     @contextmanager
#     def open(self, name) -> Generator[BytesIO]:
#         z = zf.ZipFile(self.arch_path, 'r')
#         member = z.open(name, 'r')
#         try:
#             yield member
#         finally:
#             zf.close()

#     def _gather_test_files_into_archive(self):
#         with zf.ZipFile(self.arch_path, 'a') as zip:
#             for root, _, files in os.walk(self.base_path):
#                 for name in files:
#                     if root == self.base_path and name == self.test_file_arch_name:
#                         continue
#                     else:
#                         p = os.path.join(root, name)
#                         zip.write(p)
#                         os.unlink(p)


