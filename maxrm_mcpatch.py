"""
Hex patterns for Minecraft patching
by Max-RM
"""
__version__ = "0.3.0"

import re
IMAGE_FILE_MACHINE_AMD64 = 0x8664 # x64
IMAGE_FILE_MACHINE_ARM = 0x1c0 # ARM little endian
IMAGE_FILE_MACHINE_ARMNT = 0x1c4 # ARM Thumb-2 little endian
IMAGE_FILE_MACHINE_ARM64 = 0xaa64 # ARM64 little endian
IMAGE_FILE_MACHINE_I386 = 0x14c # Intel 386 or later processors and compatible processors

def _c_h(pattern: str): return pattern.casefold().replace(" ", "")
def _ccm(pattern: str): return re.compile(_c_h(pattern))

PATCHES = {
    "amd64": [
        (
            _ccm(r"(39 9E C8 00 00 00) 0F 95 C1 (88 0F 8B)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        ),
        (
            _ccm(r"(FF EB 05) 8A 49 61 (88 0A 8B CB E8)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        )
    ],
    "i386": [
        (
            _ccm(r"(FF EB 08 39 77 74) 0F 95 C1 (88 08 8B)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        ),
        (
            _ccm(r"(FF EB 08 8B 4D 08) 8A 49 31 (88 08 8B)"),
            _c_h(r"\g<1> B1 00 90 \g<2>"), 0
        )
    ],
    "arm": [
        (
            _ccm(r"(05 E0 .. 3 .. 0B) B1 01 (23 00 E0 00 23 2B 70 20 46)"),
            _c_h(r"\g<1> B1 00 \g<2>"), 0
        ),
        (
            _ccm(r"(02 E0) 90 F8 .. 30 (0B 70 20 46)"),
            _c_h(r"\g<1> 4F F0 00 03 \g<2>"), 0
        )
    ],
    "arm64": [
        (
            _ccm(r"(FE 97 05 00 00 14 A8 .. A 40 B9 1F 01 00 71) E9 07 9F 1A (89 02 00 39 E0 03 13 2A)"),
            _c_h(r"\g<1> 09 00 80 52 \g<2>"), 0
        ),
        (
            _ccm(r"(FC 97 03 00 00 14 08) .. 41 39 (28 00 00 39 E0 03 13 2A)"),
            _c_h(r"\g<1> 00 80 52 \g<2>"), 1
        )
    ]
}

def check_machine(filename: str):
    """
    Get machine from PE headers from Minecraft executable

    Arguments:
    filename: str: Path to Minecraft.Windows.exe

    Returns string (one of "amd64", "i386", "arm", "arm64")
    Raises NotImplementedError if unsupported architecture
    """
    with open(filename, "rb") as file:
        file.seek(0x3C)
        # COFF header offset
        COFF_offset = int.from_bytes(file.read(4), "little")
        file.seek(COFF_offset)
        # Skip signature
        file.read(4)
        # Machine header
        machine = int.from_bytes(file.read(2), "little")
        if machine == IMAGE_FILE_MACHINE_AMD64:
            return "amd64"
        elif machine == IMAGE_FILE_MACHINE_I386:
            return "i386"
        elif machine == IMAGE_FILE_MACHINE_ARM or machine == IMAGE_FILE_MACHINE_ARMNT:
            return "arm"
        elif machine == IMAGE_FILE_MACHINE_ARM64:
            return "arm64"
        else:
            raise NotImplementedError("Unsupported machine header %s" % machine)

def patch_module(architecture: str, dll_data: bytes) -> bytes:
    """
    Patch Windows.ApplicationModel.Store module.

    Arguments:
    architecture: str: Module architecture. Use
    maxrm_mcpatch.check_machine(filename) if you
    don't have a value
    dll_data: bytes: Windows.ApplicationModel.Store
    module data as a bytestring.

    Returns patched DLL as a bytestring.
    Raises NotImplementedError if unsupported architecture
    """
    dll_data = dll_data.hex()
    if architecture in PATCHES:
        for pattern, replace, count in PATCHES[architecture]:
            dll_data = pattern.sub(replace, dll_data, count)
    else:
        raise NotImplementedError("Unsupported architecture %s" % architecture)
    return bytes.fromhex(dll_data)
