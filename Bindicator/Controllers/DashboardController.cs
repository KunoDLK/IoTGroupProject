using Microsoft.AspNetCore.Mvc;
using Bindicator.Data;
using Bindicator.ViewModels;
using Microsoft.EntityFrameworkCore;
using Bindicator.Models;
using Bindicator.Services;

namespace Bindicator.Controllers
{
    public class DashboardController : Controller
    {
        private readonly BinDataService _binData;
        private readonly BinTrendService _binTrend;

        public DashboardController(BinDataService binData, BinTrendService binTrend)
        {
            _binData = binData;
            _binTrend = binTrend;
        }

        public async Task<IActionResult> Index()
        {
            var viewModel = await _binData.GetLatestBinStatusesAsync();
            return View(viewModel);
        }

        public async Task<IActionResult> Trend(string postcode, string street, int binNumber)
        {
            var vm = await _binTrend.GetTrendAsync(postcode, street, binNumber);
            return View(vm);
        }
    }
}