import asyncio
from datetime import datetime

import httpx
import pandas as pd
from sqlalchemy.orm import Session

from src.services.dao import get_current_cards, get_info_cards

URL_API = 'https://portaldarede.intranet.bb.com.br/varejo/api/publico/conteudos'
URL_SITE = 'https://portaldarede.intranet.bb.com.br/varejo/artigos/'


async def _get_one_card_data(card_number: int, client: httpx.AsyncClient):
    """Busca dados de um card no site."""
    url = f'{URL_API}/{card_number}'

    response = await client.get(url)
    if response.status_code != httpx.codes.OK:
        return None

    data = response.json()
    return {'CD_CARD': data['id'], 'SITE_VERS': data['versao']}


async def _get_all_cards_data(card_numbers: list[int], client: httpx.AsyncClient):
    """Busca dados de vários cards no site."""
    tasks = [_get_one_card_data(card, client) for card in card_numbers]
    site_data = await asyncio.gather(*tasks)
    return site_data


async def _compare_versions(session: Session, client: httpx.AsyncClient):
    """Compara versões do banco com o site."""
    # Pega dados do banco via data_acess
    db_df = pd.DataFrame(get_current_cards(session))
    db_df.columns = db_df.columns.str.upper()

    # Busca versões do site e filtra resultados None
    site_data = await _get_all_cards_data(db_df['CD_CARD'].tolist(), client)
    site_df = pd.DataFrame([item for item in site_data if item is not None])

    if site_df.empty:
        return None

    # Compara versões usando merge e query
    result_df = pd.merge(db_df, site_df, on='CD_CARD')
    return result_df


async def _get_all_info_cards_data(session: Session, client: httpx.AsyncClient):
    """Busca todos os dados definidos de InfoCards."""
    info_cards = get_info_cards(session)
    ic_df = pd.DataFrame(info_cards)
    ic_df.columns = ic_df.columns.str.upper()

    compared_df: pd.DataFrame = await _compare_versions(session, client)

    ic_df = (
        pd.merge(ic_df, compared_df, on=['CD_CARD', 'CD_VERS'], how='left')
        .query('CD_VERS != SITE_VERS')
        .rename(columns={'CD_VERS': 'DB_VERS'})
    )

    ic_df['LINK_CARD'] = URL_SITE + ic_df['CD_CARD'].astype(str)
    ic_df.fillna({'SITE_VERS': -1}, inplace=True)
    ic_df = ic_df.sort_values(by='CD_CARD')

    return ic_df.to_dict(orient='records')


async def get_all_versions_data(session: Session, token: str):
    """Busca dados de versões de cartões."""
    try:
        async with httpx.AsyncClient(
            verify=False, timeout=30, limits=httpx.Limits(max_connections=5)
        ) as client:
            client.cookies.set('BBSSOToken', token)
            data = await _get_all_info_cards_data(session, client)
        data = {'versoes': data, 'exec': datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S')}
        return data
    except Exception:
        return None
