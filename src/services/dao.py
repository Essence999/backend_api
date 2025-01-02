import logging

from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def execute_query(session: Session, query: str, params: dict | None = None) -> list[dict]:
    """Executa uma query e retorna os resultados em forma de dicionário."""
    try:
        logging.debug(f'Executando query: {query} com parâmetros: {params}')
        result = session.execute(query, params).mappings().all()
        data = [dict(row) for row in result]
        logging.info(f'Query executada com sucesso. Retornando {len(data)} registros.')
        return data
    except Exception as e:
        logging.error(f'Erro ao executar a query: {e}', exc_info=True)
        session.rollback()
        return []  # Retorna uma lista vazia em caso de erro


def get_info_cards(session: Session) -> list[dict]:
    """Busca todos os registros definidos de InfoCards do mês/ano atual."""
    query = text(
        """
        SELECT DISTINCT CD_CARD, NM_CARD, VL_RGUA_MAX_CARD, QT_PTO_FXA_RGUA_CARD,
        VL_META_CARD, CD_IND_ATB, NM_IND_ATB, TIP_ACRD, CD_VERS
        FROM DB2ATB.INFO_CARDS
        WHERE CD_CARD < 10000
        AND REF_AA = YEAR(CURRENT DATE)
        AND REF_MM = MONTH(CURRENT DATE)
        """
    )
    return execute_query(session, query)


def get_ocr_meta(session: Session) -> list[dict]:
    """Busca dados de meta OCR."""
    query = text(
        """
        SELECT VL_META_IN_MBZ, VL_META_CARD, CD_PRF_CARD, CD_IND_ATB,
        NM_IN_MBZ, AA_APRC, MM_APRC, TS_ATU
        FROM DB2ATB.VS_DVGA_ATB_CARD
        WHERE OCR_META = 1
        ORDER BY CD_PRF_CARD ASC
        """
    )
    return execute_query(session, query)


def get_regua_cards(session: Session) -> list[dict]:
    """Busca dados de régua OCR."""
    query = text(
        """
        SELECT RGUA_ATB, RGUA_CARD, CD_PRF_CARD, CD_IND_ATB,
        NM_IN_MBZ, AA_APRC, MM_APRC, TS_ATU
        FROM DB2ATB.VS_DVGA_ATB_CARD
        WHERE OCR_RGUA = 1
        ORDER BY CD_PRF_CARD ASC
        """
    )
    return execute_query(session, query)


def get_ocr_cards(session: Session, card_type: str) -> list[dict]:
    """Busca dados de OCR com base no tipo (meta ou régua)."""
    logging.info(f'Buscando dados de OCR para o tipo: {card_type}')
    if card_type == 'meta':
        return get_ocr_meta(session)
    return get_regua_cards(session)


def update_card(session: Session, query: str, params: dict) -> bool:
    """Executa uma query de atualização."""
    try:
        logging.debug(f'Executando query de atualização: {query} com parâmetros: {params}')
        session.execute(query, params)
        session.commit()
        logging.info('Query de atualização executada com sucesso.')
        return True
    except Exception as e:
        logging.error(f'Erro ao executar a query de atualização: {e}', exc_info=True)
        session.rollback()
        return False  # Retorna False em caso de erro


def update_meta_card(session: Session, new_value: float, ind: str, prf: str) -> bool:
    """Atualiza o valor da meta de um cartão."""
    query = text(
        """
        UPDATE DB2ATB.INFO_CARDS SET VL_META_CARD = :meta, TS_ATU = CURRENT_DATE
        WHERE CD_IND_ATB = :ind AND
        CD_PRF_CARD = :prf AND
        REF_AA = YEAR(CURRENT_DATE) AND
        REF_MM = MONTH(CURRENT_DATE)
        """
    )
    params = {'meta': new_value, 'ind': ind, 'prf': prf}
    return update_card(session, query, params)


def update_regua_card(session: Session, vl: float, qt: float, ind: str, prf: str) -> bool:
    """Atualiza os valores de régua de um cartão."""
    vl_query = text(
        """
        UPDATE DB2ATB.INFO_CARDS SET VL_RGUA_MAX_CARD = :vl, TS_ATU = CURRENT_DATE
        WHERE CD_IND_ATB = :ind AND
        CD_PRF_CARD = :prf AND
        REF_AA = YEAR(CURRENT_DATE) AND
        REF_MM = MONTH(CURRENT_DATE)
        """
    )
    qt_query = text(
        """
        UPDATE DB2ATB.INFO_CARDS SET QT_PTO_FXA_RGUA_CARD = :qt, TS_ATU = CURRENT_DATE
        WHERE CD_IND_ATB = :ind AND
        CD_PRF_CARD = :prf AND
        REF_AA = YEAR(CURRENT_DATE) AND
        REF_MM = MONTH(CURRENT_DATE)
        """
    )

    vl_params = {'vl': vl, 'ind': ind, 'prf': prf}
    qt_params = {'qt': qt, 'ind': ind, 'prf': prf}

    try:
        success_vl = update_card(session, vl_query, vl_params)
        success_qt = update_card(session, qt_query, qt_params)
        if success_vl and success_qt:
            logging.info('Régua atualizada com sucesso.')
            return True
        else:
            logging.warning('Erro ao atualizar a régua. Uma ou mais operações falharam.')
            return False
    except Exception as e:
        logging.error(f'Erro ao atualizar a régua: {e}', exc_info=True)
        return False
