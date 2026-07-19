from bot import MusicBot
from config import load_token


def main() -> None:
    token = load_token()
    MusicBot().run(token)


if __name__ == "__main__":
    main()
