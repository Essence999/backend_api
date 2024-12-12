import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from src.services.dao import get_ocr_cards


def get_ocr_cards_data(session: Session, type: str):
    data = get_ocr_cards(session, type)

    if data:
        df = pd.DataFrame(data)
        df.columns = df.columns.str.upper()
        df['NM_IN_MBZ'] = df['NM_IN_MBZ'].str.strip()
        df['TS_ATU'] = df['TS_ATU'].astype(str)
        data = df.replace({np.nan: None}).to_dict(orient='records')
    data = {type: data}

    return data
