using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;


namespace Demo
{
    class API
    {
        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_OpenDevice(int modules, IntPtr hWnd);

        [DllImport("lib\\A8Capture.dll")]
        public static extern void IO_CloseDevice();

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_Calibrate();

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CaptureFile(string irFileName,
                                                string whFileName,
                                                string uvFileName,
                                                int cardtype);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CaptureAndDecodeFile(string imgFileNameIr, string imgFileNameWh, string imgFileNameUv,
                                 int barType, bool muti,
                                 byte[] result, ref int resultSize);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CaptureAndRecognizeFile(string imgFileNameIr, string imgFileNameWh, string imgFileNameUv,

                               int cardType,ref CardDetails cardDetails);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_GetCardStatus(ref int status);

        /**************************************************************
        *  use callback mode for functions
        **************************************************************/
        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_OpenDeviceCB(int modules, IntPtr hWnd, CallbackResult callback);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CloseDeviceCB(CallbackResult callback);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CalibrateCB(CallbackResult callback);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CaptureAndDecodeFileCB(string imgFileNameIr, string imgFileNameWh, string imgFileNameUv,
                                 int barType, bool muti,
                                 CallbackCaptureAndDecodeFile callback);

        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_CaptureAndRecognizeFileCB(string imgFileNameIr, string imgFileNameWh, string imgFileNameUv,

                                 int cardType, CallbackCaptureAndRecognizeFile callback);

        // new stuff
        [DllImport("lib\\A8Capture.dll")]
        public static extern int IO_GetCardStatus(ref int status, CallbackResult callback);
        // new stuff end
    
        /***************************************************************************
        *  system api
        * ************************************************************************/
        [DllImport("user32.dll", EntryPoint = "SendMessageA")]
        public static extern int SendMessage(IntPtr hwnd, int wMsg, IntPtr wParam, string lParam);
        [DllImport("user32.dll", EntryPoint = "SendMessageA")]
        public static extern int SendMessage(IntPtr hwnd, int wMsg, IntPtr wParam, ref System.Drawing.Rectangle lParam);

        #region
        public struct BarcodeResult
        {
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4096)]
            public byte[] data;

            public int dataLen;
            public int type;
            public int x;
            public int y;
            public int w;
            public int h;
        }
        #endregion

        #region
        public struct CardDetails
        {
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
            public byte[] cnName;            // 中文姓名

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
            public byte[] cnSurname;         // 中文姓

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
            public byte[] cnGivenname;       // 中文名

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 120)]
            public byte[] enName;           // 英文姓名

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 120)]
            public byte[] enSurname;        // 英文姓

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 120)]
            public byte[] enGivenname;      // 英文名

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)]
            public byte[] cnGender;           // 中文性别

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 4)]
            public byte[] enGender;           // 英文性别

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 22)]
            public byte[] nation;            // 民族、国籍、地区代码

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 22)]
            public byte[] dateOfBirth;       // 出生日期

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 72)]
            public byte[] address;           // 住址

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 36)]
            public byte[] identityNumber;    // 身份证号码

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 36)]
            public byte[] cardNumber;        // 证件号码

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
            public byte[] cnAuthority;       // 中文签发机关

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 64)]
            public byte[] enAuthority;       // 英文签发机关

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 22)]
            public byte[] dateOfIssue;       // 有效期起始日期

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 22)]
            public byte[] dateOfExpiry;      // 有效期结束日期

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 22)]
            public byte[] dateOfDepart;      // 最晚离开日期

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 16)]
            public byte[] timesOfIssue;      // 签发次数

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 36)]
            public byte[] types;             // 证件类型

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 36)]
            public byte[] cnPlaceOfBirth;    // 中文出生地点

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 72)]
            public byte[] enPlaceOfBirth;    // 英文出生地点

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 36)]
            public byte[] cnPlaceOfIssue;    // 中文签发地点

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 72)]
            public byte[] enPlaceOfIssue;    // 英文签发地点

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 32)]
            public byte[] career;            // 职业

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 6)]
            public byte[] cardVersion;        // 证件版本号

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 46)]
            public byte[] firstMRZ;          // 第一行机读码

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 46)]
            public byte[] secondMRZ;         // 第二行机读码

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 46)]
            public byte[] thirdMRZ;          // 第三行机读码

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 1024)]
            public byte[] image;  // 头像

            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 1024)]
            public byte[] finger; // 指纹（如果有）
        }
        #endregion

        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        public delegate void CallbackResult(int result);

        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        //public delegate void CallbackCaptureAndDecodeFile(int result
        //     , string irFileName
        //     , string whFileName
        //     , string uvFileName
        //     , int barType
        //     , bool muti
        //     , ref BarcodeResult[] barcodeResult
        //  , int barcodeResultSize);
        public delegate void CallbackCaptureAndDecodeFile(int result
             , string irFileName
             , string whFileName
             , string uvFileName
             , int barType
             , bool muti
             , IntPtr barcodeResults
             , int barcodeResultSize);

        [UnmanagedFunctionPointer(CallingConvention.StdCall)]
        public delegate void CallbackCaptureAndRecognizeFile(int result
             , string irFileName
             , string whFileName
             , string uvFileName
             , int cardType
             , ref CardDetails cardDetails
             );
    }

}


