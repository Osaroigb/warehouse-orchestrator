from enum import Enum


class WarehouseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class RobotStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class InventoryStatus(str, Enum):
    SYNCED = "synced"
    OUT_OF_SYNC = "out_of_sync"