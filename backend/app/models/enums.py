import enum


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    MODERATOR = "MODERATOR"


class ContentStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class CommentStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SPAM = "SPAM"


class MediaKind(str, enum.Enum):
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    VIDEO = "VIDEO"


class VideoType(str, enum.Enum):
    MUSIC_VIDEO = "MUSIC_VIDEO"
    LIVE_PERFORMANCE = "LIVE_PERFORMANCE"
    INTERVIEW = "INTERVIEW"
    BEHIND_THE_SCENES = "BEHIND_THE_SCENES"
    PROMOTIONAL = "PROMOTIONAL"


class VideoSource(str, enum.Enum):
    UPLOAD = "UPLOAD"
    EXTERNAL = "EXTERNAL"
