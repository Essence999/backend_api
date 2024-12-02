from sqlalchemy.orm import Session
from sqlalchemy.sql import text


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
    result = session.execute(query).mappings().all()
    data = [dict(row) for row in result]
    return data


def get_info_cards(session: Session) -> list[dict]:
    """Busca todos os registros definidos de InfoCards.

    Args:
        session (Session): Sessão do banco de dados.

    Returns:
        list[dict]: Lista de registros de InfoCards.
    """
    # query = text(
    #     """
    #     SELECT DISTINCT CD_CARD, NM_CARD, VL_RGUA_MAX_CARD, QT_PTO_FXA_RGUA_CARD,
    #     VL_META_CARD, REF_AA, REF_MM, CD_IND_ATB, NM_IND_ATB, TIP_ACRD, CD_VERS
    #     FROM DB2ATB.INFO_CARDS
    #     WHERE CD_CARD < 10000
    #     AND REF_AA = YEAR(CURRENT DATE)
    #     AND REF_MM = MONTH(CURRENT DATE)
    #     """
    # )
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
    result = session.execute(query).mappings().all()
    d_list = [dict(row) for row in result]
    return d_list
