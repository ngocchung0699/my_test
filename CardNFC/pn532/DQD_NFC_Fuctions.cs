using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using TrueOrigin.Fuction;
using TrueOrigin.NFC_Config;
using TrueOrigin.Services;
using Xamarin.Forms;
using static TrueOrigin.Class.DQD_NFC_Para;

namespace TrueOrigin.Class.NFC
{
    public class DQD_NFC_Fuctions
    {
        //public static byte[] pwdNFC = new byte[6] { 0x01, 0x02, 0x03, 0x04, 0x05, 0x06};

        const int NUM_TRY = 10; //số lần cố gắng ghi lại NFC
        public static async Task<bool> TryConnect()
        {
            if (await GetInfoTag()) //lấy thông tin của thẻ NFC
            {
                DQD_Debug.WriteLine("Get info OK");

                var pwdNFC = await CreatePwd(); //tạo pwd từ UID của thẻ
                if (pwdNFC != null)
                {
                    bool isResetPwd = await OpenSecurity(pwdNFC);

                    if (isResetPwd) DQD_Debug.WriteLine("reset pwd OK");
                    else DQD_Debug.WriteLine("reset pwd Err");

                    return isResetPwd;
                }
                else return false;
            }
            else return false;
        }


        public static async Task<bool> Close(bool result)
        {
            try
            {
                await DependencyService.Get<DQD_NFC>().EndSession(result); //đóng session

                DQD_Debug.WriteLine("Close NFC OK");
                return true;
            }
            catch (Exception ex)
            {
                DQD_Debug.WriteLine("Close NFC Err: " + ex);
                return false;
            }
        }


        public static async Task<bool> GetInfoTag()
        {
            try
            {
                byte[] isBegan = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] { //lấy được thông tin get_version
                        (byte) 0x60    // địa chỉ GET_VERSION
                });

