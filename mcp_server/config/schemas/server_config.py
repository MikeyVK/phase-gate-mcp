# pgmcp:v1 id=python_pydantic_config pv=1.0.0 pf=TDVmp2pacKoBW_qk sf=WI5iXHBKVOU91bYE

"Closed startup timing configuration; no filesystem or loader knowledge."

# Standard library
from typing import Annotated, Literal, Self

# Third party
from pydantic import BaseModel, ConfigDict, Field, model_validator

PositiveSeconds = Annotated[float, Field(strict=True, gt=0, allow_inf_nan=False)]


class StartupLockConfig(BaseModel):
    """Finite, explicit bounds for ordinary startup contention."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    max_wait_seconds: PositiveSeconds
    retry_interval_seconds: PositiveSeconds

    @model_validator(mode="after")
    def validate_interval(self) -> Self:
        if self.retry_interval_seconds > self.max_wait_seconds:
            raise ValueError("startup_lock_interval_exceeds_wait")
        return self


class ProxyConfig(BaseModel):
    """Explicit proxy initialization deadline."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)
    initialization_timeout_seconds: PositiveSeconds


class ServerConfig(BaseModel):
    "Required immutable startup policy shared by server and proxy composition."

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
    )

    version: Literal["1.0.0"] = Field(
        description="Version of the startup policy schema.",
    )

    startup_lock: StartupLockConfig
    proxy: ProxyConfig

    @model_validator(mode="after")
    def validate_deadline(self) -> Self:
        if self.proxy.initialization_timeout_seconds <= self.startup_lock.max_wait_seconds:
            raise ValueError("proxy_deadline_must_exceed_lock_wait")
        return self
