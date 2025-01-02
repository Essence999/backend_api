from sqlalchemy.orm import Session
from sqlalchemy.sql import text


def get_dict_from_query(session: Session, query: str, params: dict | None = None) -> list[dict] | None:
    """Executa uma query e retorna os resultados em forma de dicionário."""
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


def get_ocr_meta(session: Session) -> list[dict] | None:
    query = text(
        """
        SELECT VL_META_IN_MBZ, VL_META_CARD, CD_PRF_CARD, CD_IND_ATB,
        NM_IN_MBZ, AA_APRC, MM_APRC, TS_ATU
        FROM DB2ATB.VS_DVGA_ATB_CARD
        WHERE OCR_META = 1
        ORDER BY NM_IN_MBZ ASC
        """
    )
    return get_dict_from_query(session, query)


def get_regua_cards(session: Session) -> list[dict] | None:
    query = text(
        """
        SELECT RGUA_ATB, RGUA_CARD, CD_PRF_CARD, CD_IND_ATB,
        NM_IN_MBZ, AA_APRC, MM_APRC, TS_ATU
        FROM DB2ATB.VS_DVGA_ATB_CARD
        WHERE OCR_RGUA = 1
        ORDER BY NM_IN_MBZ ASC
        """
    )
    return get_dict_from_query(session, query)


def get_ocr_cards(session: Session, type: str) -> list[dict] | None:
    if type == 'meta':
        data = get_ocr_meta(session)
    else:
        data = get_regua_cards(session)

    if data is not None:
        return data
    return None


def update_meta_card(session: Session, new_value: float, ind: str, prf: str) -> bool:
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
        session.execute(query, params)
        session.commit()

        return True
    except Exception as e:
        print(str(e))
        session.rollback()
        return False


def update_regua_card(session: Session, vl: float, qt: float, ind: str, prf: str) -> bool:
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
        session.execute(vl_query, vl_params)
        session.execute(qt_query, qt_params)

        session.commit()
        return True
    except Exception as e:
        print(str(e))
        session.rollback()
        return False
