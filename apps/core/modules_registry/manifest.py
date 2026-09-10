from dataclasses import dataclass, field


@dataclass(slots=True)
class RegistryManifest:
    """
    Unified registry contract returned from every app.registry.
    """

    app_label: str
    module_path: str

    entity_types: list[dict] = field(default_factory=list)
    permissions: list[dict] = field(default_factory=list)
    # role_templates: list[dict] = field(default_factory=list)

    # app_levels: dict[str, list[str]] = field(
    #     default_factory=dict
    # )
    module: dict | None = None
