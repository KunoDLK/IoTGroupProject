namespace Bindicator.ViewModels
{
    public class BinStatusViewModel
    {
        public string Postcode { get; set; }
        public string Street { get; set; }
        public int BinNumber { get; set; }
        public float FillLevel { get; set; }
        public float Weight { get; set; }
        public float Density { get; set; }
        public DateTime Timestamp { get; set; }
    }
}