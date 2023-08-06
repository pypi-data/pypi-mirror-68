import click

from is_url import is_url


@click.command(context_settings={'help_option_names': ["-h", "--help"]})
@click.argument("url")
@click.option('--print-url', is_flag=True, default=False)
@click.option('--strict', is_flag=True, default=False)
def cli(url, print_url, strict):

    is_url_result = is_url(url=url, strict=strict)

    if print_url:
        print(f"{is_url_result}: {url}")
    else:
        print(is_url_result)


if __name__ == "__main__":
    cli()
