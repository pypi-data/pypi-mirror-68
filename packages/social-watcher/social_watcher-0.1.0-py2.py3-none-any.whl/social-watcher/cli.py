import click

@click.command()
@click.option("--config", help="Full path of configuration file" )
@click.option("--sqlite", help="Full path for sqlite database, if not initialized all datas storaged at on-memory", default=None)
def main(config, sqlite):
    if not config or not os.path.exists(config):
        print("Config file not exists, please specify full path.")
        print("Use --help parameter for available parameters.")
        return

    if sqlite and not os.path.exists(sqlite):
        pass
