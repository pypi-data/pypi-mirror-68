A simple lightweight API to interact with Oracle ERP integration Service.

Usage:
    >>> import OracleSaaSApi
    >>> erp = OracleSaaSApi.ErpServiceApi(url, username, password)
    >>> docId = erp.upload_file_to_ucm()
