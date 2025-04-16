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