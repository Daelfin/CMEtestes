// Create and configure FastNoise object
using System.Text;

int imgSize = 856;

int frame = Convert.ToInt32(args[0]);
int seed = Convert.ToInt32(args[1]);

FastNoiseLite noise = new();
noise.SetNoiseType(FastNoiseLite.NoiseType.OpenSimplex2S);

// Gather noise data
float[] noiseData = new float[imgSize * imgSize];
int index = 0;

noise.SetSeed(seed);
noise.SetNoiseType(FastNoiseLite.NoiseType.OpenSimplex2S);
noise.SetFractalType(FastNoiseLite.FractalType.FBm);
noise.SetFrequency(0.005f);
noise.SetFractalOctaves(2);
noise.SetFractalWeightedStrength(1f);

for (int y = 0; y < imgSize; y++)
{
    for (int x = 0; x < imgSize; x++)
    {
        noiseData[index] = ((noise.GetNoise(x, y, 20 * frame) + 1) / 2) * 280;

        index++;
    }
}

string fileName = $"CMEFrame{frame}.txt";

File.WriteAllText(fileName, "");
StringBuilder sb = new();
foreach (float f in noiseData)
{
    sb.Append(f.ToString().Replace(',', '.') + ",");
}
sb.Remove(sb.Length - 1, 1);
File.WriteAllText(fileName, sb.ToString());