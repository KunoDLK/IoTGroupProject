using Bindicator.Models;

namespace Bindicator.ViewModels
{
    public class BinTrendViewModel
    {
        public string Postcode { get; set; }
        public string Street { get; set; }
        public int BinNumber { get; set; }
        public List<SensorData> Readings { get; set; } = new();
        public List<SpikePoint> Spikes { get; set; } = new();
    }

    public class SpikePoint
    {
        public DateTime Timestamp { get; set; }
        public float FromLevel { get; set; }
        public float ToLevel { get; set; }
    }
}
