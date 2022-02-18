import ldap
from fastapi import HTTPException, status


def auth_ldap(username: str, password: str) -> str:
    address = "ldap://156.54.242.110:389"
    try:
        con = ldap.initialize(address)
        con.protocol_version = ldap.VERSION3
    except ldap.SERVER_DOWN:
        raise HTTPException(status_code=500, detail="Can't contact LDAP SERVER!")
    base_dn = "O=Telecom Italia Group"
    search_filter = f"(uid={username})"
    try:
        result = con.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, None)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except:
        raise HTTPException(status_code=500, detail="LDAP search failed!")
    user_dn = result[0][0]  # get the user DN
    # print(f"user_dn={user_dn}")
    try:
        con.simple_bind_s(user_dn, password)
    except ldap.INVALID_CREDENTIALS:
        raise HTTPException(status_code=400, detail="Incorrect credentials!")
    return 1
