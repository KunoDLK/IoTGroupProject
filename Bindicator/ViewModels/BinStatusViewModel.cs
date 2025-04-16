namespace Bindicator.ViewModels
{
    public class BinStatusViewModel
    {
        public string Postcode { get; set; } = string.Empty;
        public string Street { get; set; } = string.Empty; 
        public int BinNumber { get; set; }
        public float FillLevel { get; set; }
        public float Weight { get; set; }
        public float Density { get; set; }
        public DateTime Timestamp { get; set; }
        public double Latitude { get; set; }
        public double Longitude { get; set; }
    }
}