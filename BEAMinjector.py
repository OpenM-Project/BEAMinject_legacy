"""
BEAMinjector module, made for BEAMinject

For usage as a module, check out the
"# Modify values for imported usage" section
of the code, and then configure accordingly
"""
__version__ = "0.3.1"

import os
import sys
import json
import ctypes
import subprocess
import librosewater
import librosewater.module
import maxrm_mcpatch

# Modify values for imported usage
launchmc = True
if sys.stdout:
    write_logs = sys.stdout.write
else:
    # sys.stdout doesn't exist, so we can just write a dummy function
    def write_logs(*args, **kwargs):
        pass
quitfunc = sys.exit

# Identify for inject_buildstr.py
buildstr = "custombuild"

def main():
    write_logs(f"* Hello from BEAMinjector {__version__}\n")
    write_logs("= Getting Minecraft install... ")
    mcinstall = json.loads(subprocess.run(["powershell.exe",
    "Get-AppxPackage -name Microsoft.MinecraftUWP | ConvertTo-Json"],
    stdout=subprocess.PIPE, text=True).stdout)
    if not mcinstall:
        write_logs("\n! Couldn't find Minecraft\n")
        return quitfunc()
    mcpath = os.path.join(mcinstall["InstallLocation"], "Minecraft.Windows.exe")
    write_logs(f"found version {mcinstall["Version"]}!\n")
    if launchmc:
        write_logs("= Launching Minecraft\n")
        subprocess.run(["powershell.exe", f'explorer.exe shell:AppsFolder\\{mcinstall["PackageFamilyName"]}!App'])
    write_logs("= Waiting for Minecraft to launch... ")
    while not "Minecraft.Windows.exe".encode() in \
        subprocess.check_output(["tasklist", "/FI", "IMAGENAME eq Minecraft.Windows.exe"],
            stderr=subprocess.STDOUT):
        continue
    output = subprocess.check_output(
        ["tasklist", "/FI", f"IMAGENAME eq Minecraft.Windows.exe", "/FO", "CSV"],
        stderr=subprocess.STDOUT)
    lines = output.decode().splitlines()
    PID = int(lines[1].split(",")[1][1:-1])
    write_logs(f"found at PID {PID}!\n")
    process_handle = ctypes.windll.kernel32.OpenProcess(librosewater.PROCESS_ALL_ACCESS, False, PID)
    
    # Get module address
    write_logs("= Waiting for module... ")
    try:
        module_address, _ = librosewater.module.wait_for_module(process_handle, "Windows.ApplicationModel.Store.dll")
    except librosewater.exceptions.QueryError:
        write_logs(f"! Couldn't wait for module, did Minecraft close?\n")
        return quitfunc()
    write_logs(f"found at {hex(module_address)}!\n")

    # Dump module to variable
    write_logs("= Dumping module... ")
    try:
        data = librosewater.module.dump_module(process_handle, module_address)
    except librosewater.exceptions.ReadWriteError:
        write_logs(f"\n! Couldn't dump module, did Minecraft close?\n")
        return quitfunc()
    write_logs(f"done (read {len(data[1])} bytes)!\n")

    # Inject new module data
    write_logs("= Patching module... ")
    try:
        arch = maxrm_mcpatch.check_machine(mcpath)
    except NotImplementedError:
        write_logs("\n ! Couldn't find patches for platform, may be unsupported")
    write_logs(f"got architecture {arch}... ")
    new_data = maxrm_mcpatch.patch_module(arch, data[1])
    write_logs("done!\n")

    write_logs("= Injecting module... ")
    try:
        librosewater.module.inject_module(process_handle, module_address, new_data)
    except librosewater.exceptions.ReadWriteError:
        write_logs(f"\n! Couldn't inject module, did Minecraft close?\n")
        return quitfunc()
    write_logs(f"done (wrote {len(new_data)} bytes)!\n")

    write_logs("* Patched successfully!\n")
    return quitfunc()

if __name__ == "__main__":
    main()
