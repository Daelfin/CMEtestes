// Create and configure FastNoise object
using Microsoft.VisualBasic;
using System.Text;

DateTime start = DateTime.Now;

FastNoiseLite noise = new();
noise.SetNoiseType(FastNoiseLite.NoiseType.OpenSimplex2S);

int imgSize = 856;

// Gather noise data
Float[] noiseData = new Float[imgSize * imgSize];
int index = 0;

Float minValue = new(999);
float maxValue = 0;

Random random = new();
noise.SetSeed(random.Next());
noise.SetNoiseType(FastNoiseLite.NoiseType.OpenSimplex2S);
noise.SetFractalType(FastNoiseLite.FractalType.FBm);
noise.SetFrequency(0.005f);
noise.SetFractalOctaves(2);
noise.SetFractalWeightedStrength(1f);

int h = 300;    // x do centro da elipse
int k = 400;    // y do centro da elipse
int rx = 400;       // raio maior da elipse
int ry = 150;       // raio menor da elipse
double degree = 60; // angulo de inclinação da elipse em graus
double radian = degree * Math.PI / 180; // conversao para radianos


for (int y = 0; y < imgSize; y++)
{
    for (int x = 0; x < imgSize; x++)
    {
        Float valor = minValue;
        //double distance = Math.Pow(x - h, 2) / Math.Pow(rx, 2) + Math.Pow(y - k, 2) / Math.Pow(ry, 2); // versão para elipse sem rotação
        double cosa = Math.Cos(radian);
        double sina = Math.Sin(radian);
        double dd = rx * rx;
        double DD = ry * ry;
        double a = Math.Pow(cosa*(x-h)+sina*(y-k),2);
        double b = Math.Pow(sina*(x-h)-cosa*(y-k),2);
        double distance = (a/dd)+(b/DD);

        if (distance <= 1)
        {
            valor = new Float((float)((((noise.GetNoise(x, y) + 1) / 2) * 280) /** (1 - distance)*/));

            if (valor.value < minValue.value)
                minValue.value = valor.value;
            else if (valor.value > maxValue)
                maxValue = valor.value;
        }

        noiseData[index] = valor;//((valor + 1) / 2) * 245;

        index++;
    }
}

File.WriteAllText("Teste.txt", "");
StringBuilder sb = new();
foreach (Float f in noiseData)
{
    sb.Append(f.value.ToString().Replace(',', '.') + ",");
}
sb.Remove(sb.Length - 1, 1);
File.WriteAllText("Teste.txt", sb.ToString());
TimeSpan time = DateTime.Now - start;
Console.WriteLine(time.TotalSeconds);

string strCmdText;
strCmdText = "/C python generateCME.py";
System.Diagnostics.Process.Start("CMD.exe", strCmdText);

class Float
{
    public Float(float value)
    {
        this.value = value;
    }
    public float value = 999f;

    public override string ToString()
    {
        return value.ToString() + "F";
    }
}