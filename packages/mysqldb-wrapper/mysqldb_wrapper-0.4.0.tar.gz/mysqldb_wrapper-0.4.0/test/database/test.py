"""Test table"""

from mysqldb_wrapper import Base, Id


class Test(Base):
    """Test class"""

    __tablename__ = "test"

    id = Id()
    hashed = bytes()
    number = int(1)
    string = str("string")
    boolean = bool(True)
    created_at = int()
    updated_at = int()

    def func(self):
        pass
