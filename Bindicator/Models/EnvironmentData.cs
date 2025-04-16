namespace Bindicator.Models
{
    public class EnvironmentData
    {
        public int Id { get; set; }
        public string Postcode { get; set; } = string.Empty;
        public string Street { get; set; } = string.Empty;
        public int BinNumber { get; set; }
        public float Temperature { get; set; }
        public float Humidity { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
