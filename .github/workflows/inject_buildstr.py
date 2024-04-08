import sys
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("scriptpath", type=str,
    help="Script path for injecting.")
parser.add_argument("ident", type=str, default="custombuild", nargs='?',
                    help="Identifier value used that is equal to buildstr.")
parser.add_argument('-nf', '--nofail',
    help="Returns exit code 0 on error.", action='store_true')
args = parser.parse_args()
scriptpath = args.scriptpath
ident = args.ident
exit_code = 1 - args.nofail

def get_latest_commit(fallback="default"):
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        print("! Exception on getting latest commit, returning fallback")
        return fallback

def inject_buildstr(commithash):
    try:
        with open(scriptpath, "r+") as file:
            content = file.read()
            file.seek(0)
            file.writelines(content.replace(f'buildstr = "{ident}"',
                f'buildstr = "{commithash[:7]}"'))
            file.truncate()
        print(f"Updated {scriptpath} with commit hash: {commithash}")
    except FileNotFoundError:
        print("! Script not found, exiting")
        sys.exit(exit_code)
    except Exception as e:
        print(f"! Uncaught exception {e}, exiting")
        sys.exit(exit_code)

if __name__ == "__main__":
    inject_buildstr(get_latest_commit())
