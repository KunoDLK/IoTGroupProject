using Microsoft.AspNetCore.Mvc;
using Bindicator.Data;
using Bindicator.ViewModels;
using Microsoft.EntityFrameworkCore;
using Bindicator.Models;

namespace Bindicator.Controllers
{
    public class DashboardController : Controller
    {
        private readonly ApplicationDbContext _context;

        public DashboardController(ApplicationDbContext context)
        {
            _context = context;
        }

        public async Task<IActionResult> Index()
        {
            // Dummy data for testing
            var dummyData = new List<BinStatusViewModel>
            {
                new()
                {
                    Postcode = "TS16",
                    Street = "Formby Walk",
                    BinNumber = 1,
                    FillLevel = 95,
                    Weight = 20.4f,
                    Density = 1.8f,
                    Timestamp = DateTime.UtcNow.AddMinutes(-3)
                },
                new()
                {
                    Postcode = "TS16",
                    Street = "Alder Crescent",
                    BinNumber = 2,
                    FillLevel = 65,
                    Weight = 15.0f,
                    Density = 1.2f,
                    Timestamp = DateTime.UtcNow.AddMinutes(-10)
                },
                new()
                {
                    Postcode = "TS17",
                    Street = "Oakwood Drive",
                    BinNumber = 3,
                    FillLevel = 10,
                    Weight = 5.5f,
                    Density = 0.9f,
                    Timestamp = DateTime.UtcNow.AddMinutes(-60)
                }
            };

            return View(dummyData);

            //var allReadings = await _context.SensorReadings
            //    .OrderByDescending(b => b.Timestamp)
            //    .ToListAsync();

            //var latestBins = allReadings
            //    .GroupBy(b => new { b.Postcode, b.Street, b.BinNumber })
            //    .Select(g => g.First()) // already ordered descending
            //    .OrderByDescending(b => b.Timestamp)
            //    .ToList();

            //var viewModel = latestBins.Select(b => new BinStatusViewModel
            //{
            //    Postcode = b.Postcode,
            //    Street = b.Street,
            //    BinNumber = b.BinNumber,
            //    FillLevel = b.FillLevel,
            //    Weight = b.Weight,
            //    Density = b.Density,
            //    Timestamp = b.Timestamp
            //}).ToList();

            //return View(viewModel);
        }

        public async Task<IActionResult> Trend(string postcode, string street, int binNumber)
        {
            // Check if the bin has any readings
            if (!_context.SensorReadings.Any(b =>
                b.Postcode == postcode && b.Street == street && b.BinNumber == binNumber))
            {
                // Generate dummy data for the bin
                var now = DateTime.UtcNow;

                var dummyReadings = new List<SensorData>
                {
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 10, Weight = 5, Density = 0.9f, Timestamp = now.AddMinutes(-60) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 18, Weight = 5.8f, Density = 0.95f, Timestamp = now.AddMinutes(-50) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 26, Weight = 6.1f, Density = 1.0f, Timestamp = now.AddMinutes(-40) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 29, Weight = 6.5f, Density = 1.05f, Timestamp = now.AddMinutes(-30) },
                    // 🔺 Spike!
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 72, Weight = 14.8f, Density = 1.3f, Timestamp = now.AddMinutes(-20) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 78, Weight = 15.5f, Density = 1.4f, Timestamp = now.AddMinutes(-10) },
                    new() { Postcode = postcode, Street = street, BinNumber = binNumber, FillLevel = 85, Weight = 16.2f, Density = 1.5f, Timestamp = now }
                };

                _context.SensorReadings.AddRange(dummyReadings);
                await _context.SaveChangesAsync();
            }
            // Fetch the readings for the specified bin
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

            var vm = new BinTrendViewModel
            {
                Postcode = postcode,
                Street = street,
                BinNumber = binNumber,
                Readings = readings,
                Spikes = spikes
            };

            return View(vm);
        }
    }
}