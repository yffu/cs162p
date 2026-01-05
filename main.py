def display_lines(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file]

            if lines:
                print("Errors logged:")
                # print("File contains:")

                for i in range(len(lines)):
                    if lines[i].split()[0] == "[ERROR]":
                        print(lines[i])
            else:
                print("No lines found.")

    except FileNotFoundError:
        print("File not found. Please check the file path.")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    display_lines("server_logs.txt")

if __name__ == "__main__":
    main()
