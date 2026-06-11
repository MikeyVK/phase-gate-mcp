import subprocess

def main():
    # Print the file from disk directly
    print("--- FILE ON DISK ---")
    with open("tests/mcp_server/test_tier0_two_line_format.py", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines, 1):
            if idx <= 40:
                print(f"{idx:2d}: {line}", end="")
    
    # Print git diff of the file
    print("\n--- GIT DIFF ---")
    res = subprocess.run(["git", "diff", "tests/mcp_server/test_tier0_two_line_format.py"], capture_output=True, text=True)
    print(res.stdout)

if __name__ == "__main__":
    main()
