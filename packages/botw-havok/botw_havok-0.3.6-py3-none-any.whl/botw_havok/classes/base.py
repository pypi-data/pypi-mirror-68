from ..binary import BinaryReader, BinaryWriter
from ..binary.types import String
from ..container.util.hkobject import HKObject

if False:
    from ..hkfile import HKFile


class HKBaseClass:
    hkClass: String

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: HKObject):
        # SPECIFIC HKCLASS BEHAVIOUR EXECUTES AFTER THIS

        self.hkClass = obj.hkClass.name

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: HKObject):
        # SPECIFIC HKCLASS BEHAVIOUR EXECUTES BEFORE THIS

        obj.bytes = bw.getvalue()
        obj.size = len(obj.bytes)

    def assign_class(self, hkFile: "HKFile", obj: "HKObject"):
        obj.hkClass = hkFile.classnames.get(self.hkClass)

    def as_dict(self):
        return {"hkClass": self.hkClass}

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.hkClass = String(d["hkClass"])

        return inst

    def __eq__(self, value: object):
        if not isinstance(value, HKBaseClass):
            raise NotImplementedError()
        comparison = self.__dict__ == value.__dict__
        if not comparison:
            print(f"Class '{self.__class__.__name__}' doesn't match")
        return comparison
