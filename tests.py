from functions.run_python import run_python_file

def main():
    print("Test 1: ")
    print(run_python_file("calculator", "main.py"), end="\n\n")

    print("Test 2: ")
    print(run_python_file("calculator", "tests.py"), end="\n\n")

    print("Test 3: – should fail")
    print(run_python_file("calculator", "../main.py"), end="\n\n")

    print("Test 4: – should fail")
    print(run_python_file("calculator", "nonexistent.py"), end="\n\n")

if __name__ == "__main__":
    main()

# from functions.write_file import write_file

# def main():
#     print("Test 1: ")
#     print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), end="\n\n")

#     print("Test 2: ")
#     print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), end="\n\n")

#     print("Test 3: – should fail")
#     print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), end="\n\n")

# if __name__ == "__main__":
#     main()


# from functions.get_file_content import get_file_content

# def main():
#     print("Test 1: ")
#     print(get_file_content("calculator", "main.py"), end="\n\n")

#     print("Test 2: ")
#     print(get_file_content("calculator", "pkg/calculator.py"), end="\n\n")

#     print("Test 3: – should fail")
#     print(get_file_content("calculator", "/bin/cat"), end="\n\n")

# if __name__ == "__main__":
#     main()


# from functions.get_files_info import get_files_info

# def main():
#     print("Test 1: Current Directory (.)")
#     print(get_files_info("calculator", "."), end="\n\n")

#     print("Test 2: pkg Directory")
#     print(get_files_info("calculator", "pkg"), end="\n\n")

#     print("Test 3: Absolute Path (/bin) – should fail")
#     print(get_files_info("calculator", "/bin"), end="\n\n")

#     print("Test 4: Parent Directory (../) – should fail")
#     print(get_files_info("calculator", "../"), end="\n\n")

# if __name__ == "__main__":
#     main()