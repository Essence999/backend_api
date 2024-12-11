

def updateScript(novo_valor, cd_prf, cd_in):
    
    # script para dar update no db2
    # sql_update = f"""
    #     UPDATE DB2ATB.INFO_CARDS SET VL_META_CARD = {novo_valor}, TS_ATU = CURRENT_DATE
    #     WHERE CD_IND_ATB = {cd_in} AND
    #     CD_PRF_CARD = {cd_prf} AND
    #     REF_AA = YEAR(CURRENT_DATE) AND 
    #     REF_MM = MONTH(CURRENT_DATE)
    # """
    
    sql_update = f"""
            UPDATE DB2ATB.INFO_CARDS SET VL_META_CARD = {novo_valor}, TS_ATU = CURRENT_DATE
            WHERE CD_IND_ATB = {cd_in} AND
            CD_PREFS_CARD = {cd_prf}
        """
    return sql_update

def sql_select_atb():
    sql_query = f"""
    SELECT
               VL_META_IN_MBZ,
                VL_META_CARD,
               CD_PRF_CARD,
                 CD_IND_ATB,
                 NM_IN_MBZ,
                AA_APRC,
                MM_APRC,
                TS_ATU
            FROM
                DB2ATB.VS_DVGA_ATB_CARD
            WHERE
                OCR_META = 1
            ORDER BY NM_IN_MBZ ASC
"""
    return sql_query


def select_regua():
    sql_query = f"""
        SELECT
            VL_META_IN_MBZ,
                VL_META_CARD,
               CD_PRF_CARD,
                 CD_IND_ATB,
                 NM_IN_MBZ,
                AA_APRC,
                MM_APRC,
                TS_ATU
        FROM
            DB2ATB.VS_DVGA_ATB_CARD
        WHERE
            OCR_RGUA = 1
        ORDER BY NM_IN_MBZ ASC
    """
    return sql_query