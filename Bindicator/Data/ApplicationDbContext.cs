using Bindicator.Models;
using Microsoft.EntityFrameworkCore;

namespace Bindicator.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<SensorData> SensorReadings { get; set; }
        public DbSet<EnvironmentData> EnvironmentReadings { get; set; }
    }
}
