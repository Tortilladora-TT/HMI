using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Media;

namespace Spotify2._0
{
    public partial class Form3 : Form
    {
        SoundPlayer sonido;
        public Form3()
        {
            InitializeComponent();
        }
      



        private void button3_Click(object sender, EventArgs e)
        {
           
        }

        private void button1_Click(object sender, EventArgs e)
        {
            
        }

        private void button6_Click(object sender, EventArgs e)
        {
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            
        }

        private void button4_Click(object sender, EventArgs e)
        {
            
        }

        private void button5_Click(object sender, EventArgs e)
        {
           
        }

        private void button7_Click(object sender, EventArgs e)
        {
          
        }

        private void button8_Click(object sender, EventArgs e)
        {
            
        }

        private void button9_Click(object sender, EventArgs e)
        {
            Form2 f = new Form2();
            f.Show();
            this.Hide();
        }

        private void button10_Click(object sender, EventArgs e)
        {
            Form4 f = new Form4();
            f.Show();
            this.Hide();
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void pictureBox4_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox15_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox13_Click(object sender, EventArgs e)
        {

        }
       
            
        
        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            // Parse the input from textBox1
            if (double.TryParse(textBox1.Text, out double value))
            {
                // Check if the value exceeds 3.0
                if (value > 3.0)
                {
                    // Show an alert message
                    MessageBox.Show("Te pasaste de masa");
                }
                else
                {
                    // Check if the number is an integer
                    if (value == Math.Floor(value))
                    {
                        // If it's an integer, display with .0
                        label5.Text = value.ToString("F1");
                    }
                    else
                    {
                        // If it has decimals, display as is
                        label5.Text = value.ToString();
                    }

                    // Multiply the value by 35 and display in label6
                    int result = (int)Math.Round( value * 35);
                    
                    label8.Text =result.ToString();
                }
            }
            else
            {
                // Handle invalid input (non-numeric)
                label5.Text = "0.0";
                label8.Text = ""; 
            }

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void Form3_Load(object sender, EventArgs e)
        {

        }

        private void pictureBox19_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox21_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox22_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {
            
        }

        private void pictureBox3_Click(object sender, EventArgs e)
        {

        }
    }
}