                DQD_NFC_Process NFCprocess = new DQD_NFC_Process();
                NFCprocess.ResetStatus();
                var nameNFC = NFCprocess.GetInfoTag(isBegan);       //lấy version của thẻ NFC đang được quét
                if (nameNFC == null) return false;
                else return true;
            }
            catch
            {
                return false;
            }
        }

        public static async Task<byte[]> Transceive(byte[] data) // hàm gửi 1 lệnh thao tác với thanh ghi NFC
        {
            return await DependencyService.Get<DQD_NFC>().Transceive(data);
        }

        public static async Task<bool> WritePage(int page, byte[] data) //ghi giữ liệu vào 1 page
        {
            byte[] byteTrans = new byte[6];
            byteTrans[0] = DQD_NFC_Command.WRITE;

            byteTrans[1] = (byte)page;
            byteTrans[2] = data[0];
            byteTrans[3] = data[1];
            byteTrans[4] = data[2];
            byteTrans[5] = data[3];

            if (await Transceive(byteTrans) != null) //nếu gửi thành công
            {
                return true;
            }
            else return false;
            //else
            //{
            //    int try_transceive = 0;
            //    bool done = false;
            //    while (!done && try_transceive < NUM_TRY)  //chờ ghi thành công
            //    {
            //        Thread.Sleep(10);
            //        if (await Transceive(byteTrans) != null) done = true;
            //        else done = false;
            //        try_transceive++;
            //    }
            //    if (done) //nếu có lần thử thành công
            //    {
            //    }
            //    else //nếu thử tất cả đều lỗi
            //    {
            //        return false;
            //    }

            //}
        }

        static async Task<bool> IsProtectedPwd()
        {
            try
            {
                byte[] response = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                    (byte) DQD_NFC_Command.READ,    // READ
                    (byte)DQD_NFC_Register.AUTH0,   // page address
                });
                if (response[3] == (byte)0xFF) //nếu thẻ chưa được bảo vệ mật khẩu
                {
                    return false;
                }
                else return true;
            }
            catch
            {
                return true;
            }
        }

        static async Task ReadPackPwd()
        {
            //2. Đặt PACK (trang 44, byte 0-1) thành xác nhận mật khẩu mong muốn của bạn (giá trị mặc định
            byte[] result2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte)DQD_NFC_Command.READ,  
                (byte)0x00
            });

            DQD_Debug.WriteLine("Đọc pack pwd===== " + Utils.HexDump(result2, 16));
        }    

        static async Task<byte[]> CreatePwd()
        { 
            /* Mật khẩu của thẻ được Gen từ UID của thẻ -> mỗi thẻ sẽ có 1 pwd khác nhau- pwd này là pwd tĩnh
             * Việc sử dụng roll pwd là không có ý nghĩa trong trường hợp này, với lý do thẻ là thụ động và nó ko tự ý roll pwd được 
             * Mỗi thẻ có 1 pwd riêng sẽ đảm bảo tính an toàn riêng tư, khi 1 thẻ bị lộ pwd cũng ko ảnh hưởng đến các thẻ khác
             * 
             */
            byte[] pwd = new byte[6];

            //lấy UID của thẻ
            byte[] reponse = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte)DQD_NFC_Command.READ,
                (byte)0x00
            });

            if (reponse != null)
            {
                byte[] UIDbyte = new byte[] { reponse[0], reponse[1], reponse[2], reponse[3], reponse[4], reponse[5], reponse[6], reponse[7] };
                DQD_Debug.WriteLine("UID của tem: " + Utils.HexDump(UIDbyte, UIDbyte?.Length ?? 16));
                //hash UID
                var UIDhash = DQD_SHA256.getHashSha256(UIDbyte);
                DQD_Debug.WriteLine("Hash UID của tem: " + Utils.HexDump(UIDhash, UIDhash.Length));
                //lấy tùy chọn 4 byte pwd và 2 byte pack (2015/03/30 - thời gian thành lập công ty Onyx)
                pwd[0] = UIDhash[2];
                pwd[1] = UIDhash[0];
                pwd[2] = UIDhash[1];
                pwd[3] = UIDhash[5];
                pwd[4] = UIDhash[0];
                pwd[5] = UIDhash[3];
                return pwd;
            }
            else return null;
        }
        static async Task SetPwd(byte[] pwd)
        {
            /*Việc đặt mật khẩu cho NFC được gán mật khẩu và mã xác minh
             * sau khi gán xong cần đặt auth0= X- vị trí page đầu tiên cần bảo vệ, để xác nhận đặt mật khẩu (auth0 =0xff là xóa mật khẩu)
             * do auth0 là cài đặt vị trí thanh ghi đầu tiên được bảo vệ bởi mật khẩu
             */

            //1. Đặt PWD (trang 43) thành mật khẩu mong muốn của bạn (giá trị mặc định là 0xFFFFFFFF).
            byte[] result1 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte)DQD_NFC_Command.WRITE,  /* CMD = WRITE */
                (byte)DQD_NFC_Register.PWD,  /* PAGE = 43 */
                pwd[0], pwd[1], pwd[2], pwd[3]
            });

            //2. Đặt PACK (trang 44, byte 0-1) thành xác nhận mật khẩu mong muốn của bạn (giá trị mặc định
            byte[] result2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte)DQD_NFC_Command.WRITE,  /* CMD = WRITE */
                (byte)DQD_NFC_Register.PACK,  /* PAGE = 44 */
                pwd[4], pwd[5], 0, 0
            });

            //3. Đặt AUTHLIM (trang 42, byte 0, bit 2-0) thành số lần thử xác minh mật khẩu không thành công tối đa (đặt giá trị này thành 0 sẽ cho phép số lần thử PWD_AUTH không giới hạn).

            //4. Đặt PROT (trang 42, byte 0, bit 7) thành giá trị mong muốn (0 = PWD_AUTH chỉ cần cho truy cập ghi, 1 = PWD_AUTH cần thiết cho truy cập đọc và ghi).
            byte[] response = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte) DQD_NFC_Command.READ, // READ
                (byte) DQD_NFC_Register.PROT    // page address
            });
            if ((response != null) && (response.Length >= 16))
            { 
                bool prot = true;  // false = PWD_AUTH for write only, true = PWD_AUTH for read and write
                int authlim = 0; // value between 0 and 7, giới hạn số lần thử pass, 0=không giới hạn
                response = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                    (byte) DQD_NFC_Command.WRITE, // WRITE
                    (byte) DQD_NFC_Register.PROT,   // page address
                    (byte) ((response[0] & 0x078) | (prot ? 0x080 : 0x000) | (authlim & 0x007)),
                    response[1], response[2], response[3]  // keep old value for bytes 1-3
                });
            }

            //5. Đặt AUTH0 (trang 41, byte 3) thành trang đầu tiên yêu cầu xác thực mật khẩu.
            byte[] response2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte) DQD_NFC_Command.READ, // READ
                (byte) DQD_NFC_Register.AUTH0    // page address
            });
            if ((response2 != null) && (response2.Length >= 16))
            {  // read always returns 4 pages
                int auth0 = 2; // xác nhận đặt mật khẩu cho Tag NFC : auth0= địa chỉ thanh ghi đầu tiên cần được bảo vệ - page0,1 là ID cho phép đọc mà ko cần bảo vệ
                response2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                    (byte) DQD_NFC_Command.WRITE, // WRITE
                    (byte) DQD_NFC_Register.AUTH0,   // page address
                    response2[0], // keep old value for byte 0
                    response2[1], // keep old value for byte 1
                    response2[2], // keep old value for byte 2
                    (byte) (auth0 & 0x0ff)
                });
            }
        } //đặt mk cho tem- thao tác này chỉ cần sử dụng khi phát hành tem

        static async Task<bool> OpenSecurity(byte[] pwd) //điền mk, nếu đúng thì Reset vùng bảo vệ (để có thể đọc-ghi các thanh ghi User)
        {
            /*
             * 1. cần xác minh mật khẩu qua PWD_AUTH có đúng hay ko, nếu ko đúng thì việc đọc-ghi các thanh ghi bị vô hiệu hóa
             * 2. reset mật khẩu bằng cách đặt AUTH0 = 0xff (vị trí thanh ghi  cuối cùng)
             */
            bool confirm_pass = false;

            //xác minh mật khẩu đã lưu trong Tag NFC
            byte[] response = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
            (byte) DQD_NFC_Command.PWD_AUTH, // PWD_AUTH
            pwd[0], pwd[1], pwd[2], pwd[3]
            });
            if ((response != null) && (response.Length >= 2)) //trả về 2 bit xác minh mật khẩu (chính là 2 bit PACK)
            {
                int stamp_confirm = 0;
                // success
                for (int ii = 0; ii < response.Length; ii++)
                {
                    if (response[ii] == pwd[ii+4]) stamp_confirm++;
                }
                if (stamp_confirm == response.Length) confirm_pass = true; 
            }

            DQD_Debug.WriteLine("Kết quả check Pwd" + confirm_pass + " | " + Utils.HexDump(response, 8) + " | " + DQD_NFC_Command.PWD_AUTH);

            if (confirm_pass) // nếu reset pwd thành công
            {
                //Đặt AUTH0 (trang 41, byte 3) thành trang đầu tiên yêu cầu xác thực mật khẩu.
                byte[] response2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                    (byte) DQD_NFC_Command.READ, // READ
                    (byte) DQD_NFC_Register.AUTH0  // page address
                });
                if ((response2 != null) && (response2.Length >= 16))
                {  // read always returns 4 pages
                    int auth0 = 0xff; // =0xff tương ứng với việc vô hiệu hóa mật khẩu
                    response2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                        (byte) DQD_NFC_Command.WRITE, // WRITE
                        (byte) DQD_NFC_Register.AUTH0,   // page address
                        response2[0], // keep old value for byte 0
                        response2[1], // keep old value for byte 1
                        response2[2], // keep old value for byte 2
                        (byte) (auth0 & 0x0ff)
                    });
                }
            }
            return confirm_pass;
        }

        public static async Task<bool> CloseSecurity() //đóng khóa bảo mật- kéo thanh bảo vệ đến page 2 để bảo vệ (page1,2 là ID của tem- ko cần bảo vệ để có thể đọc ID tem)
        {
            //5. Đặt AUTH0 (trang 41, byte 3) thành trang đầu tiên yêu cầu xác thực mật khẩu.
            byte[] response2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                (byte) DQD_NFC_Command.READ, // READ
                (byte) DQD_NFC_Register.AUTH0    // page address
            });
            if ((response2 != null) && (response2.Length >= 16))
            {  // read always returns 4 pages
                int auth0 = 2; // xác nhận đặt mật khẩu cho Tag NFC : auth0= địa chỉ thanh ghi đầu tiên cần được bảo vệ - page0,1 là ID cho phép đọc mà ko cần bảo vệ
                response2 = await DependencyService.Get<DQD_NFC>().Transceive(new byte[] {
                    (byte) DQD_NFC_Command.WRITE, // WRITE
                    (byte) DQD_NFC_Register.AUTH0,   // page address
                    response2[0], // keep old value for byte 0
                    response2[1], // keep old value for byte 1
                    response2[2], // keep old value for byte 2
                    (byte) (auth0 & 0x0ff)
                });
                DQD_Debug.WriteLine("Đặt bảo vệ thành công");
                return true;
            }
            DQD_Debug.WriteLine("Đặt bảo vệ thất bại");
            return false;
        }
    }
