import asyncio
from datetime import datetime

import httpx
import pandas as pd
from sqlalchemy.orm import Session

from src.services.dao import get_info_cards

URL_API = 'https://portaldarede.intranet.bb.com.br/varejo/api/publico/conteudos'
URL_SITE = 'https://portaldarede.intranet.bb.com.br/varejo/artigos/'


async def _get_card_data(card_number: int, client: httpx.AsyncClient) -> dict | None:
    """Busca dados de um card no site."""
    url = f'{URL_API}/{card_number}'
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return {'CD_CARD': data['id'], 'SITE_VERS': data['versao']}
    except httpx.HTTPStatusError as e:
        print(
            f'Erro ao buscar card {card_number}: {e.response.status_code} - {e.response.text}')
    except httpx.RequestError as e:
        print(f'Erro de conexão ao buscar card {card_number}: {e!s}')
    return None


async def _get_all_cards_data(card_numbers: list[int], client: httpx.AsyncClient) -> list[dict]:
    """Busca dados de vários cards no site."""
    tasks = [_get_card_data(card, client) for card in card_numbers]
    site_data = await asyncio.gather(*tasks)
    return [item for item in site_data if item is not None]


async def _compare_versions(db_df: pd.DataFrame, client: httpx.AsyncClient) -> pd.DataFrame:
    """Compara versões do banco com o site."""
    try:
        site_data = await _get_all_cards_data(db_df['CD_CARD'].tolist(), client)
        if not site_data:
            print('Nenhum dado válido encontrado no site.')
            return pd.DataFrame()

        site_df = pd.DataFrame(site_data)
        return pd.merge(db_df, site_df, on='CD_CARD')
    except Exception as e:
        print(f'Erro ao comparar versões: {e!s}')
        return pd.DataFrame()


async def _get_all_info_cards_data(session: Session, client: httpx.AsyncClient) -> list[dict]:
    """Busca todos os dados definidos de InfoCards."""
    try:
        info_cards = get_info_cards(session)
        ic_df = pd.DataFrame(info_cards)
        ic_df.columns = ic_df.columns.str.upper()

        db_df = ic_df[['CD_CARD', 'CD_VERS']]

        compared_df = await _compare_versions(db_df, client)
        if compared_df.empty:
            print('Nenhuma comparação de versões disponível.')
            return []

        ic_df = pd.merge(ic_df, compared_df, on=[
                         'CD_CARD', 'CD_VERS'], how='left')
        ic_df = ic_df.query('CD_VERS != SITE_VERS').rename(
            columns={'CD_VERS': 'DB_VERS'})
        ic_df['LINK_CARD'] = URL_SITE + ic_df['CD_CARD'].astype(str)
        ic_df.fillna({'SITE_VERS': -1}, inplace=True)
        ic_df = ic_df.sort_values(by='CD_CARD')

        return ic_df.to_dict(orient='records')
    except Exception as e:
        print(f'Erro ao processar InfoCards: {e!s}')
        return []


async def get_all_versions_data(session: Session, token: str) -> dict | None:
    """Busca dados de versões de cartões."""
    try:
        async with httpx.AsyncClient(
            verify=False, timeout=30, limits=httpx.Limits(max_connections=10)
        ) as client:
            client.cookies.set('BBSSOToken', token)
            data = await _get_all_info_cards_data(session, client)
        return {'versoes': data, 'exec': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    except httpx.RequestError as e:
        print(f'Erro de conexão ao buscar dados: {e!s}')
    except Exception as e:
        print(f'Erro inesperado ao buscar dados: {e!s}')
    return None
