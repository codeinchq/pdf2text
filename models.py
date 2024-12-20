#  Copyright 2024 Code Inc. <https://www.codeinc.co>
#
#  Use of this source code is governed by an MIT-style
#  license that can be found in the LICENSE file or at
#  https://opensource.org/licenses/MIT.

from pydantic import BaseModel
from typing import List

class Page(BaseModel):
    page_number: int
    text: str

class ExtractResponse(BaseModel):
    pages: List[Page]