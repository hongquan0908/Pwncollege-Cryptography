import json
import base64

from Crypto.PublicKey import RSA
from Crypto.Hash.SHA256 import SHA256Hash

user_key = RSA.generate(1024)

key_e = 65537
key_n = 137605833569039211231393780859263095420434806255811214303245901542275652062093628626958169776358713851924026728202442918494054564263473581450936295703005061723880030351773536181465305956093161071551327876933841506979435509779460830950834916695941947745654345315615123146637589941463550303428736438831919073749
key_d = 5591936406194114459191136104390381599378564746033373765859280212436724756311257098139163307091983836094674217371639777571132197358357813384793415773243025590909138309876085098613233047318193290055148298638226178956030776072497758992562860253705511527887910781918417338415577728751529152823404234138154192377

# first generate the user key
# now we want to build our own cerificate and verify it
user_certificate = {
        "name": "Connor",
        "key": {
            "e": key_e,
            "n": key_n
        },
        "signer": "root", # The code only trust root as signer
    }
# json dump it as a string 
user_certificate_data = json.dumps(user_certificate).encode()
# encode it to make it byte string
user_certificate_data = base64.b64encode(user_certificate_data)

# After this send it to the server

root_key_d = 0x1b675d4cc54edb9a066d81f0a61f977294b7779abe9e0f5cf9a467d7789e12b8922f6eade5dbfead0e119b7b65e3f8bc439db084311b9a98d928fcbed6e45c410e559c5290bbd0a6e95e1068bfd1d1b6705cc37d00b9cf3f10ff9ecd7005f32ce34911be450e7856573466939b37a30d90ed0b4192a4749a6bc6a24072b7967dd5f89a1cd6a38863cafccc9998b6deed645863d614b337e614c5fb6f05c4ca9d925188f7736e4517c11c5ad2e0a1608cdd1ced1bf2aa9da0fc2f0dd8e4d377978938e10dd390f2be381d898f95bf7cad9e069979c498abf6f68a156505eb89812a321c3008569ff61b4d842c52c21b3e375e0bfe6f007bcd14c3e9b61bb72e55

# look at root certificate to get n
root_key_n = 24521211538330503868409571899247169836568271394920407942278090260102543296922834583966437611484972282648992596466908968289042419337737108482292614942858222585004320555073900967935868118974058679811325043755382273608733501519060987829321447988131260566930267277377059780682798083106201354049943716302582523271575357017979857890718049329217014352651026044815895198333218877061834682662277548220779528770354804624366902476079051614288962408395123137824638142473994263908697942455492657563113759030709988483465829867858559479707104981782002542440795294073368612446272297664971797753840532230160672970744980368218656499939

# now we need to sign our certificate
user_certificate_hash = SHA256Hash(json.dumps(user_certificate).encode()).digest()

user_certificate_signature = pow(
        int.from_bytes(user_certificate_hash, "little"),
        root_key_d,
        root_key_n
    ).to_bytes(256, "little")

# send this to server
# print(base64.b64encode(user_certificate_signature))

c = "NUX4k2PDMKj6F88BgTXZt7k4f69Zul1JucGCBaj0X4r0GjVzrJO/28Ifa0k2VU5g7vzRQuPbI2ts/AqoYm4NZ6rMfdzezGvfw5j2/otEpZ67sV3dvl9z/NGEG+DsLXv6CGCqhWyanMZEIGkXDPDg2SmOYlrL8s7mpe6j3YqNvkwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="

c = base64.b64decode(c)

plain_text = pow(
        int.from_bytes(c, "little"),
        key_d,
        key_n
    ).to_bytes(256, "little")

print(plain_text)

# pwn.college{sTOtRriqwjONldki3XiCZjtC57K.dVDOzMDL3UjN2MzW}
