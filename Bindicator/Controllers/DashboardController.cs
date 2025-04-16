using Bindicator.Data;
using Bindicator.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace Bindicator.Controllers
{
    public class DashboardController : Controller
    {
        private readonly BinDataService _binData;
        private readonly BinTrendService _binTrend;
        private readonly ApplicationDbContext _context;

        public DashboardController(BinDataService binData, BinTrendService binTrend, ApplicationDbContext context)
        {
            _binData = binData;
            _binTrend = binTrend;
            _context = context;
        }

        public async Task<IActionResult> Index()
        {
            var viewModel = await _binData.GetLatestBinStatusesAsync();
            return View(viewModel);
        }

        public async Task<IActionResult> Trend(string postcode, string street, int binNumber)
        {
            var viewModel = await _binTrend.GetTrendAsync(postcode, street, binNumber);
            return View(viewModel);
        }

        [HttpGet]
        public async Task<IActionResult> GetLatestBins()
        {
            var viewModel = await _binData.GetLatestBinStatusesAsync();
            return PartialView("_BinTable", viewModel);
        }

        public async Task<IActionResult> Map()
        {
            var bins = await _context.SensorReadings
                .GroupBy(b => new { b.Postcode, b.Street, b.BinNumber, b.Latitude, b.Longitude })
                .Select(g => g.OrderByDescending(b => b.Timestamp).First())
                .ToListAsync();

            return View(bins);
        }
    }
}