using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Demo
{
    public partial class Form1 : Form
    {
        const int WM_SETTEXT = 0x0C;
        const int BARCODE_PDF_417 = (1 << 11);
        const int BARCODE_QR_CODE = (1 << 12);
        const int CARD_TYPE_INTERNATIONAL_ID = 7;

        int mBarcodeResultSize;
        API.CardDetails mCardDetailsRef;

        public Form1()
        {
            InitializeComponent();
            CheckForIllegalCrossThreadCalls = false;
            this.Load += Form1_Load; // Hook the Load event
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            // Automatically open device
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "app_log.txt");

            int ret = API.IO_OpenDevice(CARD_TYPE_INTERNATIONAL_ID, IntPtr.Zero);
            if (ret == 0)
            {
                API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, "Device opened successfully!");
                Variable.connected = true;

                int cardStatus = 0;
                // ret = API.IO_GetCardStatus(ref cardStatus);
                // print(ret);
                // if (ret != 0)
                // {
                //     File.AppendAllText(logPath, $"{DateTime.Now}: Failed to get card status! Return code: {ret}\r\n");
                //     return;
                // }
                // if (cardStatus != 2)
                // {
                //     File.AppendAllText(logPath, $"{DateTime.Now}: No card detected on device. Please place a card.\r\n");
                //     return;
                // }
                // --- End card status check ---

                // Automatically capture image
                ret = API.IO_CaptureFile("./ir.jpg", "./wh.jpg", "./uv.jpg", CARD_TYPE_INTERNATIONAL_ID);
                if (ret == 0)
                {
                    API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, "Images captured successfully!");
                    if (File.Exists("./wh.jpg"))
                    {
                        API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, "wh.jpg found.");
                        string imagePath = @"bin\Release\wh.jpg";
                        RunOcrOnImage(imagePath);
                    }
                    else API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, "wh.jpg not found!");
                    showImage("./ir.jpg", pictureBoxIR);
                    showImage("./wh.jpg", pictureBoxWH);
                    showImage("./uv.jpg", pictureBoxUV);
                }
                else
                {
                    API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, $"Capture failed! Return code: {ret}");
                }
            }
            else
            {
                API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, $"Device open failed! Return code: {ret}");
            }
        }

        public static void WriteCardStatusToFile()
        {
            const int CARD_TYPE_INTERNATIONAL_ID = 7;
            int ret = API.IO_OpenDevice(CARD_TYPE_INTERNATIONAL_ID, IntPtr.Zero);
            int cardStatus = 0;
            if (ret == 0)
            {
                ret = API.IO_GetCardStatus(ref cardStatus);
                // Optionally: API.IO_CloseDevice(); // If your SDK requires closing
            }
            File.WriteAllText("card_status.txt", cardStatus.ToString());
        }
        
        private void showImage(string filename, PictureBox pb)
        {
            try
            {
                FileStream pFileStream = new FileStream(filename, FileMode.Open, FileAccess.Read);
                pb.Image = Image.FromStream(pFileStream);
                pFileStream.Close();
                pFileStream.Dispose();
            }
            catch (Exception ex)
            {
                API.SendMessage(txtResult.Handle, WM_SETTEXT, IntPtr.Zero, $"Error loading image {filename}: {ex.Message}");
            }
        }

        private void RunOcrOnImage(string imagePath)
        {
            // MessageBox.Show($"About to run: python ocr_doctr.py \"{imagePath}\"", "Debug");

            var psi = new System.Diagnostics.ProcessStartInfo
            {
                FileName = "python",
                Arguments = $"ocr_doctr.py \"{imagePath}\"",
                WorkingDirectory = @"C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (var process = System.Diagnostics.Process.Start(psi))
            {
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                MessageBox.Show("Python process finished.", "Debug");

                if (!string.IsNullOrWhiteSpace(error))
                    MessageBox.Show(error, "OCR Error");

                MessageBox.Show(output, "OCR Result");
            }
        }

        public static void RunCapture()
        {
            const int CARD_TYPE_INTERNATIONAL_ID = 7;
            string logPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "capture_log.txt");
            try
            {
                // Open device
                int ret = API.IO_OpenDevice(CARD_TYPE_INTERNATIONAL_ID, IntPtr.Zero);
                if (ret == 0)
                {
                    Variable.connected = true;
                    File.AppendAllText(logPath, $"{DateTime.Now}: Device opened successfully.\r\n");

                    // --- Card status check ---
                    int cardStatus = 0;
                    ret = API.IO_GetCardStatus(ref cardStatus);
                    if (ret != 0)
                    {
                        File.AppendAllText(logPath, $"{DateTime.Now}: Failed to get card status! Return code: {ret}\r\n");
                        return;
                    }
                    if (cardStatus != 2)
                    {
                        File.AppendAllText(logPath, $"{DateTime.Now}: No card detected on device. Please place the CNIC first.\r\n");
                        // No MessageBox here, let Python UI handle feedback
                        return;
                    }
                    // --- End card status check ---

                    // Capture images
                    ret = API.IO_CaptureFile("./ir.jpg", "./wh.jpg", "./uv.jpg", CARD_TYPE_INTERNATIONAL_ID);
                    if (ret == 0)
                    {
                        File.AppendAllText(logPath, $"{DateTime.Now}: Images captured successfully.\r\n");
                        if (File.Exists("./wh.jpg"))
                        {
                            File.AppendAllText(logPath, $"{DateTime.Now}: wh.jpg found. Running OCR...\r\n");

                            // Run OCR (no UI)
                            var psi = new System.Diagnostics.ProcessStartInfo
                            {
                                FileName = "python",
                                Arguments = $"ocr_doctr.py bin\\Release\\wh.jpg",
                                WorkingDirectory = @"C:\Users\DELL\Desktop\StingRey Tech\A8Capture(V2.2.2.0)_800PX\sorcecode\C#\Demo\Demo",
                                RedirectStandardOutput = true,
                                RedirectStandardError = true,
                                UseShellExecute = false,
                                CreateNoWindow = true
                            };

                            using (var process = System.Diagnostics.Process.Start(psi))
                            {
                                string output = process.StandardOutput.ReadToEnd();
                                string error = process.StandardError.ReadToEnd();
                                process.WaitForExit();

                                File.AppendAllText(logPath, $"{DateTime.Now}: OCR Output:\r\n{output}\r\n");
                                if (!string.IsNullOrWhiteSpace(error))
                                    File.AppendAllText(logPath, $"{DateTime.Now}: OCR Error:\r\n{error}\r\n");
                            }
                        }
                        else
                        {
                            File.AppendAllText(logPath, $"{DateTime.Now}: wh.jpg not found after capture.\r\n");
                        }
                    }
                    else
                    {
                        File.AppendAllText(logPath, $"{DateTime.Now}: Capture failed! Return code: {ret}\r\n");
                    }
                }
                else
                {
                    File.AppendAllText(logPath, $"{DateTime.Now}: Device open failed! Return code: {ret}\r\n");
                }
            }
            catch (Exception ex)
            {
                File.AppendAllText(logPath, $"{DateTime.Now}: Exception: {ex.Message}\r\n");
            }
        }
        private void btnOpenDevice_Click(object sender, EventArgs e) { }
        private void btnDecodeBarcode_Click(object sender, EventArgs e) { }
        private void checkBox1_CheckedChanged(object sender, EventArgs e) { }
        private void btnRecognizeID_Click(object sender, EventArgs e) { }
        private void button1_Click(object sender, EventArgs e) { }
        private void button2_Click(object sender, EventArgs e) { }
        private void pictureBoxIR_Click(object sender, EventArgs e) { }
        private void button3_Click(object sender, EventArgs e) { }


        #region bytesToStruct
        public static object bytesToStruct(byte[] bytes, Type type)
        {
            int size = Marshal.SizeOf(type);
            if (bytes.Length < size) return null;
            IntPtr structPtr = Marshal.AllocHGlobal(size);
            Marshal.Copy(bytes, 0, structPtr, size);
            object obj = Marshal.PtrToStructure(structPtr, type);
            Marshal.FreeHGlobal(structPtr);
            return obj;
        }
        #endregion
    }
}