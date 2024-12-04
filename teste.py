import httpx

with httpx.Client(verify=False, timeout=10) as c:
    c.cookies.set(
        'BBSSToken',
        '3M7BmbHT4vTvvM975KYfaT6rgok.*AAJTSQACMDMAAlNLABxlOTdLRVdJVWFwUngyNHFQSFhMWUN5aDhrQ2c9AAR0eXBlAANDVFMAAlMxAAIyNA..*')
    response = c.get(
        'https://portaldarede.intranet.bb.com.br/varejo/api/publico/conteudos/8530')

print(response.json())
print(response.status_code)
