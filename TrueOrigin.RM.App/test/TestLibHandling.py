from unittest import result
from Libraries.LibHandling import LibHandling

if __name__ == '__main__':
    lib = LibHandling()
    data = lib.Login("trantrungbk95@gmail.com", "12345678")
    print(data)
    if lib.Sealer is not None:
        print("Sealer: " + lib.Sealer.Info.Username)
    else:
        print("Sealer không được khởi tạo")

    response = lib.GetAllOrders()
    r1 = lib.SelectOder(8)

    r2 = lib.GetCurrentSeri(8)
    print(r2.no_number)
    r3 = lib.UpdateSeriReleased(8, r2.no_number, True)
   
    print(str(r3))
    # lib.UpdateSeriReleased(order_id= 9, no_number= 115, IsReleased= True)
    # lib.UpdateSeriReleased(order_id= 8, no_number= 123, IsReleased= True)
