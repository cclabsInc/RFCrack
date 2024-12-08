from rich import print as printf

from argparse import ArgumentParser




def init_main():
    parser = ArgumentParser()
    parser.add_argument('file', type=str)
    args = parser.parse_args()

    with open(args.file) as f:    content = f.read()
    printf(content)






if __name__ == '__main__':
    init_main()


