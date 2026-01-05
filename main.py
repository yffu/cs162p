import sys

def display_lines(file_path, search_sequence):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file]

            if lines:
                print(search_sequence + "s logged:")

                for line in lines:
                    if (search_sequence in line):
                        print(line)
            else:
                print("No lines found.")

    except FileNotFoundError:
        print("File not found. Please check the file path.")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # print(sys.argv)
    if len(sys.argv) != 3:
        print("Usage: python3 program.py <file_path> <search_sequence>")
        return

    file_path = sys.argv[1]
    search_sequence = sys.argv[2]
    display_lines(file_path, search_sequence)


if __name__ == "__main__":
    main()
