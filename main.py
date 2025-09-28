from core.app_state import config
from core.logging_config import setup_logging


def main():
    setup_logging(log_path=config.app.log_path, log_level=config.app.log_level)
    print("Hello from synapse!")


if __name__ == "__main__":
    main()
