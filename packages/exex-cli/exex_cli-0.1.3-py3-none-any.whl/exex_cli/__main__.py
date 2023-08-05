from .application import application
from .commands import ExtractCommand

if __name__ == "__main__":
    application.add(ExtractCommand())
    application.set_default_command("extract", is_single_command=True)
    application.run()
