

def updateScript(novo_valor,df,index_para_alterar):
    
    # script para dar update no db2
    # sql_update = f"""
    #     UPDATE DB2ATB.INFO_CARDS SET VL_META_CARD = {novo_valor}, TS_ATU = CURRENT_DATE
    #     WHERE CD_IND_ATB = {df.loc[index_para_alterar, 'CD_IND_ATB']} AND
    #     CD_PRF_CARD = {df.loc[index_para_alterar, 'CD_PRF_CARD']} AND
    #     REF_AA = YEAR(CURRENT_DATE) AND 
    #     REF_MM = MONTH(CURRENT_DATE)
    # """
    
    sql_update = f"""
            UPDATE DB2ATB.INFO_CARDS SET VL_META_CARD = {novo_valor}, TS_ATU = CURRENT_DATE
            WHERE CD_IND_ATB = {df.loc[index_para_alterar, 'CD_IND_ATB']} AND
            CD_PREFS_CARD = {df.loc[index_para_alterar, 'CD_PREFS_CARD']}
        """
    return sql_update

def sql_gera_coluna(coluna):
    sql_query_db2 = f"""
                SELECT
                {coluna}
            FROM
                DB2ATB.VS_DVGA_ATB_CARD
            WHERE
                OCR_META = 1
    """
    return sql_query_db2

def sql_select_atb(coluna_pref, coluna_in):
    sql_query = f"""
    SELECT
               VL_META_IN_MBZ,
                VL_META_CARD,
               CD_PRF_CARD,
               -- CD_PREF_DEP,
               -- CD_IN_MBZ,
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


#     sql_query = f"""
#                     SELECT VL_META_CARD,
# --                 VL_META_IN_MBZ,
#                CD_PRF_CARD,
#                  CD_IND_ATB,
#                  NM_CARD,
#                 REF_AA ,
#                 REF_MM,
#                 TS_ATU
#                     FROM DB2ATB.INFO_CARDS
#                     WHERE CD_PRF_CARD IN (coluna_pref) AND 
#                     CD_IND_ATB IN (coluna_in) AND 
#                     REF_AA = YEAR(CURRENT_DATE) AND 
#                     REF_MM = MONTH(CURRENT_DATE)
#                     """
    return sql_query