using Bindicator.Data;
using Bindicator.Models;
using Bindicator.ViewModels;
using Microsoft.EntityFrameworkCore;

namespace Bindicator.Services
{
    /// <summary>
    /// Service to handle bin trend operations. Fetches readings for a specific bin
    /// Handles the logic for detecting spikes in fill levels
    /// </summary>
    public class BinTrendService
    {
        private readonly ApplicationDbContext _context;

        /// <summary>
        /// Initializes a new instance of the <see cref="BinTrendService"/> class.
        /// </summary>
        /// <param name="context">The application database context.</param>
        public BinTrendService(ApplicationDbContext context)
        {
            _context = context;
        }

        /// <summary>
        /// Gets the trend of bin fill levels and detects spikes.
        /// </summary>
        /// <param name="postcode">The postcode of the bin location.</param>
        /// <param name="street">The street of the bin location.</param>
        /// <param name="binNumber">The bin number.</param>
        /// <returns>A <see cref="BinTrendViewModel"/> containing the trend data and detected spikes.</returns>
        public async Task<BinTrendViewModel> GetTrendAsync(string postcode, string street, int binNumber)
        {
            var exists = await _context.SensorReadings.AnyAsync(b =>
                b.Postcode == postcode && b.Street == street && b.BinNumber == binNumber);

            if (!exists)
            {
                // Add dummy data (optional)
                var now = DateTime.UtcNow;
                var dummyReadings = new List<SensorData>
                {
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 10, Weight = 5, Density = 0.9f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now.AddMinutes(-60) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 18, Weight = 5.8f, Density = 0.95f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now.AddMinutes(-50) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 26, Weight = 6.1f, Density = 1.0f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now.AddMinutes(-40) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 29, Weight = 6.5f, Density = 1.05f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now.AddMinutes(-30) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 72, Weight = 14.8f, Density = 1.3f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now.AddMinutes(-20) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 78, Weight = 15.5f, Density = 1.4f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now.AddMinutes(-10) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 85, Weight = 16.2f, Density = 1.5f, Latitude = 54.5610, Longitude = -1.3090, Timestamp = now }
                };

                _context.SensorReadings.AddRange(dummyReadings);
                await _context.SaveChangesAsync();
            }

            var readings = await _context.SensorReadings
                .Where(b => b.Postcode == postcode && b.Street == street && b.BinNumber == binNumber)
                .OrderBy(b => b.Timestamp)
                .ToListAsync();

            var spikes = new List<SpikePoint>();

            for (int i = 1; i < readings.Count; i++)
            {
                var prev = readings[i - 1];
                var current = readings[i];
                if ((current.FillLevel - prev.FillLevel) >= 30)
                {
                    spikes.Add(new SpikePoint
                    {
                        Timestamp = current.Timestamp,
                        FromLevel = prev.FillLevel,
                        ToLevel = current.FillLevel
                    });
                }
            }

            return new BinTrendViewModel
            {
                Postcode = postcode,
                Street = street,
                BinNumber = binNumber,
                Readings = readings,
                Spikes = spikes
            };
        }
    }
}