import print_toys


def main():
    print_toys.lattice_examples()
    print_toys.process_examples()
    print_toys.enabled_collection_examples()

    # print_toys.simulation_examples()
    print_toys.simulation_interactive(num_sites=1)


if __name__ == '__main__':
    main()
