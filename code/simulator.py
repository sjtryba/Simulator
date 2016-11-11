import rocket


def main():
    sls = rocket.load_rocket()  # create rocket object
    rocket.pre_launch(sls)

if __name__ == '__main__':
    main()
