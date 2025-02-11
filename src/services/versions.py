import asyncio
import logging
from datetime import datetime

import httpx
import pandas as pd
from sqlalchemy.orm import Session

from src.services.dao import get_info_cards

URL_API = 'https://portaldarede.intranet.bb.com.br/varejo/api/publico/conteudos'
URL_SITE = 'https://portaldarede.intranet.bb.com.br/varejo/artigos/'


async def _get_card_data(card_number: int, client: httpx.AsyncClient) -> dict | None:
    """Busca dados de um card no site."""
    logging.debug(f'Iniciando busca de dados para o card {card_number}')
    url = f'{URL_API}/{card_number}'
    try:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        logging.debug(f'Dados do card {card_number} obtidos com sucesso')
        return {'CD_CARD': data['id'], 'SITE_VERS': data['versao']}
    except httpx.HTTPStatusError as e:
        logging.error(f'Erro ao buscar card {card_number}: {e.response.status_code} - {e.response.text}')
    except httpx.RequestError as e:
        logging.error(f'Erro de conexão ao buscar card {card_number}: {e!s}')
    return None


async def _get_all_cards_data(card_numbers: list[int], client: httpx.AsyncClient) -> list[dict]:
    """Busca dados de vários cards no site."""
    card_numbers = set(card_numbers)
    logging.info(f'Iniciando busca de dados para {len(card_numbers)} cards.')
    logging.info(f'Cards: {card_numbers}')
    tasks = [_get_card_data(card, client) for card in card_numbers]
    site_data = await asyncio.gather(*tasks)
    return [item for item in site_data if item is not None]


async def _compare_versions(db_df: pd.DataFrame, client: httpx.AsyncClient) -> pd.DataFrame:
    """Compara versões do banco com o site."""
    logging.debug('Iniciando comparação de versões.')
    try:
        site_data = await _get_all_cards_data(db_df['CD_CARD'].tolist(), client)
        logging.info(f'Busca concluída com {len(site_data)} resultados.')
        if not site_data:
            logging.warning('Nenhum dado válido encontrado no site.')
            return pd.DataFrame()

        site_df = pd.DataFrame(site_data)
        logging.debug('Comparação de versões concluída.')
        return pd.merge(db_df, site_df, on='CD_CARD')
    except Exception as e:
        logging.error(f'Erro ao comparar versões: {e!s}')
        return pd.DataFrame()


async def _get_all_info_cards_data(session: Session, client: httpx.AsyncClient) -> list[dict]:
    """Busca todos os dados definidos de InfoCards."""
    logging.debug('Iniciando processamento de InfoCards.')
    try:
        info_cards = get_info_cards(session)
        db_df = pd.DataFrame(info_cards)
        db_df.columns = db_df.columns.str.upper()

        comp_df = await _compare_versions(db_df, client)
        if comp_df.empty:
            logging.warning('Nenhuma comparação de versões disponível.')
            return []

        comp_df = comp_df.query('CD_VERS != SITE_VERS').rename(columns={'CD_VERS': 'DB_VERS'})
        comp_df = comp_df.rename(
            columns={
                'CD_VERS': 'DB_VERS',
                'VL_RGUA_MAX_CARD_CLTO': 'VL_RGUA',
                'QT_PTO_FXA_RGUA_CARD_CLTO': 'QT_RGUA',
                'VL_META_CARD': 'META',
            }
        )

        comp_df['LINK_CARD'] = URL_SITE + comp_df['CD_CARD'].astype(str)
        comp_df.fillna({'SITE_VERS': -1}, inplace=True)

        logging.info(f'Comparação de versões finalizada com {len(comp_df)} cards.')

        comp_df = comp_df.convert_dtypes()

        comp_df = comp_df.rename(
            columns={
                'CD_CARD': 'Código card',
                'NM_CARD': 'Nome card',
                'VL_RGUA': 'Régua vl',
                'QT_RGUA': 'Régua qt',
                'META': 'Meta',
                'CD_IND_ATB': 'Código indicador',
                'NM_IND_ATB': 'Nome indicador',
                'TIP_ACRD': 'Tipo acordo',
                'DB_VERS': 'Versão',
                'SITE_VERS': 'Versão site',
                'LINK_CARD': 'Link',
            }
        )

        return comp_df.to_dict(orient='records')
    except Exception as e:
        logging.error(f'Erro ao processar InfoCards: {e!s}')
        return []


async def get_all_versions_data(session: Session, token: str) -> list[dict]:
    """Busca dados de versões de cartões."""
    logging.debug('Iniciando busca de dados de versões de cartões.')
    try:
        async with httpx.AsyncClient(
            verify=False, timeout=30, limits=httpx.Limits(max_connections=5)
        ) as client:
            client.cookies.set('BBSSOToken', token)
            data = await _get_all_info_cards_data(session, client)
        return {'versoes': data, 'exec': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    except httpx.RequestError as e:
        logging.error(f'Erro de conexão ao buscar dados: {e!s}')
    except Exception as e:
        logging.error(f'Erro inesperado ao buscar dados: {e!s}')
    return []
