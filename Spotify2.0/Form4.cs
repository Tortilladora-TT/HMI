using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace Spotify2._0
{
    public partial class Form4 : Form
    {
        public Form4()
        {
            InitializeComponent();
        }


        private void Form4_Load(object sender, EventArgs e)
        {

        }

        private void button9_Click(object sender, EventArgs e)
        {
            Form2 f = new Form2();
            f.Show();
            this.Hide();
        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string valor = "1";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void textBox2_TextChanged_1(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            string valor = "2";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button3_Click(object sender, EventArgs e)
        {
            string valor = "3";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button4_Click(object sender, EventArgs e)
        {
            string valor = "4";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button5_Click(object sender, EventArgs e)
        {
            string valor = "5";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button6_Click(object sender, EventArgs e)
        {
            string valor = "6";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button7_Click(object sender, EventArgs e)
        {
            string valor = "7";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button8_Click(object sender, EventArgs e)
        {
            string valor = "8";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button11_Click(object sender, EventArgs e)
        {
            string valor = "9";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button13_Click(object sender, EventArgs e)
        {
            string valor = "0";
            // Añade el valor al final del texto actual del TextBox
            textBox2.Text += valor; // Esto concatenará el nuevo valor al texto existente
        }

        private void button12_Click(object sender, EventArgs e)
        {
            // Verifica si hay texto en el TextBox
            if (textBox2.Text.Length > 0)
            {
                // Elimina el último carácter del texto
                textBox2.Text = textBox2.Text.Substring(0, textBox2.Text.Length - 1);
            }
        }

        private void button14_Click(object sender, EventArgs e)
        {
            // Parse the input from textBox1
            if (double.TryParse(textBox2.Text, out double value))
            {
                // Check if the value is less than 4
                if (value < 4)
                {
                    // Show an alert message
                    MessageBox.Show("¡Es a partir de 4 tortillas en adelante!", "ERES TONOTO?", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
                // Check if the value exceeds 105
                else if (value > 105)
                {
                    // Show an alert message
                    MessageBox.Show("Has superado el valor máximo permitido.", "ERES TONOTO?", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
                else
                {
                    // Divide the value by 35 and display in label5
                    double result = value / 35;

                    // Format the result to a fixed number of decimal places if needed
                    label5.Text = result.ToString("F1"); // Adjust the format as needed
                }
            }
            else
            {
                // Handle invalid input (non-numeric)
                label5.Text = "0.0";
            }


        }
    }
}
