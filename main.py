import sys

def display_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file]

            if lines:
                print("Errors logged:")

                for line in lines:
                    if ("INFO" in line):
                        print(line)
            else:
                print("No lines found.")

    except FileNotFoundError:
        print("File not found. Please check the file path.")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Usage: python3 program.py <file_path>")
        return

    file_path = sys.argv[1]
    display_lines(file_path)


if __name__ == "__main__":
    main()
