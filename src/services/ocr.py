import pandas as pd
from sqlalchemy.orm import Session

from src.services.dao import get_ocr_cards, update_meta_card, update_regua_card


def get_ocr_cards_data(session: Session, type: str):
    data = get_ocr_cards(session, type)
    if data:
        df = pd.DataFrame(data)
        df.columns = df.columns.str.upper()
        df['NM_IN_MBZ'] = df['NM_IN_MBZ'].str.strip()
        df['TS_ATU'] = df['TS_ATU'].astype(str)
        data = df.to_dict(orient='records')
        data = {type: data}
    return data


def update_ocr_card(
    session: Session, type: str, new_value: str, ind: str, prf: str
) -> dict:
    if type == 'meta':
        return update_meta_card(session, new_value, ind, prf)
    elif type == 'regua':
        return update_regua_card(session, new_value, ind, prf)
    else:
        return {'sucess': False, 'message': 'Tipo inválido.'}
