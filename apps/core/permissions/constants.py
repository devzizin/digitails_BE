"""
Core permission architecture constants.

IMPORTANT:
These are stable platform-level permission identifiers.
"""

class Actions:
    LIST = "list"

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"

    ASSIGN = "assign"
    MANAGE = "manage"
    EXPORT = "export"

    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"

    CHANGE_STATUS = "change_status"

class Levels:
    ADMIN = "admin"
    MANAGER = "manager"
    EDITOR = "editor"
    VIEWER = "viewer"
    CONTRIBUTOR = "contributor"
    RESTRICTED = "restricted"
    ASSIGNEE = "assignee"
