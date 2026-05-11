# .phase-gate\temp\ValidationTestDto.py
# template=dto version=0d83ee77 created=2026-05-08T13:23Z updated=
"""ValidationTestDto DTO module.

Data Transfer Object for ValidationTestDto.

@layer: DTOs
@dependencies: pydantic.BaseModel
@responsibilities: Data validation, type safety
"""

# Third-party
from pydantic import BaseModel, Field

# Project modules

class ValidationTestDto(BaseModel):
    """ValidationTestDto DTO.

    Data Transfer Object for ValidationTestDto.

    Fields:
        symbol: str
        price: float
    """
    symbol: str = Field(
        description="symbol field",
    )
    price: float = Field(
        description="price field",
    )

    model_config = {
        "frozen": False,
        "extra": "forbid",
    }
