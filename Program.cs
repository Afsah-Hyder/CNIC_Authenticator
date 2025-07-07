using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace Demo
{
    static class Program
    {
        /// <summary>
        /// 应用程序的主入口点。
        /// </summary>
        [STAThread]
        // static void Main()
        // {
        //     Application.EnableVisualStyles();
        //     Application.SetCompatibleTextRenderingDefault(false);
        //     Application.Run(new Form1());
        // }
        static void Main(string[] args)
        {
            File.AppendAllText("debug_log.txt", $"Args: {string.Join(",", args)}\r\n");

            if (args.Length > 0 && args[0] == "--write-card-status")
            {
                Form1.WriteCardStatusToFile();
                return;
            }

            if (args.Length > 0 && args[0] == "--silent")
            {
                File.AppendAllText("debug_log.txt", "Silent mode triggered\r\n");
                Form1.RunCapture();
                Environment.Exit(0);
            }
            File.AppendAllText("debug_log.txt", "Normal mode triggered\r\n");
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }
    }
}
