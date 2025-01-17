import pandas as pd
from sqlalchemy.orm import Session

from src.services.dao import get_ocr_cards


def get_ocr_cards_data(session: Session, card_type: str):
    data = get_ocr_cards(session, card_type)

    if data:
        df = pd.DataFrame(data)
        # df.columns = df.columns.str.upper()
        df['Nome indicador'] = df['Nome indicador'].str.strip()
        df = df.convert_dtypes()
        data = df.to_dict(orient='records')
    data = {card_type: data}

    return data
