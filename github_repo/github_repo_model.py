from pydantic import BaseModel, validator


class SpecModel(BaseModel):
    visibility: str

    @validator("visibility")
    def _validate_visibility(cls, value):
        allowed_values = ["private", "public"]
        assert value in allowed_values, f"{value} not in {allowed_values}"
        return value


class MetadataModel(BaseModel):
    name: str


class GitHubRepoModel(BaseModel):
    kind: str
    metadata: MetadataModel
    spec: SpecModel

    @validator("kind")
    def _validate_kind(cls, value):
        valid_kind = "GitHubRepo"
        assert value == valid_kind, f"{value} is not {valid_kind}"
        return value
