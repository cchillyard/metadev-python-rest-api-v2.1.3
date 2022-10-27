import requests


def check_vendor_by_url(url: str):
    cog = 0
    availability = 'In Stock'

    res = requests.get(url)
    res_text = res.text
    main_price_text = res_text[res_text.find(
        'US $'): res_text.find('US $') + 20]
    cog = main_price_text.split('$')[1].split('<')[0]
    cog = float(cog.replace(',', '.'))

    on_sale = res_text.find('Buy It Now')

    if on_sale < 0:
        # for russian
        on_sale = res_text.find('Купить сейчас')

    if on_sale < 0:
        availability = 'Out of Stock'
    else:
        in_stock = res_text.find('available</span>')

        if in_stock < 0:
            # for russian
            in_stock = res_text.find('наличии</span>')
            if in_stock < 0: in_stock = res_text.find('Доступно более 10')

        if in_stock > 0:
            availability = 'In Stock'
        else:
            availability = 'Out of Stock'

    return {'cog': cog, 'availability': availability}
