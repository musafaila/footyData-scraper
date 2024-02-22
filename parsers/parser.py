from parsers.prima_league_parser import parse_primatips_league_stats


def parser(page_html):
    if page_html == "":
        return

    data = parse_primatips_league_stats(page_html)
    return data