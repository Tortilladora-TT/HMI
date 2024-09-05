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
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\FALLING.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\ROXANE.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button6_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\SHE.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\PANINI.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button4_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\RODEO.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\TO DIE FOR.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button7_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\EARTH SONG.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button8_Click(object sender, EventArgs e)
        {
            try
            {
                sonido = new SoundPlayer(Application.StartupPath + @"\son\TATTOO.wav");
                sonido.Play();
            }
            catch (Exception ex)

            {
                MessageBox.Show("Error" + ex);
            }
        }

        private void button9_Click(object sender, EventArgs e)
        {
            if (sonido != null)
            {
                sonido.Stop();
            }
        }

        private void button10_Click(object sender, EventArgs e)
        {
            Form2 f = new Form2();
            f.Show();
            this.Hide();
        }
    }
}
