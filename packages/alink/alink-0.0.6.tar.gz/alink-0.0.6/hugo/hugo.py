import os
import click


@click.command()
@click.argument('url')
def cli(url):
    if len(url) == 0:
        return
    output = os.popen('adb -d shell am start %s -a android.intent.action.VIEW' % url).readlines()[0]
    echo(output)


def echo(value):
    print('\033[32m %s \033[0m' % value)


if __name__ == '__main__':
    cli()
