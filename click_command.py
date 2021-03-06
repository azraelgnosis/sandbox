import click

# @click.command()
# def hello():
#     click.echo("Hello World!")

# if __name__ == '__main__':
#     hello()

################################################################

@click.group()
def cli(): pass

@click.command()
def init_db():
    click.echo("Initialized the database.")

@click.command()
def close_db():
    click.echo("closed the database.")

cli.add_command(init_db)
cli.add_command(close_db)

#################################################################

@click.group()
def cli2(): pass

@cli.command()
def init_db2():
    click.echo("Initialized the database.")

@cli.command()
def close_db2():
    click.echo("closed the database.")

###################################################################

# @click.command()
# @click.option('--count', default=1, help='number of greetings')
# @click.argument('name')
# def hello(count, name):
#     for x in range(count):
#         click.echo(f'Hello {name}!')

# if __name__ == '__main__':
#     hello()
#     init_db()

###################################################################

@click.command(name="yo")
@click.argument('howdy')
def sup(howdy):
    click.echo("sup")

class Alpha(object):
    def __init__(self, message):
        self.message = message

    @staticmethod
    @click.command()
    def hi():
        print("hi there")
        click.echo(Alpha().greet())

    @staticmethod
    def bye():
        print("goodbye")

    @click.command()
    def greet(self):
        click.echo(self.message)

class Beta(Alpha):
    def __init__(self, message):
        self.message = message

# a = Alpha()
# a.hi()

b = Beta("welcome")
