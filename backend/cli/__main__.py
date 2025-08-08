from cleo.application import Application
from cli.commands.dbinit import DbInitCommand

def main():
    app = Application("ai-adviser CLI", "1.0.0")
    app.add(DbInitCommand())
    app.run()

if __name__ == "__main__":
    main()
