"""
Hex patterns for Minecraft patching
by Max-RM
"""
IMAGE_FILE_MACHINE_AMD64 = 0x8664 # x64
IMAGE_FILE_MACHINE_ARM = 0x1c0 # ARM little endian
IMAGE_FILE_MACHINE_ARMNT = 0x1c4 # ARM Thumb-2 little endian
IMAGE_FILE_MACHINE_ARM64 = 0xaa64 # ARM64 little endian
IMAGE_FILE_MACHINE_I386 = 0x14c # Intel 386 or later processors and compatible processors

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
        COFF_offset = int.from_bytes(file.read(4), byteorder="little")
        file.seek(COFF_offset)
        # Skip signature
        file.read(4)
        # Machine header
        machine = int.from_bytes(file.read(2), byteorder="little")
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
    """
    if architecture == "amd64":
        return dll_data.replace(
            bytes.fromhex("39 9E C8 00 00 00 0F 95 C1 88 0F 8B"),
            bytes.fromhex("39 9E C8 00 00 00 B1 00 90 88 0F 8B")
        ).replace(
            bytes.fromhex("FF EB 05 8A 49 61 88 0A 8B CB E8"),
            bytes.fromhex("FF EB 05 B1 00 90 88 0A 8B CB E8")
        )
    elif architecture == "i386":
        return dll_data.replace(
            bytes.fromhex("FF EB 08 39 77 74 0F 95 C1 88 08 8B"),
            bytes.fromhex("FF EB 08 39 77 74 B1 00 90 88 08 8B")
        ).replace(
            bytes.fromhex("FF EB 08 8B 4D 08 8A 49 31 88 08 8B"),
            bytes.fromhex("FF EB 08 8B 4D 08 B1 00 90 88 08 8B")
        )
    elif architecture == "arm": # Experimental
        return dll_data.replace(
            bytes.fromhex("73 6F 0B B1 01 23 00"),
            bytes.fromhex("73 6F 0B B1 00 23 00")
        ).replace(
            bytes.fromhex("02 E0 90 F8 31 30"),
            bytes.fromhex("02 E0 4F F0 00 03")
        )
    elif architecture == "arm64": # Experimental
        return dll_data.replace(
            bytes.fromhex("FE 97 05 00 00 14 A8 CA 40 B9 1F 01 00 71 E9 07 9F 1A 89 02 00 39 E0 03 13 2A"),
            bytes.fromhex("FE 97 05 00 00 14 A8 CA 40 B9 1F 01 00 71 09 00 80 52 89 02 00 39 E0 03 13 2A")
        ).replace(
            bytes.fromhex("FC 97 03 00 00 14 08 84 41 39 28 00 00 39 E0 03 13 2A"),
            bytes.fromhex("FC 97 03 00 00 14 08 00 80 52 28 00 00 39 E0 03 13 2A"),
            1 # Use only the first result
        )
