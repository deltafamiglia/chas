from src.api_client.client import Client


def main():
    client = Client()

    parser = argparse.ArgumentParser(
        '--address', '-a',
        dest='containerd_address', type=str, metavar='A',
        default='unix:///run/containerd/containerd.sock',
        help='address for containerd\'s GRPC server'
    )

    args = parser.parse_args()
    lsctr(args)


if __name__ == "__main__":
    main()
