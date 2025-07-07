namespace Demo
{
    partial class Form1
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.btnOpenDevice = new System.Windows.Forms.Button();
            this.btnDecodeBarcode = new System.Windows.Forms.Button();
            this.checkBox1 = new System.Windows.Forms.CheckBox();
            this.txtResult = new System.Windows.Forms.TextBox();
            this.btnRecognizeID = new System.Windows.Forms.Button();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.pictureBoxIR = new System.Windows.Forms.PictureBox();
            this.pictureBoxWH = new System.Windows.Forms.PictureBox();
            this.pictureBoxUV = new System.Windows.Forms.PictureBox();
            this.button3 = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxIR)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxWH)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxUV)).BeginInit();
            this.SuspendLayout();
            // 
            // btnOpenDevice
            // 
            this.btnOpenDevice.Location = new System.Drawing.Point(727, 49);
            this.btnOpenDevice.Name = "btnOpenDevice";
            this.btnOpenDevice.Size = new System.Drawing.Size(191, 35);
            this.btnOpenDevice.TabIndex = 0;
            this.btnOpenDevice.Text = "Open Device";
            this.btnOpenDevice.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.btnOpenDevice.UseVisualStyleBackColor = true;
            this.btnOpenDevice.Click += new System.EventHandler(this.btnOpenDevice_Click);
            // 
            // btnDecodeBarcode
            // 
            this.btnDecodeBarcode.Location = new System.Drawing.Point(727, 251);
            this.btnDecodeBarcode.Name = "btnDecodeBarcode";
            this.btnDecodeBarcode.Size = new System.Drawing.Size(191, 35);
            this.btnDecodeBarcode.TabIndex = 1;
            this.btnDecodeBarcode.Text = "Decode Barcode（PDF417）";
            this.btnDecodeBarcode.UseVisualStyleBackColor = true;
            this.btnDecodeBarcode.Click += new System.EventHandler(this.btnDecodeBarcode_Click);
            // 
            // checkBox1
            // 
            this.checkBox1.AutoSize = true;
            this.checkBox1.Location = new System.Drawing.Point(752, 12);
            this.checkBox1.Name = "checkBox1";
            this.checkBox1.Size = new System.Drawing.Size(150, 16);
            this.checkBox1.TabIndex = 2;
            this.checkBox1.Text = "Callback funcion mode";
            this.checkBox1.UseVisualStyleBackColor = true;
            this.checkBox1.CheckedChanged += new System.EventHandler(this.checkBox1_CheckedChanged);
            // 
            // txtResult
            // 
            this.txtResult.Location = new System.Drawing.Point(12, 12);
            this.txtResult.Multiline = true;
            this.txtResult.Name = "txtResult";
            this.txtResult.Size = new System.Drawing.Size(379, 567);
            this.txtResult.TabIndex = 3;
            // 
            // btnRecognizeID
            // 
            this.btnRecognizeID.Location = new System.Drawing.Point(727, 305);
            this.btnRecognizeID.Name = "btnRecognizeID";
            this.btnRecognizeID.Size = new System.Drawing.Size(191, 35);
            this.btnRecognizeID.TabIndex = 4;
            this.btnRecognizeID.Text = "Recognize ID(Three MRZ)";
            this.btnRecognizeID.UseVisualStyleBackColor = true;
            this.btnRecognizeID.Click += new System.EventHandler(this.btnRecognizeID_Click);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(727, 138);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(191, 35);
            this.button1.TabIndex = 5;
            this.button1.Text = "Calibrate";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(727, 192);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(191, 35);
            this.button2.TabIndex = 6;
            this.button2.Text = "Capture Image File";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // pictureBoxIR
            // 
            this.pictureBoxIR.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pictureBoxIR.Location = new System.Drawing.Point(408, 11);
            this.pictureBoxIR.Name = "pictureBoxIR";
            this.pictureBoxIR.Size = new System.Drawing.Size(288, 194);
            this.pictureBoxIR.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxIR.TabIndex = 7;
            this.pictureBoxIR.TabStop = false;
            this.pictureBoxIR.Click += new System.EventHandler(this.pictureBoxIR_Click);
            // 
            // pictureBoxWH
            // 
            this.pictureBoxWH.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pictureBoxWH.Location = new System.Drawing.Point(408, 211);
            this.pictureBoxWH.Name = "pictureBoxWH";
            this.pictureBoxWH.Size = new System.Drawing.Size(288, 182);
            this.pictureBoxWH.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxWH.TabIndex = 8;
            this.pictureBoxWH.TabStop = false;
            // 
            // pictureBoxUV
            // 
            this.pictureBoxUV.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.pictureBoxUV.Location = new System.Drawing.Point(408, 399);
            this.pictureBoxUV.Name = "pictureBoxUV";
            this.pictureBoxUV.Size = new System.Drawing.Size(288, 180);
            this.pictureBoxUV.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBoxUV.TabIndex = 9;
            this.pictureBoxUV.TabStop = false;
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(727, 515);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(191, 35);
            this.button3.TabIndex = 10;
            this.button3.Text = "Exit";
            this.button3.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(957, 593);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.pictureBoxUV);
            this.Controls.Add(this.pictureBoxWH);
            this.Controls.Add(this.pictureBoxIR);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.btnRecognizeID);
            this.Controls.Add(this.txtResult);
            this.Controls.Add(this.checkBox1);
            this.Controls.Add(this.btnDecodeBarcode);
            this.Controls.Add(this.btnOpenDevice);
            this.Name = "Form1";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxIR)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxWH)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBoxUV)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button btnOpenDevice;
        private System.Windows.Forms.Button btnDecodeBarcode;
        private System.Windows.Forms.CheckBox checkBox1;
        private System.Windows.Forms.TextBox txtResult;
        private System.Windows.Forms.Button btnRecognizeID;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.PictureBox pictureBoxIR;
        private System.Windows.Forms.PictureBox pictureBoxWH;
        private System.Windows.Forms.PictureBox pictureBoxUV;
        private System.Windows.Forms.Button button3;
    }
}

