from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_dict_from_query(
    session: Session, query: str, params: dict | None = None
) -> list[dict] | None:
    try:
        query_result = session.execute(query, params).mappings().all()
        data = [dict(row) for row in query_result]
        return data
    except Exception as e:
        print(str(e))
        return None


def get_current_cards(session: Session) -> list[dict]:
    """Busca cartões e versão do mês/ano atual com número menor que MAX_CARD_NUMBER.

    Args:
        session (Session): Sessão do banco de dados.

    Returns:
        list[dict]: Lista de cartões com CD_CARD e CD_VERS do mês/ano atual.
    """
    query = text(
        """
        SELECT DISTINCT CD_CARD, CD_VERS
        FROM DB2ATB.INFO_CARDS
        WHERE CD_CARD < 10000
        AND REF_AA = YEAR(CURRENT DATE)
        AND REF_MM = MONTH(CURRENT DATE)
        """
    )
    return get_dict_from_query(session, query)


def get_info_cards(session: Session) -> list[dict]:
    """Busca todos os registros definidos de InfoCards.

    Args:
        session (Session): Sessão do banco de dados.

    Returns:
        list[dict]: Lista de registros de InfoCards.
    """
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
    return get_dict_from_query(session, query)


def get_ocr_cards(session: Session, type: str) -> list[dict] | None:
    if type == 'meta':
        ocr = 'OCR_META'
    elif type == 'regua':
        ocr = 'OCR_RGUA'
    else:
        return None

    query = text(
        f"""
        SELECT VL_META_IN_MBZ, VL_META_CARD, CD_PRF_CARD, CD_IND_ATB,
        NM_IN_MBZ, AA_APRC, MM_APRC, TS_ATU
        FROM DB2ATB.VS_DVGA_ATB_CARD
        WHERE {ocr} = 1
        ORDER BY NM_IN_MBZ ASC
        """
    )
    data = get_dict_from_query(session, query)
    if data is not None:
        return data
    return

def get_dev_query(session: Session) -> list[dict] | None:
    query = text(
        f"""
            SELECT  DISTINCT *
                        FROM DB2ATB.INFO_CARDS
                        ORDER BY NM_CARD ASC
        """
    )
    data = get_dict_from_query(session, query)
    if data is not None:
        return data
    return

def update_meta_card(session: Session, new_value: str, ind: str, prf: str) -> dict:
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
    try:
        result = session.execute(query, params)
        session.commit()

        if result.rowcount > 0:
            return {'sucess': True, 'message': 'Atualizado com sucesso.'}
        else:
            return {'sucess': False, 'message': 'Nenhuma linha foi alterada.'}
    except Exception as e:
        session.rollback()
        return {'sucess': False, 'message': str(e)}


def update_regua_card(session: Session, new_value: str, ind: str, prf: str) -> dict:
    query = text(
        """
        UPDATE DB2ATB.INFO_CARDS SET VL_META_CARD = :regua, TS_ATU = CURRENT_DATE
        WHERE CD_IND_ATB = :ind AND
        CD_PRF_CARD = :prf AND
        REF_AA = YEAR(CURRENT_DATE) AND
        REF_MM = MONTH(CURRENT_DATE)
        """
    )
    params = {'regua': new_value, 'ind': ind, 'prf': prf}
    try:
        result = session.execute(query, params)
        session.commit()

        if result.rowcount > 0:
            return {'sucess': True, 'message': 'Atualizado com sucesso.'}
        else:
            return {'sucess': False, 'message': 'Nenhuma linha foi alterada.'}
    except Exception as e:
        session.rollback()
        return {'sucess': False, 'message': str(e)}
