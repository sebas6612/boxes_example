from algopy import ARC4Contract, BoxMap, Global, Txn, subroutine, UInt64, gtxn
from algopy.arc4 import abimethod, Struct, Address, String


class NameKey(Struct):
    owner: Address

class NameValue(Struct):
    name: String

class HelloWorld(ARC4Contract):
    def __init__(self) -> None:
        self.names_list = BoxMap(NameKey, NameValue)

    @subroutine
    def get_box_mbr(self) -> UInt64:
        # 2.500 + 400 * (# box Bytes = prefix + key bytes + value bytes)
        return (
            2_500
            + (
                self.names_list.key_prefix.length
                + 32 #address
                + 32 #name limited to 32 bytes
            )
            * 400
        )

    @abimethod()
    def save_name_on_boxes(self, user_name: String, mbr_pay: gtxn.PaymentTransaction) -> None:
        assert mbr_pay.sender == Txn.sender
        assert mbr_pay.receiver == Global.current_application_address
        assert mbr_pay.amount == self.get_box_mbr()

        box_key = NameKey(
            owner=Address(Txn.sender)
        )
        
        self.names_list[box_key] = NameValue(
            name=user_name
        )

    @abimethod()
    def get_name_on_box(self) -> String:
        box_key = NameKey(
            owner=Address(Txn.sender)
        )
        return self.names_list[box_key].name
    
    @abimethod()
    def get_mbr_calc(self) -> UInt64:
        return self.get_box_mbr()

